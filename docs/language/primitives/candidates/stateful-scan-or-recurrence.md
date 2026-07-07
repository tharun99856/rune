# Candidate: stateful scan / recurrence (naming undecided — NOT "SCAN")

**Status:** Under investigation, and just split. Raw count 18 (was 19 — one
problem, Validate BST, was mistagged; it's tree-recursion bounds propagation,
not a linear scan, moved to Traversal). Investigated directly (cheap, no
grammar touched) — see `docs/language/research/2026-07-08-stateful-scan-split.md`
for the full mechanism-by-mechanism breakdown. Result: **three mechanisms,
not one, and not four either:**

1. **Recurrence over an index space** (13 problems) — a value computed at
   each position from previously-computed values. Internally has a
   compiler-decidable property, not a language-level distinction: *bounded
   lookback* (Kadane's-style — needs only a fixed window of prior values,
   compilable to O(1)/O(row) space) vs. *unbounded lookback* (Coin-Change-
   style — needs the full table, no space optimization applies). "Rolling
   state" and "full DP table" are the same concept at different lookback
   widths, not two concepts — the same shape of optimization this project
   already has one example of (`ORDER DESC + TAKE k → TOP_K`).
2. **Stack** (3 problems) — LIFO push/pop, not an indexed recurrence at all.
3. **Pointer/relinking** (2 problems) — operates on a linked structure,
   rewires references rather than computing a value. One problem (Add Two
   Numbers) genuinely spans this and Recurrence at once (a rolling carry
   *plus* dual-pointer traversal) — real evidence these compose rather than
   being mutually exclusive.

**Why is this being considered?**
A running left-to-right pass carrying forward accumulated state (a sum that
can reset, a rolling count, a growing table, a stack, pointer relinking)
shows up across DP, interval-merging, stack-matching, and linked-list
problems, none of which are expressible with GROUP/COUNT/ORDER/TAKE.

**Problems requiring it:** see `docs/language/ledger.csv` (concept =
"Stateful Scan"). Full mechanism-by-mechanism list in the split entry above.

**Remaining open question:** whether Recurrence, Stack, and Pointer become
three separate concepts, or one concept with a state-shape property — same
open question `windowed-view.md` already has for fixed-vs-variable windows.
Not resolved here on purpose. Also unresolved: whether the clusters
genuinely don't overlap beyond the one known case (Add Two Numbers) — next
experiment is to find a problem that stress-tests Stack against the other
two directly.

**Alternative syntaxes considered:** none yet — still capability-before-syntax.

**Rejected designs:** "4 concepts" (Rolling / Stack / DP-table / Pointer),
the first split found — rejected after the bounded/unbounded-lookback
argument showed Rolling and DP-table are the same mechanism at different
space costs, not different mechanisms.

**Future work:** The stress-test problem above, then a promotion decision —
which stays outside this session's authority regardless of how the evidence
looks.
