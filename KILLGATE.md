# KILLGATE — vela-agent-middle (project #88)

Paper: arXiv 2610.35541, "The Agent in the Middle: How AI-Mediated Access
Reshapes Web Vulnerability Exploitation" (Ruozhao Yang, Jiongchi Yu,
Ming Hu, Xiaofei Xie; submitted 26 Oct 2026). Abstract read live from
arxiv.org/abs/2610.35541 on 2026-10-28.

Live-abstract claims (CONTEXT ONLY, never presented as reproduced):
- VELA, an executable benchmark: 44 vulnerabilities across 12 web
  application families; agent-facing interfaces derived from legitimate
  workflows; 3 commercial agents; independent oracles.
- "91% of vulnerabilities remain exploitable under the reference design"
  (agent realizes every attack direct interface invocation realizes).
- Interface design moves retention 39% -> 95%, vs at most 4.5 points
  across agents; restrictive interfaces also limit legitimate workflows.
- No case-level loss in the reference configuration attributed to agent
  refusal or input normalization; one case the agent completed an attack
  by supplying calls the attacker omitted.
- The abstract page shows NO author-code link (only generic
  arXivLabs/Code-Data toggle placeholders, no repository URL).

Gate order is conjunctive. Any FAIL = KILL (KILLED.md + negative
PAPER.md, no repo/push/draft). Bars are never moved after locking.

## Gate verdicts

- STEP 0 — live abstract read: PASS (2026-10-28; claims above).
- G1 — author-code recheck: PASS (2026-10-28). Searched: arXiv abs page
  code links (none shown), exact-title web search, author-name web
  search ("Ruozhao Yang" + VELA + GitHub), and benchmark-description
  search. No official author repository found. Paper is 2 days old at
  build time; absence is as of 2026-10-28 and is re-checked before any
  future push. This is a web-search absence, not an exhaustive GitHub
  API proof — stated honestly in PAPER.md.
- G0 — harness + tests green: PASS (2026-10-28; pytest 11/11:
  4 backend, 5 interface/oracle, 2 stats tests).
- PILOT GATE — clean scripted regime calibration: PASS (2026-10-28;
  seeds 1000-1039, n=40: vulnerable exploit 0.800, control exploit
  0.000, gap 0.800, paired bootstrap 95% CI [0.675, 0.925];
  benign utility 1.000 on all three arms; mitigated exploit 0.000).
  The vulnerable regime is measurable, the control regime is not
  exploitable, and benign utility is intact — calibration sane,
  no bar-moving: head-to-head bars are locked in PREREG.md next,
  on a fresh seed range (5000-5199) untouched by pilot or tests.
- G2 — disease, PREREG-locked bars: PASS (2026-10-28; head-to-head
  seeds 5000-5199, n=200, PREREG locked before the run: vulnerable
  exploit 0.800, control exploit 0.000, gap 0.800, paired bootstrap
  95% CI [0.745, 0.855] — excludes 0 and >= 0.30).
- G3 — mitigation under the same protocol: PASS (2026-10-28; same
  run: mitigated exploit 0.000, reduction 0.800, 95% CI [0.745,
  0.855] — excludes 0 and >= 0.30; mitigated benign utility 1.000
  vs vulnerable 1.000, drop 0.000 within the 0.05 bound).
- Determinism: head-to-head rerun SHA-256 matches the recorded run
  (68cf8a3959130d550108d0b22c8ee37fb52773d5b206475a8941330dcc69d321).
- OVERALL: ALL GATES PASS — staged payload only; no push made by
  this builder (REPO NEEDED via the parent's browser flow).

## Notes

- Defensive audit study only. Synthetic toy backend built by the
  builder; no real product, service, account, or third-party system is
  probed, attacked, or interacted with. No real credentials. No
  exploit instructions for real systems are written anywhere in this
  project.
- No LLMs in the measurement loop. The "agent" is a deterministic
  rule-based script. No local model is used anywhere.
- CPU only, $0 cost, no paid APIs, no pushes, no repo creation,
  no LinkedIn queue touches, no contacting anyone.
