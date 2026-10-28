"""Pilot run (PILOT GATE). Seeds 1000-1039, n=40. Distinct from
head-to-head seeds, so pilot numbers never contaminate the PREREG run.
Writes rows incrementally to results/pilot_rows.jsonl, then prints a
summary with paired bootstrap CIs.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vela_agent_middle.experiment import run_experiment, summarise
from vela_agent_middle.stats import paired_bootstrap_ci

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    rows_path = os.path.join(ROOT, "results", "pilot_rows.jsonl")
    if os.path.exists(rows_path):
        os.remove(rows_path)
    rows = run_experiment(range(1000, 1040), rows_path)
    s = summarise(rows)
    gap, lo, hi = paired_bootstrap_ci(
        [r["vulnerable"]["exploit"] for r in rows],
        [r["control"]["exploit"] for r in rows],
    )
    out = {
        **s,
        "gap_vuln_minus_control": gap,
        "gap_ci95": [lo, hi],
        "seeds": "1000-1039",
    }
    with open(os.path.join(ROOT, "results", "pilot_summary.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
