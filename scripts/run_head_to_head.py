"""Head-to-head run (G2/G3). PREREG-locked: seeds 5000-5199, n=200,
paired bootstrap B=10000 seed 12345. Rows are appended incrementally
to results/head_to_head_rows.jsonl as each case finishes.

Usage:
  python3 scripts/run_head_to_head.py            # full run
  python3 scripts/run_head_to_head.py --check    # determinism rerun:
      re-runs to a temp file and compares SHA-256 with the recorded run.
"""

import hashlib
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vela_agent_middle.experiment import run_experiment, summarise
from vela_agent_middle.stats import paired_bootstrap_ci

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def analyse(rows):
    s = summarise(rows)
    gap, glo, ghi = paired_bootstrap_ci(
        [r["vulnerable"]["exploit"] for r in rows],
        [r["control"]["exploit"] for r in rows],
    )
    red, rlo, rhi = paired_bootstrap_ci(
        [r["vulnerable"]["exploit"] for r in rows],
        [r["mitigated"]["exploit"] for r in rows],
    )
    return {
        **s,
        "seeds": "5000-5199",
        "gap_vuln_minus_control": gap,
        "gap_ci95": [glo, ghi],
        "reduction_vuln_minus_mitigated": red,
        "reduction_ci95": [rlo, rhi],
        "benign_utility_drop_mitigated_minus_vulnerable": (
            s["mitigated_benign"] - s["vulnerable_benign"]
        ),
        "g2_pass": bool(glo > 0 and gap >= 0.30),
        "g3_pass": bool(
            rlo > 0
            and red >= 0.30
            and s["mitigated_benign"] >= s["vulnerable_benign"] - 0.05
        ),
    }


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    check = "--check" in sys.argv
    rows_path = os.path.join(ROOT, "results", "head_to_head_rows.jsonl")
    if check:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl")
        tmp.close()
        rows = run_experiment(range(5000, 5200), tmp.name)
        digest = sha256_of(tmp.name)
        summary_path = os.path.join(ROOT, "results", "head_to_head_summary.json")
        with open(summary_path) as fh:
            recorded = json.load(fh)
        print(json.dumps({
            "rerun_sha256": digest,
            "recorded_sha256": recorded.get("rows_sha256"),
            "deterministic_match": digest == recorded.get("rows_sha256"),
        }, indent=2))
        os.remove(tmp.name)
        return
    if os.path.exists(rows_path):
        os.remove(rows_path)
    rows = run_experiment(range(5000, 5200), rows_path)
    out = analyse(rows)
    out["rows_sha256"] = sha256_of(rows_path)
    with open(os.path.join(ROOT, "results", "head_to_head_summary.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
