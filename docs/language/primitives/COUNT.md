# COUNT

**Status:** Established (in the grammar since commit 1).

**Why does this exist?**
Aggregation over groups (or a whole collection) is the near-universal second
step after GROUP.

**Problems requiring it:** 001, 002 (implicitly, via GROUP alone), 003, 004.

**Current grammar:** `COUNT EACH <noun>`

**Alternative syntaxes considered:** None yet.

**Rejected designs:** None yet.

**Open question:** `COUNT` is currently the only aggregation. SUM/MAX/MIN
haven't been requested yet in this batch, but the shape-algebra work (see the
sibling verified-intent-ir project's contract table) suggests they're the
same shape (Aggregation) and should probably arrive together, not as
one-off additions each time a problem asks for a different reduction.

**Future work:** Wait for a problem that actually needs SUM/MAX/MIN before
adding them — don't add speculatively.
