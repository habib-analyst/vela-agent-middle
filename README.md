# vela-agent-middle — Defensive audit: does the interface set exploitability?

A defensive, synthetic replication of the *mechanism* behind arXiv
2610.35541, "The Agent in the Middle: How AI-Mediated Access Reshapes
Web Vulnerability Exploitation" (Yang, Yu, Hu, Xie; submitted 26 Oct
2026). That paper's VELA benchmark (44 vulnerabilities, 12 web app
families, 3 commercial agents) found ~91% of vulnerabilities remained
exploitable under a reference interface design, with interface design
moving retention 39% -> 95% vs at most 4.5 points across agents.
**Those figures are context only. Nothing here reproduces them.**

What this project measures instead, on a toy backend it builds
itself: whether a permissive interface design makes a synthetic
backend exploitable to a scripted caller while a restricted design
does not, and whether a defensive wrapper retrofitted onto the
permissive interface removes the effect without harming benign tasks.

## What is (and is not) here

- A synthetic in-memory store of invented notes (owner, visibility,
  topic, title). No real system, account, credential, or data is
  touched. No exploit instructions for real systems are included.
- A deterministic rule-based "agent" (fixed search calls). **No LLM
  is used anywhere in the measurement loop, and no local model is
  used anywhere at all.**
- Three interface variants over the SAME backend: `vulnerable`
  (raw search, any field, no visibility filter), `control`
  (allowlisted fields + visibility filter), `mitigated` (vulnerable
  interface + integrity check + result verification wrapper).
- An independent oracle: exploit = a returned record is private AND
  owned by someone other than the caller.

## Measured results (head-to-head, PREREG-locked)

- n = 200 paired cases, seeds 5000-5199. Paired bootstrap 95% CIs,
  B = 10,000, seed 12345.
- Vulnerable exploit rate: **0.800**; control: **0.000**;
  gap **0.800, 95% CI [0.745, 0.855]** (G2 PASS).
- Mitigated exploit rate: **0.000**; reduction vs vulnerable:
  **0.800, 95% CI [0.745, 0.855]** (G3 PASS).
- Benign-task utility: **1.000 on all three arms**; mitigated drop
  **0.000**, within the PREREG 0.05 bound.
- Pilot (seeds 1000-1039, n=40): gap 0.800, 95% CI [0.675, 0.925].
- Determinism: rerun SHA-256
  `68cf8a3959130d550108d0b22c8ee37fb52773d5b206475a8941330dcc69d321`
  matches the recorded run.

## Honest limits (read before citing any number)

- These are **scripted/synthetic** results, not real-model
  measurements. The agent is a fixed rule, so the 0.800 vulnerable
  rate is set by the probe mix (80% of probes are the two
  succeeding types) — it is a demonstration of the interface
  mechanism, not an estimate of real-world exploitability.
- Control/mitigated exploit rates are 0.000 **by construction**
  (allowlist + visibility filter provably block the probe types
  used). The mitigated arm equals the control arm on this toy; the
  measured claim is reduction + utility preservation, not a novel
  defense mechanism.
- The toy has no real vulnerabilities, no real agents, and no
  commercial models. Generalisation to real agent-facing services
  is unproven by this study.

## Run it

```bash
python3 -m pytest tests/ -q            # G0: 11 tests
python3 scripts/run_pilot.py           # pilot, seeds 1000-1039
python3 scripts/run_head_to_head.py    # PREREG run, seeds 5000-5199
python3 scripts/run_head_to_head.py --check  # determinism rerun
```

CPU only, $0 cost, no network, no paid APIs. Results rows are
appended incrementally to `results/*.jsonl` as each case finishes.

## Files

- `src/vela_agent_middle/` — backend, interfaces, agent, oracle,
  experiment runner, bootstrap stats.
- `tests/` — pytest suite (G0).
- `scripts/` — pilot + head-to-head runners.
- `results/` — pilot + head-to-head rows and summaries.
- `PREREG.md` — bars locked before the head-to-head run.
- `KILLGATE.md` — per-gate verdicts.
- `LICENSE` — MIT.

## Safety

Defensive audit research. If you adapt this code, keep it on
synthetic backends you own. Do not point it at real products,
services, or accounts.
