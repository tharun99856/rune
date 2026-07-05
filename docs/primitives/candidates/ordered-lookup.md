# Candidate: ordered lookup by value (naming undecided — NOT "FIND")

**Status:** Under investigation. One data point, but structurally the
cleanest/most atomic candidate found so far.

**Why is this being considered?**
Binary Search needs to locate a specific target value's position within a
sorted collection — this is not a group, not an aggregation, not a rank
selection; none of the current verbs come close.

**Problems requiring it:** 011 (Binary Search) only.

**Alternative syntaxes considered:** none yet.

**Rejected designs:** None yet.

**Notes:** Unlike the stateful-scan candidate, this one shows no sign of
being an over-merged bucket — it doesn't decompose further and nothing else
tested so far resembles it. Still only one data point, though; needs more
before promotion.

**Future work:** Test against other search-shaped problems (e.g. search in
rotated sorted array, find peak element) to see if the same shape holds or
needs a variant.
