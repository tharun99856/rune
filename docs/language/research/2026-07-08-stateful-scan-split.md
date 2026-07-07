## Problem

Not a new algorithm. An investigation: split the 19 problems currently
tagged `Stateful Scan` and see whether they cluster — cheap, doesn't touch
the grammar, doesn't require resolving anything about syntax.

## Current Rune

N/A — this is analysis of existing ledger data
(`docs/language/ledger.csv`), not a new problem attempt.

## Pain points

Classified each of the 19 by *actual mechanism*, not by surface similarity:

| Problem | Mechanism |
|---|---|
| Merge Intervals | fixed-size accumulator (current interval), extend-or-replace |
| Kadane's | running scalar, reset on negative |
| Climbing Stairs | previous 2 values only |
| House Robber | previous 2 values only |
| Jump Game | running max-reach scalar, monotonic |
| Gas Station | running deficit scalar, reset on negative |
| Coin Change | table indexed by amount; each cell depends on arbitrarily-far-back cells (any coin denomination) |
| Word Break | table indexed by position; each cell depends on arbitrarily-far-back cells (any valid split point) |
| Longest Increasing Subsequence | table indexed by position; each cell depends on all smaller earlier values |
| LCS | 2D table; each cell depends only on the row directly above |
| Edit Distance | 2D table; each cell depends only on the row directly above |
| Unique Paths | 2D table; each cell depends only on the row directly above |
| Valid Parentheses | LIFO stack, push/pop |
| Evaluate RPN | LIFO stack, push/pop |
| Daily Temperatures | LIFO stack (monotonic), push/pop |
| Reverse Linked List | fixed pointers (prev/current/next), rewiring references |
| Merge Two Sorted Lists | fixed pointers into two lists, building a third |
| Add Two Numbers | rolling scalar (carry) **and** dual-list pointer traversal at once |
| Validate BST | (min,max) bounds propagated through *tree recursion*, not a linear scan at all |

## Candidate capabilities

**First correction, before clustering: problem 020 (Validate BST) is
probably mistagged.** It isn't a left-to-right scan carrying state at all —
it's bounds propagated down through tree recursion. That's the Traversal
concept, not Stateful Scan. Removing it from this cluster (ledger updated;
still tagged Traversal, which it already was tagged as jointly).

**With 020 removed, the remaining 18 split into three mechanisms, not four:**

1. **Recurrence over an index space** (13 problems: Merge Intervals,
   Kadane's, Climbing Stairs, House Robber, Jump Game, Gas Station, Coin
   Change, Word Break, LIS, LCS, Edit Distance, Unique Paths) — a value
   computed at each index/position from previously-computed values.
2. **Stack** (3: Valid Parentheses, Evaluate RPN, Daily Temperatures) — LIFO
   push/pop, not an indexed recurrence at all.
3. **Pointer/relinking** (2: Reverse Linked List, Merge Two Sorted Lists) —
   operates on a linked structure, rewires references rather than computing
   a value.

**Add Two Numbers genuinely spans two of these** (a rolling carry *and*
dual-pointer list traversal) — real evidence these three mechanisms compose
with each other rather than being mutually exclusive alternatives.

**The sharper finding, one level deeper, inside cluster 1:** "rolling state"
(Kadane's-style) isn't a different mechanism from "full table" (Coin-Change-
style) — it's a *space optimization* of the same mechanism, and whether it
applies is a property of the recurrence, not a property of the problem
category:

- **Bounded lookback** — the recurrence only ever needs a fixed, statically
  determinable window of prior values (Kadane's/Climbing-Stairs/House-Robber/
  Jump-Game/Gas-Station need only the immediately preceding value(s);
  LCS/Edit-Distance/Unique-Paths need only the previous row). These are
  compilable to O(1) or O(row-width) space instead of the full table — the
  same kind of space-optimizing rewrite this project already has one
  example of (`ORDER DESC + TAKE k → TOP_K`, heap instead of full sort).
- **Unbounded lookback** — the recurrence can reference *any* earlier value,
  not a fixed window (Coin Change references `dp[amount - coin]` for
  arbitrary coin sizes; Word Break references `dp[j]` for any earlier valid
  split point). These genuinely need the full table; no space-optimizing
  rewrite exists.

If this holds, "Rolling" and "DP table" were never two different concepts —
one compiler-decidable property (does the recurrence have bounded or
unbounded lookback?) determines which physical representation a single
`Recurrence` concept compiles to. That would mean the honest cluster count
is **3, not 4**: Recurrence (with an internal bounded/unbounded
space-optimization question, resolved by the compiler, not the language),
Stack, and Pointer.

## Rejected capabilities

Did not accept "4 concepts" (Rolling / Stack / DP / Pointer) as the final
answer, even though it was the first split found and matched the sketch
this investigation started from — the deeper mechanism-level look showed
Rolling and DP-table are the same computation with a compiler-decidable
space difference, not two different things a human should have to think
about when writing the algorithm.

## Decision

No grammar change — this is investigation, not promotion, exactly as
framed. Corrected the ledger (020 moved to Traversal-only). Updated
`docs/language/primitives/candidates/stateful-scan-or-recurrence.md` with
the 3-cluster finding. Did not build a "needs split: YES/NO" automated tool
yet — the judgment call above (is a lookback bounded or unbounded?) required
reading each recurrence, not something mechanically derivable from the
ledger's current columns. Building a tool to fake that determination with an
invented confidence score would be less honest than doing it by hand once
and writing down how.

## Outcome

🧩 — sharpened, not resolved. The candidate concept survives, but reframed:
likely `Recurrence` (bounded/unbounded lookback as an internal, compiler-
decided property) + `Stack` + `Pointer`, not one undifferentiated `Stateful
Scan`. Still a naming and promotion decision outside this session's
authority — this entry narrows *what* would be promoted, not *whether*.

## Next experiment

Before treating "3 clusters" as settled: find a problem that isolates Stack
from Recurrence and Pointer independently (e.g. a monotonic-stack DP hybrid,
if one exists) to check the clusters don't secretly overlap the way Add Two
Numbers did for Recurrence/Pointer.
