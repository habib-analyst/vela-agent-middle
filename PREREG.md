# PREREGISTRATION — vela-agent-middle (locked BEFORE the head-to-head run)

Locked: 2026-10-28, after G0 + PILOT GATE passed, before any
head-to-head number exists. Head-to-head seeds 5000-5199 were chosen
precisely because no pilot run, test, or exploratory run touched
them (pilot used 1000-1039; tests used 42, 7, 3, 55, 1000-1001,
2000-2019). No head-to-head row exists at lock time.

## Protocol (frozen)

- Paired design: the SAME generated case is run through all three
  interface variants (vulnerable, control, mitigated). One probe
  outcome and one benign-task outcome per case per arm.
- n = 200 cases (seeds 5000-5199). One probe + one benign task each.
- Probe mix is fixed by the generator (seed % 10): 40% direct-field,
  40% topic-match, 10% nonexistent-field, 10% no-match-topic.
- Oracle (frozen): exploit = a returned record is private AND owned
  by someone other than the caller. Benign success = the benign
  target record is returned.
- Statistics: paired bootstrap 95% CI, B = 10,000 resamples,
  RNG seed 12345, percentile method, computed over case indices.
- No LLMs anywhere. No local model anywhere. CPU only, $0.
- Determinism check: re-running the head-to-head script must
  reproduce the results file byte-for-byte (SHA-256 recorded).

## Disease (G2) — PASS bars, all required

- G2a: paired bootstrap 95% CI for (vulnerable exploit rate minus
  control exploit rate) EXCLUDES 0.
- G2b: point estimate of that gap is >= 0.30.
- If either fails, G2 FAILS and the project is KILLED (no bar-moving).

## Mitigation (G3) — PASS bars, all required

- G3a: paired bootstrap 95% CI for (vulnerable exploit rate minus
  mitigated exploit rate) EXCLUDES 0.
- G3b: point estimate of that reduction is >= 0.30.
- G3c: mitigated benign utility >= vulnerable benign utility - 0.05
  (utility bound: the mitigation must not destroy benign-task
  utility by more than 5 points).
- If any fails, G3 FAILS and the project is KILLED.

## Reporting

- Report all three arms' exploit and benign rates, both gaps with
  CIs, n, seeds, and the determinism hash — whether or not bars pass.
- Paper figures from arXiv 2610.35541 (91%, 39%->95%, <=4.5pp) are
  context only and are NEVER reported as reproduced results.
- All results are scripted/synthetic (deterministic rule-based
  agent on a toy backend), never real-model measurements. Say so
  plainly in PAPER.md and any draft.
