# DECISIONS

ADR-style log for Rune, following the same discipline used on the sibling
verified-intent-ir project: every entry carries Category, Status, a Revisit
condition, and Maintenance Cost. The pattern is reused deliberately; nothing
else is — Rune is a separate project with a separate mission.

---

## Rune is a separate project from verified-intent-ir

**Category:** Architecture
**Status:** Accepted
**Revisit:** Permanent.
**Maintenance Cost:** Low.

**Decision:** Rune (a language humans write to express algorithms) and
verified-intent-ir (a closed IR studying LLM claim calibration) are separate
missions, separate repos, separate roadmaps. Reuse the discipline (TDD,
structured explanations, hand-proven contracts as a pattern), never the
codebase.

**Reason:** Two different research questions don't need to share
architecture just because one was built first. Forcing them together would
carry Track-A baggage (LLM logging, claim verification) into a project that
has nothing to do with it yet.

---

## Grammar is frozen until atlas evidence justifies expansion

**Category:** Build Process
**Status:** Accepted
**Revisit:** When a candidate in `docs/language/primitives/candidates/`
accumulates enough independent problems to be promoted.
**Maintenance Cost:** Low — a discipline, not a mechanism.

**Decision:** No new concept (and therefore no new keyword) is added to the
parser until real problems, tested against the actual running grammar,
demonstrate it's needed — not reasoned about in the abstract.

**Reason:** Prevents keyword inflation, the most common failure mode of
language projects. See `docs/language/philosophy/style-laws.md` Law 5 and 8.

---

## Candidate documentation is named after the capability, not a presumed keyword

**Category:** Build Process
**Status:** Accepted
**Revisit:** Per-candidate, at the moment a concept is actually promoted and
given a real keyword — only then does it move out of `candidates/`.
**Maintenance Cost:** Low.

**Decision:** Files like `sequence-filter-with-fallback.md` are named after
the capability under investigation, never after a guessed spelling like
`WHERE.md`.

**Reason:** Naming a file after a keyword implicitly decides the spelling
before the capability itself is confirmed. This mistake was caught in
filenames after already being caught once in the atlas text itself (see next
entry) — worth guarding against at every layer, not just the parser.

---

## Correction: First-Unique and Contains-Duplicate are not the same capability gap

**Category:** Research (methodology)
**Status:** Accepted (as a precedent, not just a one-off fix)
**Revisit:** Whenever two atlas entries get tallied under the same missing
primitive — re-check they're actually the same shape before trusting the
count.
**Maintenance Cost:** Low.

**Decision:** The first pass of the atlas tallied Contains Duplicate
alongside First Unique Character as both "needing a filter" (WHERE). Re-examined
against the four-question discipline, Contains Duplicate is already solved by
existing concepts (spelled `GROUP...ORDER DESC...TAKE 1`); its only remaining gap is
interpreting a final scalar comparison — a different, much smaller question.

**Reason:** This is the concrete proof the atlas's discipline works: it
caught its own premature conclusion before any keyword was added, not after.

**Trade-offs:** None — this is a correction, not a compromise.

---

## Project named Rune; .rn extension; docs/language/ structure adopted

**Category:** Build Process / Branding
**Status:** Accepted
**Revisit:** Not planned, short of a strong reason.
**Maintenance Cost:** Low — a naming and folder-layout decision, not a
technical commitment.

**Decision:** The project (formerly `algolang`, package `lang`) is renamed
to **Rune**, directory `rune/`, package `rune/`, file extension `.rn`.
Future tooling: `runec` (compiler), `runefmt`, `runelsp`. Documentation moves
from a flat `docs/primitives/` into `docs/language/{atlas,primitives,grammar,
philosophy,decisions}` to make room for grammar/philosophy/decisions content
that a flat primitives folder had no place for.

**Reason:** A real, memorable name beats a placeholder before too much
tooling/documentation accumulates under the old one. The docs layout is
restructured now, while the surface area is still small, rather than later
when it would mean a much larger migration.

**Trade-offs:** None material — caught early, low migration cost (13 files
moved, imports fixed, tests re-verified green).

---

## Rune's identity is not "the AI language"

**Category:** Architecture / Branding
**Status:** Accepted
**Revisit:** Permanent — re-affirm any time an AI-recovery feature is added.
**Maintenance Cost:** Low — a framing discipline, not a mechanism.

**Decision:** The eventual AI recovery layer (semantic negotiation, ambiguity
resolution — see the original project brief) is one feature of Rune, not
Rune's identity. If AI models change completely in five years, Rune should
still be a good, usable language on its own deterministic merits.

**Reason:** Tying a language's identity to a specific AI capability makes it
obsolete the moment that capability is superseded or commoditized. The
deterministic core (grammar, parser, rewrite engine, strategy selection) is
what should still matter in twenty years.

---

## Internal vocabulary: "concept" and "keyword" are never the same word

**Category:** Architecture
**Status:** Accepted
**Revisit:** Permanent.
**Maintenance Cost:** Low — a vocabulary discipline, applied across existing
docs, not a new mechanism.

**Decision:** Stop calling `GROUP`, `ORDER`, `TAKE`, `COUNT` "verbs" as if the
spelling were the fundamental unit. A **concept** (Grouping, Ordering,
Selection, Aggregation, and future candidates like Stateful Scan or
Traversal) is the semantic idea. A **keyword** is today's spelling of one
concept. `GROUP` could later legally become `CLUSTER` without the concept of
Grouping changing at all.

**Reason:** This distinction becomes load-bearing the moment Rune has more
than one candidate spelling for the same idea, or the moment a keyword needs
renaming for readability reasons unrelated to what it does. Making it
explicit now, while there are only four keywords, costs nothing; retrofitting
it after dozens of docs conflate the two would not.

**Trade-offs:** None — a same-day terminology sweep across existing docs
(no new files beyond this entry), not new process.
