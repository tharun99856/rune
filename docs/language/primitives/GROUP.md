# GROUP

**Status:** Established (in the grammar since commit 1).

**Why does this exist?**
Partitioning a collection by a key is the single most common first step
across the anchor problems tested so far (Top-K-Frequent, Group-Anagrams,
First-Unique all start here).

**Problems requiring it:** 001, 002, 003, and every problem needing a
frequency count first.

**Current grammar:** `GROUP <source> BY <key>`

**Alternative syntaxes considered:** None yet — this was part of the first
slice, not derived from pressure. Worth revisiting once more problems accumulate.

**Rejected designs:** None yet.

**Open question (see docs/algorithm-atlas.md #012):** should `GROUP` support
a *computed* key (e.g. `GROUP nums BY (target - value)`), not just a literal
field reference? This would extend GROUP's reach into territory currently
assumed to need a new relation/join primitive (Two Sum). Unresolved — this is
exactly the kind of question that should be answered before adding a new verb.

**Future work:** Resolve the computed-key question before considering a
separate MATCH/JOIN primitive.
