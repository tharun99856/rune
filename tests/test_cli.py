from rune.cli import main


def test_stats_command_returns_zero_and_prints_report(capsys):
    exit_code = main(["stats"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Problems tested:" in captured.out


def test_unknown_command_returns_nonzero():
    exit_code = main(["bogus"])

    assert exit_code != 0


def test_mine_command_returns_zero_and_prints_trend_and_queue(capsys):
    exit_code = main(["mine"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Concept trend" in captured.out
    assert "Review queue" in captured.out
    assert "confidence" not in captured.out.lower()


def test_mine_marks_resolved_concepts_not_ready_to_investigate(capsys):
    # Both Traversal (promoted to EXPLORE) and Stateful Scan (dissolved) are
    # over the review threshold but already resolved -- the tool must not keep
    # calling them "ready to investigate", which would be stale and misleading.
    main(["mine"])
    out = capsys.readouterr().out

    assert "promoted" in out  # Traversal
    assert "dissolved" in out  # Stateful Scan


def test_demo_command_returns_zero_and_prints_the_pipeline(capsys):
    exit_code = main(["demo"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Rewrote:" in captured.out
    assert "MISMATCH" not in captured.out


def test_proofs_command_shows_all_three_and_returns_zero(capsys):
    exit_code = main(["proofs"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "TOP_K" in captured.out
    assert "Dijkstra" in captured.out
    assert "KADANE" in captured.out or "Kadane" in captured.out
    assert "MISMATCH" not in captured.out


def test_verify_command_shows_verified_and_rejected(capsys):
    exit_code = main(["verify"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "VERIFIED" in captured.out
    assert "REJECTED" in captured.out
