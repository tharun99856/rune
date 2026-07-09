# Candidate: objective over a scope (naming undecided — NOT "MAXIMIZE"/"DP")

**Status (updated 2026-07-09, after the whole-ledger scope-closure sweep —
`docs/language/research/2026-07-09-objectives-scope-closure.md`):** SPLIT.
Objectives do not close uniformly. The concept bifurcates by *scope type*,
and only one half is a viable Rune concept:

- **Objective over a STRUCTURAL scope** (~10 problems: max sum over contiguous
  subarrays, max area over pairs, max over windows, select by rank, max tree
  path). Scope is a nameable shape, no predicate needed → **viable, narrow
  candidate.** Payoff: one strong new optimizer proof (Kadane O(n) vs naive
  all-subarrays O(n²)). Several rank cases already near-`ORDER`+`TAKE`.
- **Objective over a PREDICATE-defined scope** (~12–14 problems: Coin Change,
  LIS, LCS, Edit Distance, Word Break, Partition, palindrome/no-repeat
  substrings, House Robber). Scope needs an arbitrary constraint predicate
  ("sums to X", "is increasing", "is a palindrome", "in the dictionary") →
  **out of reach.** Expressing it needs the arbitrary-predicate escape hatch
  the closed-vocabulary rule forbids (or one keyword per constraint = stdlib
  zoo). This is the closed-vocabulary ceiling, not a candidate to pursue.

The rest of this doc is the pre-sweep framing, kept for the record.

---

**Why is this being considered?**
A large share of problems state an **objective over a defined space**: return
the max / min / count / existence of some quantity, subject to constraints.
No current concept expresses an objective — `ORDER`+`TAKE` gets "top k by a
key," but not "the maximum sum *over all contiguous subarrays*" or "the
minimum number of coins summing to a target." The space being optimized over
is combinatorial (subarrays, subsequences, partitions, paths), not just the
input list.

**Problems pointing at it (floor: 15, from the Stateful Scan set alone):**
- MAXIMIZE: Kadane's, Max Product Subarray, House Robber, LIS, LCS, Longest
  Palindromic Substring, Largest Rectangle
- MINIMIZE: Coin Change, Edit Distance, Min Cost Climbing Stairs,
  Non-overlapping Intervals (min removals)
- COUNT / EXISTS: Climbing Stairs, Unique Paths, Decode Ways, Partition Equal
  Subset, Word Break

Almost certainly more exist elsewhere in the ledger (this list is only the
problems that happened to be tagged Stateful Scan). The next experiment is to
sweep the whole ledger for objective-shaped intents.

**The key design bet (unproven):** an objective concept would name *what* to
optimize and *over what scope* — e.g. `MINIMIZE coins WHERE sum == target` —
and leave *how* (dynamic programming, greedy, brute force) to the compiler,
exactly parallel to `ORDER+TAKE → TOP_K/heap`. DP would be an implementation
strategy the optimizer selects, not a language concept. Whether the "scope"
(contiguous subarrays vs. subsequences vs. partitions vs. paths) can be
expressed in a closed, non-arbitrary way is the open risk — get that wrong
and it needs arbitrary predicates, which reintroduces the closed-vocabulary
problem that just dissolved Stateful Scan.

**Alternative syntaxes considered:** none yet — capability-before-syntax.

**Rejected designs:** naming it "DP" or "MEMOIZE" — that's the technique, not
the intent, the same category error as naming a graph concept "Dijkstra."

**Future work:** whole-ledger sweep for objective-shaped intents, then
whether the scope can be closed-vocabulary. Only after that, a promotion
decision — which stays outside a working session's authority.
