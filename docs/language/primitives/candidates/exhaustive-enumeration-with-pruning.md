# Candidate: exhaustive enumeration with pruning (naming undecided)

**Status:** Under investigation — newly opened 2026-07-14 to *track* pressure,
not to promote. No keyword proposed, no syntax sketched.

**Why is this being considered?**
A family of problems builds every candidate configuration (subset, permutation,
placement, partition), abandoning partial ones that cannot lead to a valid
answer. That "grow a partial solution, prune, backtrack, emit the complete
ones" mechanism has no expression in any current concept — the pipeline
transforms a collection as a whole; it does not *construct and explore* a
search tree.

**Problems requiring it:** 035 (Subsets), 036 (Permutations), 037 (N-Queens),
066 (Combination Sum), 069 (Combination Sum II), 070 (Word Search), 071
(Palindrome Partitioning), 091 (Word Search II). Eight independent data points
in `docs/language/ledger.csv`, tagged `Enumeration`.

**Why open the page now, at 8 and not 15?**
Not to act — to *track*. It was accumulating pressure while invisible to
`candidates/`, which made the count in `rune mine` easy to overlook. Tracking
it is CLAUDE.md step 2 ("if not already tracked, add a candidate page named
after the capability"); it is explicitly **not** promotion. The review
threshold (15) still governs whether this ever becomes a grammar question.

**Open sub-questions:**
- Is this one capability or several? "Enumerate subsets/permutations" (pure
  combinatorial generation) may be a different shape from "search a grid/graph
  with backtracking" (070, 091 overlap with Traversal). Splitting may be
  warranted before the count matters — the same over-aggregation trap that
  `stateful-scan-or-recurrence` fell into.
- Is it even pipeline-shaped, or is it the wrong abstraction for this whole
  category? Too early to say — that verdict needs ~20 problems in one category
  failing the same way (see `../../research/ABSTRACTION_QUESTIONS.md`), not 8.

**Alternative syntaxes considered:** none yet — deliberately.

**Rejected designs:** none yet.

**Future work:** One or two more enumeration problems to test whether the
combinatorial-generation shape and the grid-backtracking shape are the same
capability or should be split, before the count is anywhere near actionable.
