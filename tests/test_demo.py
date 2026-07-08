from rune.demo import run_demo


def test_demo_shows_source_optimizer_explanation_and_timings():
    output = run_demo(data_size=1000, domain_size=50, seed=1)

    assert "GROUP nums BY value" in output
    assert "ORDER_TAKE_TO_TOP_K" not in output  # internal rule name, not for humans
    assert "Rewrote:" in output
    assert "TOP_K" in output
    assert "Naive" in output and "Optimized" in output
    assert "ms" in output


def test_demo_raises_if_optimized_result_ever_disagrees_with_naive():
    # Correctness is checked inside run_demo itself -- a presentable demo
    # that silently shows a wrong number is worse than no demo at all.
    output = run_demo(data_size=1000, domain_size=50, seed=1)

    assert "MISMATCH" not in output
