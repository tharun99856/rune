# EXPLORE

**Status:** Established. Promoted from candidate (`graph-traversal.md`) after
Traversal reached 24 problems in the ledger and held up as one coherent
concept across trees, grids, and graphs — see
`docs/language/V0.1_FREEZE.md`'s "Promoted since the freeze" section for the
full evidence and reasoning.

**Why does this exist?**
GROUP/COUNT/ORDER/TAKE have no notion of adjacency or connectivity at all —
they operate on flat collections, never a structure where elements relate to
neighbors. Traversal is a fundamentally different shape, and it recurs
across graphs, grids, and trees (a tree turned out to be the same concept,
restricted to an acyclic, single-parent structure — not a separate one).

**Problems requiring it:** graphs (Number of Islands, Course Schedule, Clone
Graph, Pacific Atlantic Water Flow, Word Ladder, Alien Dictionary) and trees
(Max Depth, Validate BST, LCA, Level Order Traversal, Diameter). Full list
in `docs/language/ledger.csv` (concept = "Traversal").

**Current grammar:** `EXPLORE <source> FROM <start> [TO <target>]`. Without
`TO`: returns a `{node: distance}` map (reachability from `start`). With
`TO`: returns the shortest distance to `target`, or `None` if unreachable.

**Strategy selection is a runtime decision, not a syntax one.** Unlike
`ORDER+TAKE -> TOP_K` (a compile-time rewrite, since the parser can see the
pattern in the syntax alone), whether to use BFS or Dijkstra depends on the
actual edge weights in the data, which the parser never sees. The runner
inspects the graph at execution time and picks BFS (all weights == 1) or
Dijkstra (otherwise), with the choice explained via
`rune.runner.explore_with_explanation`. See `python -m rune.cli explain`
and `docs/language/decisions/DECISIONS.md` for the correctness bug (tie-
breaking) this distinction surfaced.

**Rejected designs:** Union-Find (Number of Connected Components) was
deliberately NOT folded into this concept — it merges sets incrementally
rather than walking edges, and is tracked separately as the "Set Merging"
candidate.

**Future work:** Weighted-graph handling currently assumes non-negative
weights (Dijkstra's own precondition) — not yet validated or tested against
negative-weight input. Revisit if a problem in the ledger needs it.
