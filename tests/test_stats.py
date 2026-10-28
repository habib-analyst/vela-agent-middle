import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vela_agent_middle.stats import paired_bootstrap_ci


def test_bootstrap_deterministic_and_excludes_zero_for_clear_gap():
    x = [1] * 80 + [0] * 20
    y = [0] * 100
    diff, lo, hi = paired_bootstrap_ci(x, y, n_boot=2000, seed=12345)
    assert diff == 0.8
    assert lo > 0
    diff2, lo2, hi2 = paired_bootstrap_ci(x, y, n_boot=2000, seed=12345)
    assert (diff, lo, hi) == (diff2, lo2, hi2)


def test_bootstrap_zero_gap_interval_covers_zero():
    x = [1, 0] * 50
    y = [1, 0] * 50
    diff, lo, hi = paired_bootstrap_ci(x, y, n_boot=2000, seed=1)
    assert diff == 0.0
    assert lo <= 0 <= hi
