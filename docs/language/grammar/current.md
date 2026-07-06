# Rune grammar — current (frozen)

This documents exactly what `rune/parser.py` accepts today. It is kept in
sync with the parser deliberately — if this file and the parser disagree,
the parser is the ground truth and this file is stale.

**Status: frozen.** No new verbs until `docs/language/atlas/algorithm-atlas.md`
produces enough independent evidence to promote a candidate from
`docs/language/primitives/candidates/`.

## Program structure

A Rune program is a sequence of lines, each one pipeline step. Steps compose
vertically — each line transforms the result of the previous one. No braces,
no semicolons, no nested expressions.

## Verbs

```
GROUP <source> BY <key>
COUNT EACH <noun>
ORDER BY <key> [ASC|DESC]        -- defaults to ASC if omitted
TAKE <count>
```

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
