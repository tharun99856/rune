# ORDER

**Status:** Established (in the grammar since commit 1).

**Why does this exist?**
Ranking by a key, ascending or descending, is required by every problem that
needs "the best/most/least N," and composes directly with TAKE.

**Problems requiring it:** 001, 004, 005 (partially — sorting works, the
merge step after it doesn't).

**Current grammar:** `ORDER BY <key> [ASC|DESC]`, defaults to ascending.

**Rejected designs:** None yet.

**Compiler rewrite already anticipated:** `ORDER ... DESC` immediately
followed by `TAKE k` is a candidate for a `TOP_K` internal rewrite (heap
selection instead of a full sort), confirmed by problem 001. This is a
rewrite, not new syntax — the human never writes `TOP_K`.

**Future work:** None currently pending.
