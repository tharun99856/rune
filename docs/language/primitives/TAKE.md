# TAKE

**Status:** Established (in the grammar since commit 1).

**Why does this exist?**
Selecting a bounded number of elements from the front of a sequence is the
near-universal last step.

**Problems requiring it:** 001, 004.

**Current grammar:** `TAKE <n>`

**Important limitation, surfaced by problem 003 (First Unique):** TAKE
selects by *rank/position*, never by *predicate*. "Take the first element
matching a condition" is a different, currently unsupported shape — see
`docs/language/primitives/candidates/sequence-filter-with-fallback.md`. Do not extend
TAKE itself to silently absorb predicate logic; keep the two shapes distinct
until there's a real reason to merge them.

**Rejected designs:** None yet.

**Future work:** Resolve the filter-with-fallback candidate before deciding
whether it's a new concept, a modifier on TAKE, or something else.
