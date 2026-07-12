# Rune grammar — current (frozen)

This documents exactly what `rune/parser.py` accepts today. It is kept in
sync with the parser deliberately — if this file and the parser disagree,
the parser is the ground truth and this file is stale.

**Status: frozen, with two promotions since v0.1** (`EXPLORE`/Traversal, and
`MAXIMIZE`/`MINIMIZE`/Objective — see `docs/language/V0.1_FREEZE.md`). No
further new keywords until `docs/language/atlas/algorithm-atlas.md` produces
enough independent evidence to promote another candidate concept from
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
| Traversal | `EXPLORE <source> FROM <start> [TO <target>]` — `TO` optional; without it, returns reachability/distances from `start`, with it, returns the shortest distance to `target` (or nothing if unreachable). BFS or Dijkstra is chosen at runtime from the data, not the syntax — see `rune/runner.py`'s `_select_shortest_path_strategy`. |
| Objective | `MAXIMIZE\|MINIMIZE SUM OVER CONTIGUOUS <source>` — the best (max/min) sum over contiguous subarrays. The compiler recognizes this objective and emits Kadane's O(n) pass instead of checking all O(n²) subarrays — see the optimizer. Scope is limited to `CONTIGUOUS` on purpose; only *structural* scopes close in Rune's vocabulary (see `docs/language/decisions/DECISIONS.md`, the closed-vocabulary ceiling). |

This file documents spelling. `docs/language/philosophy/style-laws.md` (the
concept-vs-syntax note) documents why the two columns are kept separate.

## Lexical rules

- Tokens are whitespace-separated words per line.
- A closed keyword set: `GROUP, BY, COUNT, EACH, ORDER, ASC, DESC, TAKE,
  EXPLORE, FROM, TO, MAXIMIZE, MINIMIZE, SUM, OVER, CONTIGUOUS`.
- Anything not a keyword and not all-digits is an `IDENT`.
- All-digit words are `NUMBER`.

## What's deliberately NOT here

See `docs/language/primitives/candidates/` for capabilities still under
investigation (filtering with fallback, stateful scan/recurrence, windowed
views, relations between pairs, ordered lookup, final scalar assertions,
two-ended convergence — graph traversal moved out of this list when it was
promoted). None of them exist in the grammar yet — they haven't earned it.
