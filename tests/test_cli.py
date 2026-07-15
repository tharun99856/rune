import json

from rune.cli import main


def test_run_executes_a_program_file_against_json_data(tmp_path, capsys):
    prog = tmp_path / "topk.rn"
    prog.write_text("GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 2\n")
    data = tmp_path / "data.json"
    data.write_text(json.dumps([1, 1, 1, 2, 2, 3, 4, 4, 4, 4]))

    exit_code = main(["run", str(prog), "--data", str(data)])

    out = capsys.readouterr().out
    assert exit_code == 0
    assert out.splitlines()[:2] == ["4: 4", "1: 3"]


def test_run_executes_an_objective_and_prints_the_scalar(tmp_path, capsys):
    prog = tmp_path / "kadane.rn"
    prog.write_text("MAXIMIZE SUM OVER CONTIGUOUS nums\n")
    data = tmp_path / "data.json"
    data.write_text(json.dumps([-2, 1, -3, 4, -1, 2, 1, -5, 4]))

    exit_code = main(["run", str(prog), "--data", str(data)])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "6"


def test_run_executes_explore_on_a_json_graph(tmp_path, capsys):
    prog = tmp_path / "path.rn"
    prog.write_text("EXPLORE graph FROM a TO d\n")
    data = tmp_path / "graph.json"
    data.write_text(json.dumps({"a": [["b", 1], ["c", 1]], "b": [["d", 1]], "c": [["d", 1]], "d": []}))

    exit_code = main(["run", str(prog), "--data", str(data)])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "2"


def test_run_with_explain_shows_the_compiler_choice(tmp_path, capsys):
    prog = tmp_path / "topk.rn"
    prog.write_text("GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 2\n")
    data = tmp_path / "data.json"
    data.write_text(json.dumps([1, 1, 2]))

    exit_code = main(["run", str(prog), "--data", str(data), "--explain"])

    out = capsys.readouterr().out
    assert exit_code == 0
    assert "TOP_K" in out


def test_run_with_missing_program_file_fails_helpfully(tmp_path, capsys):
    data = tmp_path / "data.json"
    data.write_text("[1]")

    exit_code = main(["run", str(tmp_path / "nope.rn"), "--data", str(data)])

    out = capsys.readouterr().out
    assert exit_code != 0
    assert "nope.rn" in out


def test_run_without_data_prints_usage(tmp_path, capsys):
    prog = tmp_path / "p.rn"
    prog.write_text("TAKE 1\n")

    exit_code = main(["run", str(prog)])

    out = capsys.readouterr().out
    assert exit_code != 0
    assert "--data" in out


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


def test_ai_command_without_a_task_prints_usage(capsys):
    # no network: the no-argument path must fail fast with a helpful message
    exit_code = main(["ai"])

    captured = capsys.readouterr()
    assert exit_code != 0
    assert "usage" in captured.out.lower()
    assert "GROQ_API_KEY" in captured.out
