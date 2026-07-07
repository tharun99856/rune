# Rune grammar — current (frozen)

This documents exactly what `rune/parser.py` accepts today. It is kept in
sync with the parser deliberately — if this file and the parser disagree,
the parser is the ground truth and this file is stale.

**Status: frozen.** No new keywords until `docs/language/atlas/algorithm-atlas.md`
produces enough independent evidence to promote a candidate concept from
`docs/language/primitives/candidates/`.

## Program structure

A Rune program is a sequence of lines, each one pipeline step. Steps compose
vertically — each line transforms the result of the previous one. No braces,
no semicolons, no nested expressions.

## Keywords (today's spelling of each concept)

| Concept | Keyword |
|---|---|
| Grouping | `GROUP <source> BY <key>` |
| Aggregation | `COUNT EACH <noun>` |
| Ordering | `ORDER BY <key> [ASC\|DESC]` — defaults to ASC if omitted |
| Selection | `TAKE <count>` |

This file documents spelling. `docs/language/philosophy/style-laws.md` (the
concept-vs-syntax note) documents why the two columns are kept separate.

## Lexical rules

- Tokens are whitespace-separated words per line.
- A closed keyword set: `GROUP, BY, COUNT, EACH, ORDER, ASC, DESC, TAKE`.
- Anything not a keyword and not all-digits is an `IDENT`.
- All-digit words are `NUMBER`.

## What's deliberately NOT here

See `docs/language/primitives/candidates/` for capabilities under
investigation (filtering with fallback, stateful scan/recurrence, windowed
views, graph traversal, relations between pairs, ordered lookup, final
scalar assertions, two-ended convergence). None of them exist in the grammar
yet — they haven't earned it.
