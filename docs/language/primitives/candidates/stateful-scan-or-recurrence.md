# Candidate: stateful scan / recurrence — DISSOLVED (not a Rune concept)

**Status: DISSOLVED, 2026-07-09.** Not promotable — not as one concept, not
as three. See `docs/language/research/2026-07-09-stateful-scan-dissolved.md`
for the full argument; the short version:

- Re-classified by **intent** (not mechanism, as the earlier splits did), the
  34 tagged problems scatter across ≥8 unrelated intent families (optimize,
  count, restructure-list, consolidate-intervals, evaluate-expression,
  next-greater-relation, reachability, per-element-transform).
- A single `SCAN`/`FOLD` concept covering all of them would need an arbitrary
  user-supplied step function (`scanl :: (b -> a -> b) -> ...`) — the one
  thing Rune's founding closed-vocabulary rule forbids. So it can't be one
  concept without breaking the thesis.
- As many concepts, its members already belong to other concepts (Jump Game's
  intent is reachability = `EXPLORE`) or to a concept that doesn't exist yet
  (objectives — now tracked as `objective-over-scope.md`).

"Stateful Scan" was an *implementation shape* — "a pass that maintains state,"
which Python expresses uniformly with `for` + a mutable variable — masquerading
as an intent. The 34 count was pattern-frequency, never 34 votes for one
concept. This is the productive negative result the intent-over-implementation
thesis predicts, caught before it became a keyword.

---

Everything below is the earlier (superseded) mechanism-level analysis, kept
for the record — it's how the dissolution was reached, not a live proposal.

**Superseded finding — three mechanisms:**

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
