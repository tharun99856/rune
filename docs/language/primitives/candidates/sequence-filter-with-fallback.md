# Candidate: sequence filter + fallback (naming undecided — NOT "WHERE")

**Status:** Under investigation. One confirmed data point.

**Why is this being considered?**
Problem 003 (First Unique Character) cannot be expressed with GROUP/COUNT/
ORDER/TAKE, even with clever sort-key tricks, because nothing can restrict a
sequence to elements matching a condition, and nothing expresses "return a
default value if nothing matches."

**Problems requiring it:** 003 only, so far. Explicitly *not* 004 (Contains
Duplicate) — that was an error in the first pass of this atlas, corrected
after re-examination; 004 is already expressible today.

**Open sub-question:** is this one primitive (filter-then-take-with-default)
or two separable ones (a general filter, and a separate take-or-else)? Don't
decide yet — one data point is not enough.

**Alternative syntaxes considered:** none yet — deliberately not drafting
syntax before the capability itself is confirmed by more than one problem.

**Rejected designs:** None yet.

**Future work:** Needs at least 2–3 more independent problems requiring the
same shape before any grammar change is justified.
