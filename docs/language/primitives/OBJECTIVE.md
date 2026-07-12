# OBJECTIVE (`MAXIMIZE` / `MINIMIZE`)

**Status:** Established. Promoted 2026-07-09 from the `objective-over-scope`
candidate — but only the *structural-scope* half, and within that, only the
`CONTIGUOUS` scope. The predicate-scope half stays out of reach (the
closed-vocabulary ceiling; see below).

**Why does this exist?**
A large class of problems states an *objective over a space* — the best
(max/min) value of some measure. `ORDER`+`TAKE` gets "top-k by a key," but not
"the maximum sum over all contiguous subarrays," where the space is
combinatorial (every subarray), not just the input list. This is the first
concept whose result is a computed optimum, not a reshaped collection.

**Current grammar:** `MAXIMIZE|MINIMIZE SUM OVER CONTIGUOUS <source>`
— returns the best (max or min) sum over all contiguous subarrays of a list of
numbers. All-negative input returns the largest single element (like the
classic problem); empty input returns nothing.

**The proof it carries (why it earned promotion, not just usefulness):** the
compiler recognizes the objective's *optimal substructure* — the best subarray
ending at each position either starts fresh or extends the best one ending
just before it — and emits **Kadane's O(n) single pass** instead of the naive
O(n²) "check every subarray." Third distinct optimizer decision in Rune, and
the first DP-flavored one. Live at n=4000: naive ~845 ms → Kadane ~0.78 ms,
~1090x, identical result. See `rune/optimizer.py`
(`OBJECTIVE_CONTIGUOUS_TO_KADANE`) and `tests/test_objective_end_to_end.py`
(200 random arrays where naive and Kadane must agree).

**Deliberately narrow — and this is the important part.** The scope is only
`CONTIGUOUS`. That's not laziness; it's the closed-vocabulary boundary.
Structural scopes (contiguous subarrays, pairs, windows, rank) can be named in
Rune's vocabulary. Predicate-defined scopes (subsets *summing to X*,
*increasing* subsequences, *palindromic* substrings, *dictionary*
segmentations — i.e. much of classic DP) cannot, without an arbitrary
predicate escape hatch that would break the property letting the optimizer
reason at all. See the "closed-vocabulary ceiling" entry in
`docs/language/decisions/DECISIONS.md`. `MAXIMIZE`/`MINIMIZE` is the closeable
slice, honestly bounded.

**Rejected designs:** naming it "DP" or "MEMOIZE" — that's the technique the
compiler picks, not the intent (same category error as naming a graph concept
"Dijkstra").

**Future work:** other *structural* scopes are legitimate extensions when
evidence warrants — `OVER PAIRS` (Container With Most Water, Max Product of
Three), `OVER WINDOWS` (overlaps the windowed-view candidate). Each is a
separate promotion decision. Predicate scopes are not future work — they're
the documented ceiling.
