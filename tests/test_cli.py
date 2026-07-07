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
