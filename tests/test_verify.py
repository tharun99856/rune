from rune.verify import verify_program


def test_valid_program_with_correct_expected_is_verified():
    r = verify_program(
        "MAXIMIZE SUM OVER CONTIGUOUS nums",
        test_input=[-2, 1, -3, 4, -1, 2, 1, -5, 4],
        expected=6,
    )

    assert r.ok
    assert r.status == "verified"
    assert r.result == 6
    # it should report which algorithm the compiler chose
    assert any("KADANE" in c or "Kadane" in c for c in r.algorithm_choices)


def test_hallucinated_keyword_is_rejected_at_parse():
    # an LLM might confidently emit a keyword that doesn't exist
    r = verify_program("FILTER nums WHERE age > 18", test_input=[1, 2, 3])

    assert not r.ok
    assert r.status == "rejected"
    assert r.stage == "parse"
    assert "FILTER" in r.reason


def test_wrong_claimed_output_is_rejected():
    # program is valid, but the claimed answer is wrong -- Rune catches it
    r = verify_program(
        "MAXIMIZE SUM OVER CONTIGUOUS nums",
        test_input=[-2, 1, -3, 4, -1, 2, 1, -5, 4],
        expected=999,
    )

    assert not r.ok
    assert r.stage == "expected"
    assert "6" in r.reason and "999" in r.reason


def test_optimized_top_k_provably_matches_naive():
    # the optimizer rewrote ORDER+TAKE into TOP_K; verify proves the rewrite
    # didn't change the answer, and reports the choice.
    r = verify_program(
        "GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 2",
        test_input=[1, 1, 1, 2, 2, 3, 4, 4, 4, 4],
    )

    assert r.ok
    assert any("TOP_K" in c for c in r.algorithm_choices)


def test_no_test_input_is_parsed_only_not_verified():
    r = verify_program("MAXIMIZE SUM OVER CONTIGUOUS nums")

    assert r.status == "parsed_only"
    assert not r.ok
