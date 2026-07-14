## Problem

Sort Characters by Frequency (LeetCode 451). Given a string, order its
characters from most frequent to least.

**Solved in English first, no Rune in mind:**

> Count how many times each character appears. Then list the characters from
> the most frequent down to the least.

## Current Rune

A plausible attempt exists, and it is not a near-miss — it is the canonical
frequency pipeline:

```
GROUP text BY value
COUNT EACH char
ORDER BY count DESC
```

`[verified]` — parses through `rune.parser.parse_program`, and actually runs
through `run_program`: `list("mississippi")` → `i:4, s:4, p:2, m:1`, and
`list("tree")` → `e:2, r:1, t:1` (ties broken by ascending character, matching
the numeric-key convention). This is #001 Top K Frequent Elements with the
final `TAKE` dropped.

## Pain points

None at the grammar level. This is the third fully-expressible frequency
problem (with #001 and #004); the pipeline says exactly what the English says.

The only friction was **not linguistic**: exercising the program end-to-end
surfaced a runtime bug in the interpreter's descending tiebreak. It computed
the secondary sort key as `-_tiebreak(item)`, which assumes the tiebreak is a
number that can be negated; a character key is a string, so `ORDER BY ... DESC`
crashed with `TypeError: bad operand type for unary -: 'str'`. The canonical
example only ever ran on integer data, so the bug had never been hit. Fixed in
`rune/runner.py` with a stable two-stage sort (and a comparison-inverting
wrapper so `TopK`'s heap keeps working), with regression tests in
`tests/test_runner.py`. An implementation defect the problem exposed, not a
capability the grammar lacks.

## Candidate capabilities

**No new gap, and no new evidence for an existing candidate either.** This
confirms reach that is already closed: Grouping + Aggregation + Ordering. It is
the discipline working — a problem that looks like it might want something new
(string output, character handling) and, examined honestly, wants nothing the
grammar doesn't already have.

## Rejected capabilities

Considered whether "rebuild the answer as a string with each character repeated
`count` times" demands a new rendering/output primitive. Rejected: that is
presentation/serialization, the same boundary #001 draws when it returns ranked
buckets rather than a reconstructed structure. Drawing that line is a decision
(see `docs/language/decisions/DECISIONS.md`), not a missing feature.

## Decision

No grammar change. Added `docs/language/examples/strings/sort-characters-by-frequency.rn`
(kept parsing green by `tests/test_examples.py`), atlas entry #018, and fixed
the descending-tiebreak runtime bug this problem exposed.

## Outcome

✅ Already expressible.

## Next experiment

Unchanged from 2026-07-07: the still-open lead is a second stack-shaped problem
(Daily Temperatures or Largest Rectangle in Histogram) to test whether "stack
state" recurs independently — the evidence the `stateful-scan-or-recurrence`
over-aggregation question actually needs. This entry deliberately does not touch
that; it only confirms existing reach.
