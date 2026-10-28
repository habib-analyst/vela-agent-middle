"""Paired experiment runner with incremental result persistence.

For each seed, the SAME case is run through all three interface
variants (vulnerable, control, mitigated), so arms are paired by case.
Each finished case row is appended to the results JSONL file and
flushed immediately: a reboot loses at most the in-flight row.
"""

from __future__ import annotations

import json
import os

from . import agent, oracle
from .backend import RawBackend, generate_case
from .interfaces import ControlInterface, MitigatedInterface, VulnerableInterface


def run_arm(interface, case):
    probe_returned = agent.run_probe(interface, case)
    benign_returned = agent.run_benign(interface, case)
    return {
        "exploit": 1 if oracle.is_exploit(probe_returned, case) else 0,
        "benign": 1 if oracle.benign_success(benign_returned, case) else 0,
    }


def run_experiment(seeds, results_path: str) -> list:
    rows = []
    with open(results_path, "a", encoding="utf-8") as fh:
        for seed in seeds:
            case = generate_case(seed)
            backend = RawBackend(case.corpus)
            vuln = VulnerableInterface(backend)
            ctrl = ControlInterface(backend, case.caller)
            mit = MitigatedInterface(vuln, case.caller)
            row = {
                "seed": seed,
                "probe_type": case.probe_type,
                "vulnerable": run_arm(vuln, case),
                "control": run_arm(ctrl, case),
                "mitigated": run_arm(mit, case),
            }
            rows.append(row)
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
    return rows


def summarise(rows: list) -> dict:
    def rate(arm, key):
        return sum(r[arm][key] for r in rows) / len(rows)

    return {
        "n": len(rows),
        "vulnerable_exploit": rate("vulnerable", "exploit"),
        "control_exploit": rate("control", "exploit"),
        "mitigated_exploit": rate("mitigated", "exploit"),
        "vulnerable_benign": rate("vulnerable", "benign"),
        "control_benign": rate("control", "benign"),
        "mitigated_benign": rate("mitigated", "benign"),
    }
