# Abstraction questions

Tracks ❌ "wrong abstraction" findings — the rarest and most consequential
outcome a research journal entry can reach. Different in kind from the other
four outcomes: those ask "does Rune have the right *keyword*." This asks
"does Rune have the right *model*" for an entire category of problem.

**No findings yet.** This file exists so there's a real home for one the
moment evidence crosses the threshold — not so one gets declared early to
have something to put here.

## What would actually count as evidence

A single problem never triggers this. The threshold, by example (the one
given directly): if, after ~20 problems in one category, every single one
fights the vertical-pipeline model — not "needs one more concept," but the
concept-per-line, each-line-transforms-the-last shape itself doesn't fit how
the category's algorithms are structured — that's the language's model being
wrong for that category, not a missing word in it.

## Category currently closest to worth watching

**Graph / grid traversal**
(`docs/language/primitives/candidates/graph-traversal.md`). Reasoning, laid
out honestly rather than concluded: traversal is a frontier-expansion
process, not an up-front "transform the whole collection" step, which is
what every current concept does. It's an open question whether that's just a
new *concept* (`EXPLORE` still fits the pipeline shape fine as a single step —
"traverse, then hand the result to the next line") or whether real graph
algorithms need control flow (conditional branching mid-traversal, revisits,
early termination) that resists being expressed as one line at all.

**Current evidence: 2 problems** (Number of Islands, Course Schedule), both
still tagged 🧩 in the atlas, not ❌ — nowhere near the threshold. This is
explicitly the next thing to watch as more graph problems accumulate in the
research journal, not something to decide now.
