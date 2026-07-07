# Candidate: stateful scan / recurrence (naming undecided — NOT "SCAN")

**Status:** Under investigation. Leading candidate by raw count (7), but the
count itself may be over-aggregated — see the open sub-question below, now
sharper than before.

**Why is this being considered?**
A running left-to-right pass carrying forward accumulated state (a sum that
can reset, a rolling count, a growing table, a stack, pointer relinking)
shows up across DP, interval-merging, stack-matching, and linked-list
problems, none of which are expressible with GROUP/COUNT/ORDER/TAKE.

**Problems requiring it:** 005 (Merge Intervals), 006 (Kadane's), 007
(Climbing Stairs), 008 (Coin Change), 009 (LCS), 010 (Reverse Linked List),
and Valid Parentheses (`docs/language/research/2026-07-07-valid-parentheses.md`).

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
