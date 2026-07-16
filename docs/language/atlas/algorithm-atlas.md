# Algorithm Atlas

This document tracks every algorithm studied while designing the language,
**and the evolution of the language itself.**

The purpose is NOT to solve LeetCode. The purpose is to discover recurring
human reasoning patterns that deserve language primitives or compiler rewrite
rules — and to resist inventing keywords just because a problem failed.

**Discipline, applied to every failure, in this order:**
1. Can the current language already express this (even awkwardly)?
2. Can this be a compiler rewrite of something already expressible?
3. Can this be syntax sugar over existing concepts?
4. Only then: does this need a genuinely new primitive — and even so, the
   *capability* is established before any keyword/spelling is chosen.

Grammar is still frozen — `docs/language/grammar/current.md` documents exactly
what the parser accepts, and the parser, not this file, is ground truth. Two
concepts have been promoted since v0.1 on the evidence below: Traversal
(`EXPLORE`) and Objective (`MAXIMIZE`/`MINIMIZE`). "Design Decision" below is
always an open question, never a conclusion.

---

## Legend

- ✅ Already expressible with current concepts
- 🔁 Candidate for compiler rewrite
- ✨ Candidate for syntax sugar
- ❓ Genuinely open — capability unclear, naming unclear
- 🚫 Deferred — insufficient evidence to decide anything

---

## 001 Top K Frequent Elements

**Human Solution:** Return the K most frequent values.

**Current Language:** ✅ `GROUP nums BY value / COUNT EACH group / ORDER BY count DESC / TAKE k`

**Design Decision:** None needed. 🔁 candidate: `ORDER DESC + TAKE k` → `TOP_K` → Heap, purely a compiler-internal rewrite, no new syntax.

**Status:** Resolved — works today.

---

## 002 Group Anagrams

**Human Solution:** Group strings that are anagrams of each other.

**Current Language:** ✅ `GROUP words BY key`

**Design Decision:** None needed.

**Status:** Resolved — works today.

---

## 003 First Unique Character

**Human Solution:** Find the first character that appears exactly once, else -1.

**Current Language:** ❌ `GROUP chars BY value / COUNT EACH group` gets this far; nothing
expresses "keep only where count == 1, take the first survivor, or -1 if none
survive."

**Q1 — expressible today?** No. Checked directly: could a clever `ORDER BY`
key (e.g. "non-unique-ness ascending, then original index ascending") fake
this? No — even that trick can't express the -1 fallback, because nothing in
the result tells you whether a real match was found or you're just looking at
the best non-match.

**Q2/Q3 — rewrite or sugar?** No — there's no existing composition to rewrite
or desugar from.

**Q4 — new capability, name undecided.** The actual gap may be *two* smaller
things, not one: (a) restrict a sequence to elements matching a condition,
(b) take-first-or-default when nothing matches. Whether these are one
primitive or two is itself an open question — don't presume "WHERE" and
"ELSE" are separate keywords, or even that they're needed at all in that form.

**Design Decision:** ❓ Genuinely open.

**Status:** Deferred.

---

## 004 Contains Duplicate

**Human Solution:** Does any value appear more than once?

**Current Language:** ✅ (mostly) — `GROUP nums BY value / COUNT EACH group / ORDER BY count DESC / TAKE 1` already gives the highest-count group. **Verified this parses.**

**Correction from the previous pass:** this was wrongly tallied alongside
#003 as "needs a filter." It doesn't. The only remaining gap is interpreting
the *final scalar* result ("is that one count > 1?") — a completely different,
much smaller question than #003's actual gap (filtering an entire sequence,
with a fallback). Conflating them was exactly the premature-keyword-inflation
mistake this atlas exists to catch.

**Q1:** Yes, almost entirely.
**Remaining question:** does the language need any notion of a final
boolean/scalar assertion on a pipeline's result at all — and is that a
language concern or a compiler/output-interpretation concern? Possibly not a
grammar question at all.

**Design Decision:** ❓ Open, but much narrower than #003's.

**Status:** Deferred — different shape than previously assumed.

---

## 005 Merge Intervals

**Human Solution:** Merge all overlapping intervals.

**Current Language:** ✅ for the sort (`ORDER BY start ASC`); ❌ for the merge
step — nothing expresses "walk left to right, extend or close the current
interval."

**Q1–Q3:** No existing concept or composition covers a running accumulate-while-scanning pass.

**Q4:** New capability needed — a stateful, left-to-right scan that carries
forward state. Name and exact shape undecided.

**Design Decision:** ❓ Open.

**Status:** Deferred.

---

## 006–010 Maximum Subarray (Kadane's), Climbing Stairs, Coin Change, Longest Common Subsequence, Reverse Linked List

**Human Solution (shared shape):** each is a running computation that carries
state forward (a sum that resets, a rolling count, a growing table, pointer
relinking).

**Current Language:** ❌ for all five — none of GROUP/COUNT/ORDER/TAKE apply;
these aren't near-misses, they're clean misses.

**Q1–Q3:** No existing composition covers any of these.

**Q4:** All five point at the same *candidate* capability as #005 (a stateful
scan), but **whether it's genuinely one primitive or several is unresolved** —
Coin Change and LCS need a full state table, Kadane's/Climbing-Stairs only
need O(1) trailing state, Reverse-List operates over a different underlying
representation (pointer-linked, not array) entirely. Do not presume "one SCAN
primitive covers all of this" — that's exactly the kind of premature
conclusion this atlas is supposed to prevent.

**Design Decision:** ❓ Open, and specifically flagged: **the biggest error
this atlas is at risk of making now is over-merging distinct needs into one
convenient bucket, the same way #003/#004 were briefly conflated.**

**Status:** Deferred, all five.

---

## 011 Binary Search

**Human Solution:** Find a target's position in a sorted collection.

**Current Language:** ❌ `FIND target / IN sorted_numbers` — no concept resembling this exists. **Verified.**

**Q1–Q3:** No existing concept or composition searches by value; GROUP/ORDER/TAKE
operate over whole collections or ranks, never "locate this specific value."

**Q4:** New capability needed. Structurally the most atomic candidate found
so far — doesn't decompose further, only one data point, name undecided.

**Design Decision:** ❓ Open.

**Status:** Deferred.

---

## 012 Two Sum

**Human Solution:** Find two elements summing to target; return positions.

**Current Language:** ❌ — no concept relates pairs of elements.

**Q1, re-examined:** does `GROUP` already cover this if it supported a
*computed* key rather than only a literal field? E.g. grouping by
`target - value` instead of `value` might get partway there. This wasn't
considered in the first pass and is a genuinely open alternative to "add a
new MATCH/JOIN concept" — **extending an existing primitive's expressiveness vs.
adding a new one** is exactly the kind of choice this atlas should force
before deciding.

**Design Decision:** ❓ Open — two live hypotheses (extend GROUP vs. new
relation primitive), not yet one data point clearly pointing either way.

**Status:** Deferred.

---

## 013–014 Sliding Window Maximum, Longest Substring Without Repeating Characters

**Human Solution:** A bounded, moving view over a sequence (fixed size for
#013, expanding/contracting for #014).

**Current Language:** ❌ both — no concept creates any kind of windowed view.

**Q1–Q3:** No existing composition applies.

**Q4:** New capability needed, likely one shape with a fixed/variable
property rather than two separate concepts — but only two data points so far.

**Design Decision:** ❓ Open.

**Status:** Deferred.

---

## 015–016 Number of Islands, Course Schedule

**Human Solution:** Visit connected structure (grid connectivity / dependency graph).

**Current Language:** ❌ both — GROUP/COUNT/ORDER/TAKE have no notion of
adjacency or connectivity at all.

**Q4:** New capability needed — graph/grid traversal. Two data points.

**Design Decision:** ❓ Open.

**Status:** Deferred.

---

## 017 Container With Most Water

**Human Solution:** Two lines that, with the x-axis, hold the most water.

**Current Language:** ❌ — no concept converges two positions.

**Design Decision:** ❓ Open — possibly the same shape as Window (a window
that shrinks from both ends rather than slides), possibly distinct. One data
point only.

**Status:** Deferred.

---

## 047 Daily Temperatures

**Human Solution:** For each day, how many days until a warmer temperature.

**Current Language:** ❌ — no plausible attempt exists. The answer is
per-element (a span for every position), computed from a positional relation
("the nearest *later* element greater than this one"). GROUP discards
sequence, ORDER re-sorts it away, TAKE only bounds length, EXPLORE consumes
graphs, objectives return one scalar — nothing to run without inventing a
strawman.

**Design Decision:** ❓ Open — second data point for the *relation* candidate
(`primitives/candidates/relation-or-computed-group-key.md`), where the
Stateful Scan dissolution already re-filed this problem's intent
(next-greater/span relation — closer to Two Sum than to Valid Parentheses).
It also stresses the candidate's hypothesis 2 (computed GROUP key): Two Sum
relates *values*, but next-greater relates *positions with a direction* —
early evidence the two hypotheses may not be interchangeable.

**Status:** Deferred — tracked on the relation candidate. See
`research/2026-07-16-daily-temperatures.md`.

---

## 101 Sort Characters by Frequency

**Human Solution:** Count how many times each character appears, then list the
characters from most frequent to least.

**Current Language:** ✅ `GROUP text BY value / COUNT EACH char / ORDER BY count DESC`
— [verified] parses through `rune.parser.parse_program` and [verified] runs
through `run_program` (e.g. `mississippi` → i:4, s:4, p:2, m:1). It is exactly
#001's shape minus the final `TAKE`.

**Design Decision:** None needed. No new concept — this is a third independent
confirmation (with #001, #004) that Grouping + Aggregation + Ordering is a
load-bearing, already-closed pattern. Running it *did* surface an interpreter
bug — the descending tiebreak negated the sort key, assuming numbers, and
crashed on character keys — but that was an implementation defect (fixed in
`rune/runner.py`, regression-tested), not a grammar gap. Materializing the
answer back into a repeated-character string is presentation/serialization,
deliberately outside the pipeline (same boundary #001 draws).

---

# Grammar Pressure

This is signal, not a queue of approved keywords. A high count means a
capability keeps getting requested — it does not mean a keyword is approved,
and it does not mean the count is even measuring one thing (see #003/#004 and
#006–010 corrections above).

```
Stateful scan / running accumulation  ...... 6   (005–010)
Graph / grid traversal                ...... 2   (015, 016)
Windowed view (fixed or variable)     ...... 2   (013, 014)
Sequence filter + fallback            ...... 1   (003 only -- 004 removed after correction)
Final scalar assertion                ...... 1   (004 -- newly separated out, likely NOT a grammar question)
Relation between pairs / computed-key GROUP ... 1   (012 -- two competing hypotheses)
Ordered lookup by value               ...... 1   (011)
Two-ended convergence                 ...... 1   (017 -- possibly = windowed view)
```

**Nothing here is a decision.** The previous version of this atlas tallied
"Filter/WHERE" at 2; it's really 1, plus a separate, smaller, possibly
non-grammar question. That correction is the whole point of tracking pressure
this carefully instead of acting on the first plausible-looking number.

---

# Primitives (established, already in the grammar)

See `docs/language/primitives/GROUP.md`, `COUNT.md`, `ORDER.md`, `TAKE.md` for why each
of the four current concepts exists.

# Primitives (candidates, not yet decided)

See `docs/language/primitives/candidates/` — one page per open capability question
above, named after the *capability*, not a presumed keyword spelling.
