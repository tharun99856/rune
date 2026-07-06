# Candidate: stateful scan / recurrence (naming undecided — NOT "SCAN")

**Status:** Under investigation. Leading candidate by raw count (6), but the
count itself may be over-aggregated — see the open sub-question below.

**Why is this being considered?**
A running left-to-right pass carrying forward accumulated state (a sum that
can reset, a rolling count, a growing table, pointer relinking) shows up
across DP, interval-merging, and linked-list problems, none of which are
expressible with GROUP/COUNT/ORDER/TAKE.

**Problems requiring it:** 005 (Merge Intervals), 006 (Kadane's), 007
(Climbing Stairs), 008 (Coin Change), 009 (LCS), 010 (Reverse Linked List).

**Open sub-question — do not merge prematurely:** Kadane's and Climbing
Stairs only need O(1) trailing state; Coin Change and LCS need a full state
table; Reverse-List operates over a pointer-linked representation, not an
array. These may be one primitive with different state-retention needs, or
genuinely distinct primitives that happen to look similar from a distance.
**This is the single biggest risk of over-conclusion in the current atlas** —
resolve it with more problems, specifically ones that stress each sub-case
independently, before committing to one primitive.

**Alternative syntaxes considered:** none yet.

**Rejected designs:** None yet.

**Future work:** Run problems that isolate each sub-case (pure O(1)-state
scans vs. full-table recurrences vs. non-array representations) before
deciding whether this is one primitive or several.
