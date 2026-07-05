# Candidate: graph / grid traversal (naming undecided — NOT "EXPLORE")

**Status:** Under investigation. Two confirmed data points.

**Why is this being considered?**
GROUP/COUNT/ORDER/TAKE have no notion of adjacency or connectivity at all —
they operate on flat collections, never a structure where elements relate to
neighbors.

**Problems requiring it:** 015 (Number of Islands — grid adjacency), 016
(Course Schedule — directed dependency graph, plus cycle detection).

**Alternative syntaxes considered:** none yet.

**Rejected designs:** None yet.

**Future work:** Expect this count to climb fast with more graph problems.
Also worth testing whether tree traversal (a restricted, acyclic case) is the
same primitive or deserves separate treatment once tree problems are added
to the batch.
