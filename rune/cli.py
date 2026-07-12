import sys

from rune.stats import (
    compute_concept_trend,
    compute_review_queue,
    compute_stats,
    format_report,
    load_ledger,
)

REVIEW_THRESHOLD = 15

# Concepts that crossed the review threshold and have since been resolved.
# Kept here so `rune mine` reports their real disposition instead of stale
# "ready to investigate". A concept is resolved by a decision recorded in
# docs/language/decisions/DECISIONS.md, not by editing this dict alone.
RESOLVED_CONCEPTS = {
    "Traversal": "resolved: promoted to EXPLORE (docs/language/primitives/EXPLORE.md)",
    "Stateful Scan": (
        "resolved: dissolved, not a concept "
        "(docs/language/research/2026-07-09-stateful-scan-dissolved.md)"
    ),
}


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
        status = RESOLVED_CONCEPTS.get(entry["concept"], "ready to investigate")
        lines.append(f"  {entry['concept']} - {entry['count']} occurrences, {status}")

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

    if argv and argv[0] == "proofs":
        from rune.proofs import format_proofs_report

        print(format_proofs_report())
        return 0

    if argv and argv[0] == "verify":
        from rune.verify import format_verification_demo

        print(format_verification_demo())
        return 0

    if argv and argv[0] == "ai":
        task = " ".join(argv[1:]).strip()
        if not task:
            print('usage: python -m rune.cli ai "<plain-English task>"')
            print("(needs GROQ_API_KEY set in your environment)")
            return 1
        from rune.ai import english_to_verified_rune

        try:
            source, result = english_to_verified_rune(task)
        except Exception as e:  # noqa: BLE001 - surface any LLM/network error plainly
            print(f"LLM call failed: {e}")
            print("(needs GROQ_API_KEY set, and network access to Groq)")
            return 1

        print(f'You asked (English): "{task}"')
        print("LLM proposed this Rune:")
        for line in source.splitlines():
            print(f"    {line}")
        if result.status == "verified":
            print(f"Rune verdict: VERIFIED -- {result.reason}")
        elif result.status == "parsed_only":
            print("Rune verdict: VALID RUNE (parses & optimizes; pass test data to prove behavior)")
        else:
            print(f"Rune verdict: REJECTED at [{result.stage}] -- {result.reason}")
        for c in result.algorithm_choices:
            print(f"    compiler would choose: {c.split('  (')[0]}")
        return 0

    print("usage: python -m rune.cli [stats|mine|demo|complexity|explain|proofs|verify|ai]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
