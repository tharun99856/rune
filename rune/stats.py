import csv
from collections import Counter
from pathlib import Path

DEFAULT_LEDGER_PATH = Path(__file__).resolve().parent.parent / "docs" / "language" / "ledger.csv"


def load_ledger(path=DEFAULT_LEDGER_PATH):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_stats(rows):
    total = len(rows)
    outcome_counts = dict(Counter(row["outcome"] for row in rows))

    category_totals = Counter(row["category"] for row in rows)
    category_works = Counter(row["category"] for row in rows if row["outcome"] == "WORKS")
    category_coverage = {
        category: round(100 * category_works.get(category, 0) / count)
        for category, count in category_totals.items()
    }

    concept_counts = Counter()
    for row in rows:
        for concept in row["concept"].split(";"):
            concept = concept.strip()
            if concept:
                concept_counts[concept] += 1

    return {
        "total": total,
        "outcome_counts": outcome_counts,
        "category_coverage": category_coverage,
        "concept_counts": dict(concept_counts),
    }


def compute_concept_trend(rows):
    seen = set()
    by_batch = {}
    for row in rows:
        by_batch.setdefault(row["batch"], []).append(row)

    trend = []
    for batch in sorted(by_batch, key=lambda b: int(b)):
        batch_rows = by_batch[batch]
        new_this_batch = 0
        for row in batch_rows:
            for concept in row["concept"].split(";"):
                concept = concept.strip()
                if concept and concept not in seen:
                    seen.add(concept)
                    new_this_batch += 1
        trend.append(
            {
                "batch": batch,
                "problems": len(batch_rows),
                "cumulative_concepts": len(seen),
                "new_concepts": new_this_batch,
            }
        )
    return trend


def compute_review_queue(rows, threshold):
    concept_counts = Counter()
    for row in rows:
        for concept in row["concept"].split(";"):
            concept = concept.strip()
            if concept:
                concept_counts[concept] += 1

    return [
        {"concept": concept, "count": count}
        for concept, count in sorted(concept_counts.items(), key=lambda kv: -kv[1])
        if count >= threshold
    ]


OUTCOME_LABELS = [
    ("WORKS", "Works"),
    ("REWRITE", "Needs rewrite"),
    ("SUGAR", "Needs sugar"),
    ("GAP", "Missing concept"),
    ("WRONG_ABSTRACTION", "Wrong abstraction"),
]


def format_report(stats):
    lines = [f"Problems tested: {stats['total']}", ""]

    for key, label in OUTCOME_LABELS:
        lines.append(f"{label}: {stats['outcome_counts'].get(key, 0)}")

    lines.append("")
    lines.append("Language coverage:")
    for category, pct in sorted(stats["category_coverage"].items()):
        lines.append(f"  {category:.<20} {pct}%")

    lines.append("")
    lines.append("Concept frequency:")
    for concept, count in sorted(stats["concept_counts"].items(), key=lambda kv: -kv[1]):
        lines.append(f"  {concept:.<20} {count}")

    return "\n".join(lines)
