"""Deterministic scripted agent (NOT an LLM, NOT a model).

The agent is a fixed rule: for a probe it issues exactly the one
search call the probe specifies; for a benign task it searches for
the benign topic. No reasoning, no sampling, no external calls.
This isolates the interface effect: the agent's behaviour is
identical across interface variants, so any outcome gap is caused
by the interface, by construction and by measurement.
"""

from __future__ import annotations

from .backend import Case


def run_probe(interface, case: Case) -> list:
    return interface.search(case.probe_field, case.probe_value)


def run_benign(interface, case: Case) -> list:
    return interface.search("topic", case.benign_topic)
