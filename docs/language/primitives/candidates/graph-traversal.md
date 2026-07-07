# Candidate: graph / tree / grid traversal (naming undecided — NOT "EXPLORE")

**Status:** Under investigation. 11 data points (after the 2026-07-08 batch
— was 2). Second-leading candidate after Stateful Scan.

**Why is this being considered?**
GROUP/COUNT/ORDER/TAKE have no notion of adjacency or connectivity at all —
they operate on flat collections, never a structure where elements relate to
neighbors.

**Problems requiring it:** graphs (Number of Islands, Course Schedule, Clone
Graph, Pacific Atlantic Water Flow, Word Ladder, Alien Dictionary) and trees
(Max Depth, Validate BST, LCA, Level Order Traversal, Diameter). Tree
problems turned out to be the same concept, not a separate one — the
future-work question from the earlier version of this page is answered:
trees are traversal over an acyclic, single-parent-per-node structure, not a
different primitive.

**Open question carried over from `ABSTRACTION_QUESTIONS.md`:** at 11
problems, this is the closest any category has come to the ~20-problem
wrong-abstraction threshold — not close enough to conclude anything, but the
one to watch hardest.

**Alternative syntaxes considered:** none yet.

**Rejected designs:** None yet.

**Future work:** Union-Find (Number of Connected Components) was
deliberately NOT folded in here — it merges sets incrementally rather than
walking edges, tagged as a separate "Set Merging" candidate instead. Worth
revisiting whether that separation holds once more Union-Find-shaped
problems appear.
