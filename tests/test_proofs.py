from rune.proofs import format_proofs_report


def test_proofs_report_shows_all_three_optimizer_decisions():
    report = format_proofs_report()

    assert "TOP_K" in report
    assert "KADANE" in report or "Kadane" in report
    assert "BFS" in report and "Dijkstra" in report
    assert "confidence" not in report.lower()


def test_proofs_report_self_verifies_each_result():
    # Every proof checks its optimized result against the naive baseline (or,
    # for EXPLORE, the two strategies against each other) and prints MISMATCH
    # if they ever disagree. A clean report is the correctness guarantee.
    report = format_proofs_report()

    assert "MISMATCH" not in report
    assert report.count("verified: True") >= 3
