# Rune style laws

These were not decreed up front. Each one was tested against real problems
before being written down — see the conversation history and
`docs/language/atlas/` for the evidence behind each. A law that turns out
wrong should be changed the same way it was found: by testing against real
problems, not by re-arguing from principle.

## Law 1 — Every statement begins with intent

Every statement starts with a keyword naming a concept — Grouping, Ordering,
Selection, and so on — currently spelled `GROUP`, `COUNT`, `ORDER`, `TAKE`.
The concept is the fixed thing; the spelling isn't (see the note at the
bottom of this file). Never starts with an implementation (`HashMap`,
`Heap`, `DFS`) — that's not a concept at all, spelled any way.

## Law 2 — Composition is vertical

Algorithms are pipelines, not nested expressions. Each line transforms the
previous result:

```
GROUP nums BY value
COUNT EACH group
ORDER BY count DESC
TAKE 10
```

This mirrors how humans explain algorithms on a whiteboard.

## Law 3 — Modifiers always follow

Never `DESC ORDER score`. Always `ORDER BY score DESC`. Consistency beats
brevity, and postfix modifiers compose predictably regardless of how many
appear.

## Law 4 — Implementation never appears

`HashMap`, `Heap`, `DFS`, `Priority Queue` belong to the compiler. The
language ends at intent.

## Law 5 — Sugar must earn its existence

A keyword exists only if it exposes an irreducible semantic transformation,
OR repeated testing shows the composed form is consistently worse. Proven in
practice: `FIRST UNIQUE`-style sugar would be justified (First Unique's raw
composition is genuinely clunky); `TOP_K` as a keyword would NOT be (`ORDER
BY ... DESC` + `TAKE k` already reads naturally, confirmed against real
examples, not assumed).

## Law 6 — Every keyword must remove more decisions than it introduces

`FIRST UNIQUE` removes frequency-counting, order-preservation, and
filtering, and introduces zero implementation decisions — a good keyword,
if it's ever added. A keyword that merely renames an existing composition
without removing a real decision doesn't pass this test.

## Law 7 — The language describes transformations, not objects

Good: `GROUP`, `COUNT`, `ORDER`, `WINDOW`, `MATCH`. Bad: `HashMap`,
`SegmentTree`, `PriorityQueue`. Objects belong to implementation;
transformations belong to humans.

## Law 8 — Capability before syntax

Never name a keyword before confirming the underlying concept is
genuinely missing, genuinely can't be expressed by composing existing
concepts, and genuinely isn't a compiler-side rewrite or sugar question in
disguise. Discovered the hard way: an early draft of this atlas proposed
`RETURN`/`WHERE`/`ELSE` for First Unique Character before checking whether
the *capability itself* was even correctly scoped — it wasn't (Contains
Duplicate was wrongly bundled into the same need and turned out not to
require anything new at all). See `docs/language/decisions/DECISIONS.md`
for the full account.

## Law 9 — Design for yesterday's 50 problems, never tomorrow's one

If today's problem screams for a new concept, that's a mood, not evidence. If
fifty independently-solved problems quietly ask for the same capability,
that's evidence. A candidate is evaluated against accumulated history, never
against how urgent the current problem feels. This is why
`docs/language/research/` exists — a lone, whichever-problem-is-in-front-of-you
justification does not clear this bar, no matter how clean the resulting
syntax would look.

One consequence worth stating plainly: a negative result — "this problem
doesn't need anything new, it's the same capability already tracked" — is
not a wasted day. It's the ritual working. See
`docs/language/research/2026-07-07-valid-parentheses.md` for a worked
example: the finding was "no new gap," and that was the valuable outcome,
not a consolation prize for not finding one.

## Uniformity note

Even single-shape problems stay pipelines, for consistency, rather than
switching to a different surface form based on complexity:

```
FIND target
IN sorted_numbers
```

Two lines, still a pipeline — not a special case.

## Concept vs. syntax

Internally, "concept" and "keyword" are never the same word. `GROUP`,
`ORDER`, `TAKE`, `COUNT` are today's spellings. The concepts they spell —
Grouping, Ordering, Selection, Aggregation — are the fixed thing. A concept
could legally get a different spelling later (`GROUP` → `CLUSTER`, say)
without changing what it means; a keyword by itself is not evidence of
anything. Every place in this repo that talks about "the four current
X" means four *concepts*, each with one current spelling. See
`docs/language/decisions/DECISIONS.md` for when and why this distinction was
made explicit.
