import pytest

from rune.ai import _strip_fences, english_to_verified_rune, propose_rune


def test_strip_fences_removes_markdown_code_blocks():
    text = "```rune\nMAXIMIZE SUM OVER CONTIGUOUS nums\n```"
    assert _strip_fences(text) == "MAXIMIZE SUM OVER CONTIGUOUS nums"


def test_full_loop_verifies_a_good_llm_proposal():
    # stub the LLM: it "proposes" a correct Rune program
    def fake_llm(_english):
        return "MAXIMIZE SUM OVER CONTIGUOUS nums"

    source, result = english_to_verified_rune(
        "largest contiguous chunk sum of nums",
        test_input=[-2, 1, -3, 4, -1, 2, 1, -5, 4],
        expected=6,
        propose=fake_llm,
    )

    assert source == "MAXIMIZE SUM OVER CONTIGUOUS nums"
    assert result.ok
    assert any("KADANE" in c or "Kadane" in c for c in result.algorithm_choices)


def test_full_loop_rejects_a_hallucinated_llm_proposal():
    # stub the LLM: it "proposes" a program using a keyword that doesn't exist
    def fake_llm(_english):
        return "FILTER nums WHERE x > 5"

    source, result = english_to_verified_rune("keep big numbers", test_input=[1, 9], propose=fake_llm)

    assert not result.ok
    assert result.stage == "parse"


def test_propose_rune_errors_clearly_without_a_key(monkeypatch):
    # simulate a machine with neither an env var nor a .env file present
    monkeypatch.setattr("rune.ai._load_dotenv", lambda: None)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
        propose_rune("anything")
