# Candidate: final scalar assertion (newly separated from the filter candidate)

**Status:** Under investigation, but likely NOT a grammar question at all.

**Why is this being considered?**
Contains Duplicate is almost entirely expressible today
(`GROUP...COUNT...ORDER DESC...TAKE 1`) — the only remaining gap is
interpreting the final scalar result ("is that one count greater than 1?").

**Problems requiring it:** 004 (Contains Duplicate) only.

**Why this is separate from `sequence-filter-with-fallback.md`:** the first
pass of this atlas conflated 003 and 004 as the same "needs WHERE" gap. They
are not the same shape — 003 needs to filter an entire sequence and provide a
fallback; 004 only needs to compare one already-computed scalar to a
threshold. Keeping them apart is the whole point of this atlas.

**Leading hypothesis:** this may not need any new language primitive at all —
it may be a question of how a pipeline's final result is interpreted/returned
(a compiler or runtime concern), not something the grammar needs to express.

**Future work:** Watch for more problems that need a final boolean/scalar
check on an otherwise-complete pipeline before concluding either way.
