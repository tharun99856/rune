## Problem

Not an algorithm — a periodic review of grammar pressure, the capped
"go read the problems" step `python -m rune.cli mine` exists to trigger.
Question: does any open candidate have enough evidence to promote today?

## Current Rune

N/A. This entry decides nothing about syntax; it reads the ledger and the
candidate set and records a verdict so the next session doesn't re-derive it.

## Pain points

`mine` and a direct tally of `docs/language/ledger.csv` (100 problems) agree.
Concept occurrences, highest first:

```
34  Stateful Scan   -> resolved: dissolved (2026-07-09-stateful-scan-dissolved.md)
24  Traversal       -> resolved: promoted to EXPLORE (primitives/EXPLORE.md)
12  Aggregation     -> established primitive (COUNT)
12  Ordering        -> established primitive (ORDER)
10  Relation        -> candidate: relation-or-computed-group-key.md
10  Window          -> candidate: windowed-view.md
 8  Enumeration     -> NOT TRACKED (no candidate page)
 7  Grouping        -> established primitive (GROUP)
 7  Selection       -> established primitive (TAKE)
 5  ADT Definition  -> not tracked (likely not a pipeline question)
 3  Ordered Lookup  -> candidate: ordered-lookup.md
 3  Set Merging     -> not tracked
 2  Filtering       -> candidate: sequence-filter-with-fallback.md
 2  Serialization   -> not tracked
 1  Streaming / Construction
```

Review threshold is 15 (`rune/cli.py`). The only concepts that ever crossed it
are the two already resolved. **No open candidate is anywhere near the bar** —
the highest, Relation and Window, are tied at 10, still 5 short.

## Candidate capabilities

Two findings, both honest, neither a grammar change:

1. **Watch-list: Relation (10) and Window (10).** Tied for the most-pressured
   *unresolved* capability. Both stay open. The next few research entries are
   better spent here than on another Stateful-Scan-shaped problem, whose
   bucket is already resolved and adds no signal.

2. **Enumeration (8) is accumulating pressure with no candidate page.** Eight
   independent problems (035 Subsets, 036 Permutations, 037 N-Queens, 066
   Combination Sum, 069 Combination Sum II, 070 Word Search, 071 Palindrome
   Partitioning, 091 Word Search II) all reach for exhaustive enumeration with
   pruning, and nothing in `candidates/` tracks it. Per CLAUDE.md step 2, an
   untracked-but-recurring capability should get a candidate page named after
   the *capability* — this is starting to track pressure, explicitly NOT
   promoting a keyword. Added as
   `candidates/exhaustive-enumeration-with-pruning.md`.

## Rejected capabilities

Rejected promoting anything. Nothing crossed 15; acting on a count of 10 would
be exactly the "first plausible-looking number" mistake the atlas warns against
(see the Grammar Pressure note about the Filter/WHERE miscount). Also rejected
opening candidate pages for ADT Definition (5), Set Merging (3), and
Serialization (2): each is plausibly *not* a pipeline-shaped question at all,
and none has the independent-problem volume Enumeration does.

## Decision

HOLD — no promotion. Record the watch-list (Relation, Window). Start tracking
Enumeration with a capability-named candidate page. No grammar change, no
keyword proposed. Capped here, as the ritual requires.

## Outcome

🧩 New capability candidate — Enumeration, tracking-only (page created, not
promoted). All other candidates: hold and keep gathering.

## Next experiment

Solve one Relation-shaped and one Window-shaped problem next (they are tied at
the top and both under-journaled), plus one more Enumeration problem to confirm
the new candidate's shape is stable — before anything is considered for
promotion.
