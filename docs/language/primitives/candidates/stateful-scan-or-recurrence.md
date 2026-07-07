# Candidate: stateful scan / recurrence (naming undecided — NOT "SCAN")

**Status:** Under investigation. Leading candidate by raw count (19, after
the 2026-07-08 batch — was 7), a 2.7x lead over the next candidate
(Traversal). Raw count now plausibly clears "yesterday's 50 problems," but
promotion should wait on the open sub-question below, not on count alone —
see `docs/language/research/2026-07-08-batch-002.md`.

**Why is this being considered?**
A running left-to-right pass carrying forward accumulated state (a sum that
can reset, a rolling count, a growing table, a stack, pointer relinking)
shows up across DP, interval-merging, stack-matching, and linked-list
problems, none of which are expressible with GROUP/COUNT/ORDER/TAKE.

**Problems requiring it:** 19 total — see `docs/language/ledger.csv` for the
full list (id column, concept = "Stateful Scan"). Includes DP problems with
O(1) rolling state (Kadane's, Climbing Stairs, House Robber), full-table DP
(Coin Change, LCS, Word Break, Unique Paths, Edit Distance), stack-based
(Valid Parentheses, Evaluate RPN, Daily Temperatures), linked-list (Reverse
List, Merge Two Sorted Lists, Add Two Numbers), and greedy running-state
(Jump Game, Gas Station).

**Open sub-question — do not merge prematurely:** at least three distinct
state shapes now hide behind this one name: O(1) rolling state (Kadane's,
Climbing Stairs), a full table (Coin Change, LCS), and now a stack (Valid
Parentheses) — plus Reverse-List operating over a pointer-linked
representation rather than an array. Valid Parentheses didn't resolve this
question, it sharpened it: a third state shape is independent evidence
*against* treating this as one primitive, not for it.
**This is the single biggest risk of over-conclusion in the current atlas** —
resolve it with more problems, specifically ones that stress each sub-case
independently, before committing to one primitive.

**Alternative syntaxes considered:** none yet.

**Rejected designs:** None yet.

**Future work:** Run problems that isolate each sub-case (pure O(1)-state
scans vs. full-table recurrences vs. non-array representations) before
deciding whether this is one primitive or several.
