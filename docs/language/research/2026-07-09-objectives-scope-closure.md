## Problem

Investigate whether `objective-over-scope` (surfaced when Stateful Scan
dissolved) can be a *closed* Rune concept, or whether it needs arbitrary
predicates and dies the same way. Method: sweep all 100 ledger problems for
objective-shaped intent (max / min / count / exists over a space), then split
them by **scope type** — can the space be defined structurally, or only by an
arbitrary constraint predicate? This is a one-pass hand classification;
counts are approximate and judgment-heavy, stated as ~N, not N.

## The finding: objectives bifurcate by scope, and it's the split that matters

**Objective over a STRUCTURAL scope (closeable — space is a definable shape):**

| Problem | Objective | Scope |
|---|---|---|
| Max Subarray (Kadane's) | maximize sum | contiguous subarrays |
| Max Product Subarray | maximize product | contiguous subarrays |
| Container With Most Water | maximize area | pairs of positions |
| Max Product of Three | maximize product | triples |
| Sliding Window Maximum | maximize per window | fixed windows |
| Top K Frequent / Kth Largest / Kth Smallest | select by rank | ranked order |
| Max Depth / Diameter of Tree | maximize path length | tree paths |

~10 problems. The scope ("contiguous subarrays", "pairs", "windows", "rank",
"root-to-leaf paths") is a structural shape — nameable in closed vocabulary,
no arbitrary predicate needed. Several (the rank ones) are already nearly
`ORDER`+`TAKE`.

**Objective over a PREDICATE-defined scope (NOT closeable — space is defined
by an arbitrary constraint):**

| Problem | Objective | Scope constraint (the predicate) |
|---|---|---|
| Coin Change | minimize count | subsets *summing to target* |
| Partition Equal Subset | exists | subsets *summing to half* |
| Longest Increasing Subsequence | maximize length | subsequences that are *increasing* |
| Longest Common Subsequence | maximize length | subsequences *common to both strings* |
| Edit Distance | minimize edits | edit sequences *transforming A into B* |
| Word Break | exists | segmentations *into dictionary words* |
| Longest Palindromic Substring | maximize length | substrings that are *palindromes* |
| Longest Substring w/o Repeating | maximize length | substrings with *no repeat* |
| Longest Repeating Char Replacement | maximize length | substrings *≤ k replacements from uniform* |
| Minimum Window Substring | minimize length | windows *containing all target chars* |
| House Robber | maximize sum | subsets with *no two adjacent* |
| Decode Ways | count | segmentations that are *valid decodings* |

~12–14 problems. Each scope is defined by a *predicate over candidates*
("sums to X", "is increasing", "is a palindrome", "in the dictionary"). To
express these, Rune would need either a general predicate sublanguage (an
arbitrary-boolean escape hatch — the exact closed-vocabulary violation that
just dissolved Stateful Scan) or one bespoke keyword per constraint type
(the stdlib-zoo failure the whole project is built to avoid). Neither is
acceptable.

## What this means (and it's bigger than "which concept next")

**The predicate-scoped objectives outnumber the structural ones.** So a
closed objective concept would capture the *minority* — and the classic DP
problems that made "objectives" look exciting (Coin Change, LIS, Edit
Distance, Word Break, Partition) fall on the wrong side of the line.

That is a real finding about the **ceiling of the closed-vocabulary bet**,
not just a candidate's fate: there appears to be a whole class of algorithmic
problems — *optimization over a predicate-defined space*, i.e. much of classic
DP — that Rune's founding constraint may fundamentally not be able to express,
because naming the space requires arbitrary predicates. This isn't fatal
(Rune still cleanly covers grouping, ordering, selection, traversal, and
structural-scope objectives), but it honestly bounds the ambition. "Solve
Striver's sheet in Rune" is not reachable for the DP-heavy portion without
abandoning the property that makes Rune's optimizer able to reason at all.
Better to know and write down now than discover it as a wall later.

## Decision

- No promotion (investigation only, no grammar touched).
- `objective-over-scope.md` split into two: a **viable narrow** candidate
  (objective over a *structural* scope) and an **out-of-reach** note
  (objective over a *predicate* scope — the closed-vocabulary ceiling).
- Ledger left unretagged (same reasoning as the Stateful Scan dissolution:
  intent re-tagging is premature before the objective vocabulary exists).

## Outcome

🧩 partial, and honestly deflating: objectives are real but the *closeable*
slice is narrow (~10, several already near-`ORDER`+`TAKE`), while the
motivating DP slice (~12–14) hits the closed-vocabulary wall. The most
important output isn't a new concept — it's the first concrete evidence of
where Rune's closed-vocabulary design *ceilings out*.

## Next experiment / open question for a real decision

If a narrow "objective over a structural scope" concept were promoted, its
payoff would be one genuinely new optimizer proof: naive all-subarrays O(n²)
vs. Kadane O(n), the compiler recognizing "maximize sum over contiguous
subarrays" and picking the linear scan. That is a strong, DP-flavored third
proof — and it needs no predicate escape hatch, because the scope
("contiguous subarrays") is structural. Whether that one proof is worth a
new keyword is a promotion decision, and it stays the human's call.
