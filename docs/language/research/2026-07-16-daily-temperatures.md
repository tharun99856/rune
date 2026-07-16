## Problem

Daily Temperatures (ledger 047). For each day, how many days until a warmer
temperature (0 if none ever comes).

**Solved in English first, no Rune in mind:**

> For each day, look forward to the nearest later day that is warmer, and
> report how far away it is. (Efficiently: walk the days keeping a shortlist
> of days still waiting for their warmer day; each new day answers everyone
> on the shortlist it beats, then joins it.)

The efficient version is a monotonic stack — but per the 2026-07-09
dissolution, the *mechanism* is not the finding. The intent is: **relate each
element to the nearest later element greater than it.**

## Current Rune

No plausible attempt exists — stated honestly rather than running a strawman
(same stance as 2026-07-07). The required output is *per-element* (one span
for every position), derived from a *positional, directional* relation. Every
current concept fails structurally, not incidentally: `GROUP` partitions away
sequence order, `ORDER` replaces it, `TAKE` only bounds length, `EXPLORE`
consumes graphs, and objectives collapse to a single scalar. Nothing in the
grammar even superficially resembles "for each element, the nearest later
greater one."

## Pain points

Two distinct absences show up *at once*:

1. **The relation itself** — "nearest later element greater than me" relates
   pairs of positions, which is the capability
   `relation-or-computed-group-key.md` already tracks (opened for Two Sum).
2. **Per-element output** — the answer has the input's shape (one value per
   position), a family the dissolution's intent re-classification already
   named (Product of Array Except Self, Counting Bits) but which no candidate
   currently tracks on its own.

Worth naming precisely: this problem needs both, and they are separable —
3Sum needs (1) without (2); Product of Array Except Self needs (2) without (1).

## Candidate capabilities

**Not a new gap.** Second data point for the existing
`relation-or-computed-group-key` candidate — exactly where the 2026-07-09
dissolution re-filed this problem's intent ("next-greater / span relation,
closer to Two Sum than to Valid Parentheses").

It sharpens that candidate's open question rather than resolving it: the
page's hypothesis 2 (a *computed* GROUP key, e.g. `target - value`) works
naturally for **value** relations like Two Sum, but next-greater is a
**positional, directional** relation — "later than me" is not a key any
grouping can compute, because it's relative to each element, ordered, and
asymmetric. First concrete evidence the candidate's two hypotheses may cover
different sub-shapes instead of competing for the same one.

## Rejected capabilities

- **Reviving a stack candidate.** The monotonic stack is how Python solves
  this, not what is meant — the dissolution's argument applies verbatim, and
  re-opening a mechanism bucket two entries after closing it would need new
  evidence, of which this problem (re-read by intent) provides none.
- **Filing it under `windowed-view`.** The span to the next warmer day is not
  a fixed or sliding window; its extent is *defined by the relation's answer*,
  not by the program. Considered because "span" sounds windowish; rejected
  because the window candidate is about bounded views the program moves,
  not distances the data determines.

## Decision

No grammar change. Updated `relation-or-computed-group-key.md` (two data
points, hypothesis-tension noted), added atlas #047, ledger row 047 untouched
(its mechanism tag stays, per the dissolution's deliberate no-retag decision).

Housekeeping correction alongside: the 2026-07-14 sort-characters entry's
"Next experiment" still pointed at the stateful-scan over-aggregation
question, which the 07-09 dissolution had already closed — fixed to point at
the live leads (Relation, Window, Enumeration). Stale pointer, my error,
caught by re-reading the dissolution before writing this entry.

## Outcome

🧩 New capability candidate — explicitly *not new*: second data point for the
existing `relation-or-computed-group-key` candidate, and the first evidence
its two hypotheses may be sub-shapes rather than rivals.

## Next experiment

The candidate page's own next step is now sharper: attempt Two Sum under
hypothesis 2 concretely (`GROUP nums BY <computed key>`) and run it against
the real parser — then attempt the same phrasing for next-greater and watch
*where* it breaks. If hypothesis 2 handles value relations but structurally
cannot state positional ones, the candidate splits along that line, and each
half needs its own evidence before any promotion talk.
