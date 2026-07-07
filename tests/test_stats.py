from rune.stats import (
    compute_concept_trend,
    compute_review_queue,
    compute_stats,
    format_report,
    load_ledger,
)


def _rows():
    return [
        {"id": "1", "problem": "A", "category": "Arrays", "outcome": "WORKS", "concept": "Grouping"},
        {"id": "2", "problem": "B", "category": "Arrays", "outcome": "GAP", "concept": "Window"},
        {"id": "3", "problem": "C", "category": "Graphs", "outcome": "GAP", "concept": "Traversal"},
    ]


def test_total_counts_all_rows():
    stats = compute_stats(_rows())

    assert stats["total"] == 3


def test_outcome_counts_tally_by_outcome():
    stats = compute_stats(_rows())

    assert stats["outcome_counts"] == {"WORKS": 1, "GAP": 2}


def test_category_coverage_is_percent_works_per_category():
    stats = compute_stats(_rows())

    assert stats["category_coverage"] == {"Arrays": 50, "Graphs": 0}


def test_concept_counts_tally_across_rows():
    stats = compute_stats(_rows())

    assert stats["concept_counts"] == {"Grouping": 1, "Window": 1, "Traversal": 1}


def test_load_ledger_reads_csv_rows(tmp_path):
    csv_path = tmp_path / "ledger.csv"
    csv_path.write_text(
        "id,problem,category,outcome,concept\n"
        "1,Top K Frequent,Arrays,WORKS,Grouping;Ordering;Selection\n"
    )

    rows = load_ledger(csv_path)

    assert rows == [
        {
            "id": "1",
            "problem": "Top K Frequent",
            "category": "Arrays",
            "outcome": "WORKS",
            "concept": "Grouping;Ordering;Selection",
        }
    ]


def test_format_report_contains_total_and_outcome_labels():
    report = format_report(compute_stats(_rows()))

    assert "Problems tested: 3" in report
    assert "Works: 1" in report
    assert "Missing concept: 2" in report


def test_format_report_contains_category_coverage_and_concept_frequency():
    report = format_report(compute_stats(_rows()))

    assert "Arrays" in report and "50%" in report
    assert "Grouping" in report
    assert "Traversal" in report


def _batched_rows():
    return [
        {"id": "1", "concept": "Grouping;Ordering", "batch": "1"},
        {"id": "2", "concept": "Grouping", "batch": "1"},
        {"id": "3", "concept": "Window", "batch": "1"},
        {"id": "4", "concept": "Window;Traversal", "batch": "2"},
        {"id": "5", "concept": "Traversal", "batch": "2"},
    ]


def test_concept_trend_reports_new_concepts_per_batch():
    trend = compute_concept_trend(_batched_rows())

    assert trend == [
        {"batch": "1", "problems": 3, "cumulative_concepts": 3, "new_concepts": 3},
        {"batch": "2", "problems": 2, "cumulative_concepts": 4, "new_concepts": 1},
    ]


def test_review_queue_flags_concepts_at_or_above_threshold():
    rows = [{"concept": "Window"}] * 3 + [{"concept": "Grouping"}] * 5

    queue = compute_review_queue(rows, threshold=5)

    assert queue == [{"concept": "Grouping", "count": 5}]


def test_review_queue_is_empty_below_threshold():
    rows = [{"concept": "Window"}] * 3

    queue = compute_review_queue(rows, threshold=5)

    assert queue == []
