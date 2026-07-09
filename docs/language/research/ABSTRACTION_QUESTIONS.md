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

## Resolved (partially): Graph / grid traversal

Was the closest-watched category here; downgraded from "watching" because
promotion produced real evidence, not just more problem count. `EXPLORE`
(`docs/language/primitives/EXPLORE.md`) was implemented as a single pipeline
step — reachability and shortest-path-to-target both fit "traverse, then
hand the result to the next line" without needing any control-flow escape
hatch. That's a real, positive answer to the "does it fit as one line"
half of the original open question.

**Still open, and now sharper:** only reachability/shortest-path was tested.
Whether *other* graph algorithms need mid-traversal branching, revisits, or
early termination that resists one-line expression is untested, not
answered. The category isn't fully cleared — it's downgraded from "closest
to a ❌ finding" to "the ✅/🧩 half is settled, the harder cases are
unexplored," which is a different and more precise state than either
"resolved" or "still watching for a wrong-abstraction verdict."

## Other categories opened, both far earlier stage

**Enumeration / Backtracking** (Subsets, Permutations, N-Queens — 3
problems). Different concern than graph traversal: backtracking explores a
decision tree the algorithm itself constructs (choose, recurse, undo), which
doesn't obviously fit "one line transforms the previous line's result" at
all — not even as a single atomic step the way `EXPLORE` might for graphs.
3 problems is far too few to say anything; noted so it's tracked from the
start rather than rediscovered later. See
`docs/language/research/2026-07-08-batch-002.md`.

**Streaming / online algorithms** (Find Median from Data Stream — 1
problem) and **ADT definition** (Implement Trie, Min Stack — 2 problems).
Grouped together because both share the same root tension, distinct from
backtracking: every current concept assumes a complete input available up
front. A streaming algorithm never has one; an ADT-definition problem isn't
processing a collection at all, it's specifying a stateful object's
operations. 1–2 problems each — nowhere near evidence, but plausibly not
even the same *kind* of question as the other two categories here (these
may turn out to be `docs/language/ANTI_GOALS.md` material — permanently out
of scope — rather than a model that needs fixing). Left open rather than
guessed at.
