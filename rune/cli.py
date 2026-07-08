import sys

from rune.stats import (
    compute_concept_trend,
    compute_review_queue,
    compute_stats,
    format_report,
    load_ledger,
)

REVIEW_THRESHOLD = 15


def _format_mine_report(rows):
    lines = ["Concept trend (new concepts per batch):"]
    for entry in compute_concept_trend(rows):
        lines.append(
            f"  batch {entry['batch']}: {entry['problems']} problems, "
            f"+{entry['new_concepts']} new concepts "
            f"({entry['cumulative_concepts']} cumulative)"
        )

    lines.append("")
    lines.append(f"Review queue (concept count >= {REVIEW_THRESHOLD}):")
    queue = compute_review_queue(rows, threshold=REVIEW_THRESHOLD)
    if not queue:
        lines.append("  (none yet)")
    for entry in queue:
        lines.append(f"  {entry['concept']} - {entry['count']} occurrences, ready to investigate")

    lines.append("")
    lines.append("This is a count, not a verdict. No merges or splits are")
    lines.append("auto-detected here -- crossing the threshold means 'go read")
    lines.append("the problems', not 'this is decided'. See")
    lines.append("docs/language/research/README.md.")
    return "\n".join(lines)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if argv and argv[0] == "stats":
        rows = load_ledger()
        print(format_report(compute_stats(rows)))
        return 0

    if argv and argv[0] == "mine":
        rows = load_ledger()
        print(_format_mine_report(rows))
        return 0

    if argv and argv[0] == "demo":
        from rune.demo import run_demo

        print(run_demo())
        return 0

    if argv and argv[0] == "complexity":
        from rune.complexity import format_complexity_report

        print(format_complexity_report())
        return 0

    if argv and argv[0] == "explain":
        from rune.explain import format_explain_report

        print(format_explain_report())
        return 0

    print("usage: python -m rune.cli [stats|mine|demo|complexity|explain]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
