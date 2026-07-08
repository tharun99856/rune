from rune.explain import format_explain_report


def test_explain_report_shows_rule_reason_and_complexity_before_after():
    report = format_explain_report(top_k_kwargs={"data_size": 2000, "domain_size": 200, "seed": 1})

    assert "Rewrite applied" in report
    assert "ORDER" in report and "TAKE" in report and "TOP_K" in report
    assert "Before:" in report and "After:" in report
    assert "O(n log n)" in report and "O(n log k)" in report
    assert "Measured" in report
    assert "confidence" not in report.lower()
