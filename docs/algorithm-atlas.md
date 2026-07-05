# Algorithm Atlas

This document tracks every algorithm studied while designing the language.

The purpose is NOT to solve LeetCode.

The purpose is to discover recurring human reasoning patterns that deserve
language primitives or compiler rewrite rules.

**Grammar is frozen while this atlas grows.** Current verbs: `GROUP...BY`,
`COUNT EACH`, `ORDER BY...[ASC|DESC]`, `TAKE`. Nothing else exists yet. Every
entry below was checked against the actual running parser
(`lang.parser.parse_program`), not reasoned about in the abstract — marked
**[verified]** where the real parser was run, **[reasoned]** where it wasn't
(and should be, before any primitive gets promoted).

A new verb is only added once the graveyard behind it is large enough.

---

## Legend

- Primitive Needed ✅
- Rewrite Rule 🔁
- Syntax Sugar ✨
- Library Pattern 📚
- Unknown ❓

---

## 001 Top K Frequent Elements

**Category:** Heap / Grouping

**Human Goal:** Return the K most frequent values.

**Current Language**
```algo
GROUP nums BY value
COUNT EACH group
ORDER BY count DESC
TAKE k
```

**Result:** WORKS **[verified]**

**Structural Shape:** Group, Aggregate, Order, Select

**Compiler Rewrite:** `ORDER DESC + TAKE k` → `TOP_K` → Heap 🔁

**Primitive Needed?** ❌

**Reason:** Already composes naturally from existing verbs.

**Notes:** The strongest possible result for this exercise — zero new syntax,
and the rewrite target (TOP_K) was already anticipated before any code existed.

---

## 002 Group Anagrams

**Category:** Hashmap / Grouping

**Human Goal:** Group strings that are anagrams of each other.

**Current Language**
```algo
GROUP words BY key
```

**Result:** WORKS **[verified]**

**Structural Shape:** Group

**Compiler Rewrite:** None

**Primitive Needed?** ❌

**Reason:** A single GROUP is already a complete, valid program — the grouping
itself *is* the answer.

**Notes:** Confirms a program doesn't need every verb to be legal.

---

## 003 First Unique Character

**Category:** Strings

**Human Goal:** Find the first character that appears exactly once.

**Current Language (attempted)**
```algo
GROUP chars BY value
COUNT EACH group
RETURN FIRST
WHERE count == 1
ELSE -1
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'RETURN'`

**Structural Shape:** Group, Aggregate, **Filter (missing)**, Select-first (missing)

**Missing Primitive:** A select-by-condition construct — filter to elements
satisfying a predicate, then take the first (with an ELSE fallback).

**Primitive Needed?** ✅ (pending frequency — see below)

**Reason:** No existing verb expresses "keep only where a condition holds."
ORDER+TAKE selects by *rank*, not by *predicate*. These are different shapes.

**Notes:** Important finding — this is the exact example used to argue the
language already worked. It didn't. Worth remembering *why* that distinction
matters.

---

## 004 Contains Duplicate

**Category:** Hashmap

**Human Goal:** Determine whether any value appears more than once.

**Current Language (attempted)**
```algo
GROUP nums BY value
COUNT EACH group
WHERE count > 1
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'WHERE'`

**Structural Shape:** Group, Aggregate, **Filter/existence-check (missing)**

**Missing Primitive:** Same select-by-condition gap as #003 — this time as an
existence check rather than a return-first.

**Primitive Needed?** ✅

**Reason:** Second independent occurrence of the same missing shape.

**Notes:** Two for two — filter-by-condition is looking like a real gap, not
a one-off.

---

## 005 Merge Intervals

**Category:** Sorting / Intervals

**Human Goal:** Merge all overlapping intervals.

**Current Language (attempted)**
```algo
ORDER BY start ASC
[merge adjacent overlapping intervals into one -- no verb for this]
```

**Result:** PARTIAL **[verified the ORDER line only]** — sorting works; the
merge-adjacent step has no verb at all.

**Structural Shape:** Order, **Stateful Scan (missing)**

**Missing Primitive:** A running left-to-right pass that carries and updates
state (extend-or-close the current interval).

**Primitive Needed?** ✅

**Reason:** Sorting alone isn't the algorithm — the scan that follows it is
where the actual merging happens, and nothing expresses that today.

**Notes:** First appearance of "Stateful Scan" as a missing shape.

---

## 006 Maximum Subarray (Kadane's)

**Category:** DP / Arrays

**Human Goal:** Find the contiguous subarray with the maximum sum.

**Current Language (attempted)**
```algo
SCAN nums KEEPING running_sum RESET WHEN running_sum < 0
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'SCAN'`

**Structural Shape:** **Stateful Scan (missing)**

**Missing Primitive:** Same shape as #005 — a running scan with resettable
state.

**Primitive Needed?** ✅

**Reason:** Second independent occurrence of Stateful Scan.

**Notes:** None of GROUP/COUNT/ORDER/TAKE apply here at all — this problem
doesn't partially work, it's a clean miss.

---

## 007 Climbing Stairs

**Category:** DP

**Human Goal:** Count the number of ways to reach the top (1 or 2 steps at a time).

**Current Language (attempted):** no verb applies — this is a pure recurrence
with rolling state, structurally identical to #006.

**Result:** BREAKS **[reasoned, not yet parser-tested]**

**Structural Shape:** Stateful Scan (same as Kadane's — O(1) trailing state)

**Missing Primitive:** Stateful Scan — third occurrence.

**Primitive Needed?** ✅

**Reason:** Confirms Stateful Scan/Recurrence is one shape, not two, appearing
under both "DP" and "arrays" category labels.

---

## 008 Coin Change (min coins)

**Category:** DP

**Human Goal:** Minimum coins needed to make a given amount.

**Current Language (attempted):** no verb applies — needs a recurrence over a
1D state space that (unlike #006/#007) can't be reduced to O(1) trailing state.

**Result:** BREAKS **[reasoned]**

**Structural Shape:** Stateful Scan / Recurrence — fourth occurrence, and the
first case needing a full state table rather than rolling state.

**Primitive Needed?** ✅

**Reason:** Same missing shape as #005–#007, but surfaces a real sub-question:
does "SCAN" need to express *how much* state it retains, or is that the
compiler's problem once the shape exists? Flagged, not resolved.

---

## 009 Longest Common Subsequence

**Category:** DP / Strings

**Human Goal:** Longest subsequence common to two strings.

**Current Language (attempted):** no verb applies.

**Result:** BREAKS **[reasoned]**

**Structural Shape:** Stateful Scan/Recurrence (2D state) + pairwise Relation
across two sequences.

**Primitive Needed?** ✅ (Scan) + possibly ✅ (Match/Relation, see #012)

**Reason:** Fifth occurrence of Stateful Scan; also the first case that might
need *two* missing primitives at once.

---

## 010 Reverse Linked List

**Category:** Linked Lists

**Human Goal:** Reverse a singly linked list.

**Current Language (attempted):** no verb applies.

**Result:** BREAKS **[reasoned]**

**Structural Shape:** Stateful Scan, over a pointer-linked representation
rather than an array.

**Primitive Needed?** ✅

**Reason:** Sixth occurrence of Stateful Scan — and evidence the same shape
recurs across totally different underlying data representations (array,
linked list, 1D/2D state table).

---

## 011 Binary Search

**Category:** Arrays / Search

**Human Goal:** Find a target's position in a sorted collection.

**Current Language (attempted)**
```algo
FIND target
IN sorted_numbers
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'FIND'`

**Structural Shape:** **Ordered Lookup (missing)**

**Missing Primitive:** FIND — doesn't decompose into anything smaller.

**Primitive Needed?** ✅

**Reason:** Breaks immediately and cleanly, exactly as predicted before
testing. Confirms Ordered Lookup is genuinely atomic.

---

## 012 Two Sum

**Category:** Hashmap / Arrays

**Human Goal:** Find two elements summing to target; return their positions.

**Current Language (attempted)**
```algo
MATCH nums WHERE a + b == target
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'MATCH'`

**Structural Shape:** **Relation/Join (missing)**

**Missing Primitive:** MATCH or JOIN — genuinely unresolved which name/shape
is right; only one data point so far.

**Primitive Needed?** ❓ — under investigation, not yet earned.

**Reason:** Only one occurrence in this batch. Per the "earn it" rule, this
needs more evidence before being promoted, even though it clearly doesn't
work today.

---

## 013 Sliding Window Maximum

**Category:** Arrays / Deque

**Human Goal:** Maximum of every contiguous window of size k.

**Current Language (attempted)**
```algo
WINDOW size k OVER nums
MAX each window
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'WINDOW'`

**Structural Shape:** **Window (missing)**

**Primitive Needed?** ✅

**Reason:** Breaks exactly as predicted; first occurrence of Window.

---

## 014 Longest Substring Without Repeating Characters

**Category:** Strings / Window

**Human Goal:** Longest substring with no repeated characters.

**Current Language (attempted):** no verb applies — needs a *variable*-size
window, unlike #013's fixed size.

**Result:** BREAKS **[reasoned]**

**Structural Shape:** Window — second occurrence, and evidence Window needs a
fixed/variable distinction as a property, not two separate verbs.

**Primitive Needed?** ✅

---

## 015 Number of Islands

**Category:** Graphs / Grid

**Human Goal:** Count connected regions of land in a grid.

**Current Language (attempted)**
```algo
EXPLORE grid FROM start
```

**Result:** BREAKS **[verified]** — `unrecognized step starting with 'EXPLORE'`

**Structural Shape:** **Graph Traversal (missing)**

**Primitive Needed?** ✅

**Reason:** First occurrence of EXPLORE; breaks cleanly as predicted.

---

## 016 Course Schedule

**Category:** Graphs

**Human Goal:** Determine whether all courses can be completed given prerequisites.

**Current Language (attempted):** no verb applies.

**Result:** BREAKS **[reasoned]**

**Structural Shape:** Graph Traversal — second occurrence.

**Primitive Needed?** ✅

---

## 017 Container With Most Water

**Category:** Two Pointers

**Human Goal:** Two lines that, with the x-axis, form the container holding
the most water.

**Current Language (attempted):** no verb applies.

**Result:** BREAKS **[reasoned]**

**Structural Shape:** Two-ended Scan — unresolved whether this is its own
primitive or a property of Window (converging from both ends vs. expanding
from one).

**Primitive Needed?** ❓ — under investigation.

**Reason:** Only one occurrence; also structurally ambiguous with Window.
Needs more data before deciding whether it's a separate verb.

---

# Statistics

Missing-primitive tally across this batch (17 problems: 2 work, 1 partial, 14 break):

```
Stateful Scan   ...... 6   (005, 006, 007, 008, 009, 010)
Graph Traversal ...... 2   (015, 016)
Window          ...... 2   (013, 014)
Filter/Select   ...... 2   (003, 004)
Relation/Match  ...... 1   (012)
Ordered Lookup  ...... 1   (011)
Two-ended Scan  ...... 1   (017, possibly = Window)
```

# Primitive Status

| Primitive | Status | Reason |
|---|---|---|
| Stateful Scan | **Leading candidate** | 6/17 — appears across DP, intervals, linked lists, and arrays; different representations, same shape |
| Graph Traversal | Under Investigation | 2/17 — expected to climb fast once more graph problems are run |
| Window | Under Investigation | 2/17 — needs a fixed-vs-variable property, not two verbs |
| Filter/Select-by-condition | Under Investigation | 2/17 — this is what broke the "First Unique already works" claim |
| Relation/Match | Under Investigation | 1/17 — too early; name (MATCH vs JOIN) still open |
| Ordered Lookup (FIND) | Under Investigation | 1/17 — but structurally atomic and unambiguous whenever it does appear |
| Two-ended Scan | Under Investigation | 1/17 — may not be a separate primitive from Window at all |

**Nothing is Accepted yet.** 17 problems is a first batch, not the "150
problems, 46 occurrences" scale needed to promote anything. Stateful Scan is
the clear frontrunner and the honest next candidate to earn a real verb, but
that decision should wait for a second batch, per the freeze.
