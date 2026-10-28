"""Paired bootstrap confidence intervals for a difference of rates.

Resamples case indices with replacement (fixed RNG seed), recomputes
the per-arm mean difference on each resample, and returns the
percentile 95% interval. Deterministic given (x, y, n_boot, seed).
"""

from __future__ import annotations

import random


def paired_bootstrap_ci(x: list, y: list, n_boot: int = 10000, seed: int = 12345):
    """CI for mean(x) - mean(y); x, y are paired 0/1 lists of equal length."""
    assert len(x) == len(y) and len(x) > 0
    rng = random.Random(seed)
    n = len(x)
    diffs = []
    for _ in range(n_boot):
        s = 0
        for _ in range(n):
            i = rng.randrange(n)
            s += x[i] - y[i]
        diffs.append(s / n)
    diffs.sort()
    lo = diffs[int(0.025 * n_boot)]
    hi = diffs[int(0.975 * n_boot)]
    return sum(x) / n - sum(y) / n, lo, hi
