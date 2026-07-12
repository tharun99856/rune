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

---

## Tie-breaking is a defined, deterministic rule -- not implementation-dependent

**Category:** Architecture (correctness)
**Status:** Accepted
**Revisit:** Whenever a new backend is added, or `Order`/`TopK` gains a new
tie-break-relevant field.
**Maintenance Cost:** Low — one shared convention, applied consistently.

**Decision:** When two items tie on the primary sort/selection key
(`ORDER`'s key, or `TOP_K`'s), the secondary, deterministic tie-break is the
item's own identity key, always ascending, regardless of the primary
direction. Every backend must implement this exact rule, not just "a
reasonable one."

**Reason:** Building the presentable demo surfaced a real bug: `InterpreterBackend`
(Python's stable `sorted`/`heapq`) and `NumbaBackend` (`numpy.argpartition`)
picked *different* members of a tied group at the selection boundary — both
individually correct counts, but a real correctness gap, because switching
backends could silently change which result you got. This was caught by a
test that forced an exact-order comparison on deliberately tied data, not by
inspection — the mismatch didn't show up until a specific random seed
happened to produce a tie, which is exactly why "run the demo, see if it
looks right" isn't sufficient and an explicit tie-break rule is.

**Trade-offs:** Slightly more code in each backend (a combined sort/score
key instead of the naive one). `NumbaBackend.supports()` also now only
claims `TopK(descending=True)` — the `descending=False` case was never
implemented correctly in the first place (a second bug the same
investigation caught) and is honestly excluded rather than silently wrong.

---

## Traversal (`EXPLORE`) promoted from candidate to grammar

**Category:** Architecture (language)
**Status:** Accepted
**Revisit:** Not planned unless `ABSTRACTION_QUESTIONS.md`'s remaining open
half (control-flow-heavy graph algorithms, untested) turns up a real problem.
**Maintenance Cost:** Medium — a genuinely new data shape (graphs, not flat
sequences) and a runtime-decided strategy (BFS vs. Dijkstra), not just
another flat keyword.

**Decision:** Promote Traversal to a real keyword (`EXPLORE ... FROM ...
[TO ...]`), making it the fifth concept in a grammar the freeze document
said would stay at four "unless something genuinely breaks the model."

**Reason:** 24 ledger problems (second only to Stateful Scan's 34) and,
unlike Stateful Scan, no internal splitting needed — it held up as one
concept across trees, grids, and graphs. It also unlocked a second,
structurally different optimizer proof (a runtime data-dependent decision,
not a compile-time syntax rewrite), which is what made it worth promoting
on its own rather than batching it with a future round.

**Process gap, logged honestly:** this promotion happened without writing
this entry or updating `V0.1_FREEZE.md`/`grammar/current.md` at the time —
both documents said "four concepts" for several commits after a fifth
existed. Caught and fixed once the repo went public and the inconsistency
mattered enough to look for. The lesson, not just the fix: "explain your
reasoning" has to include updating the documents that claim to be current,
not only writing new ones.

**Trade-offs:** Stateful Scan (34 problems, higher raw pressure) was
deliberately *not* promoted alongside this — one promotion at a time, per
Law 9, and its internal shape (Recurrence vs. Stack vs. Pointer) is still
unresolved. Promoting it now would have meant guessing under that
uncertainty just to batch two decisions together.

---

## Stateful Scan dissolved — an implementation shape, not a concept

**Category:** Research (language)
**Status:** Accepted
**Revisit:** If a whole-ledger sweep for objective-shaped intents (the real
signal it surfaced) turns up something that changes the picture.
**Maintenance Cost:** Low — a candidate removed, not machinery added.

**Decision:** Stateful Scan — the single highest-frequency candidate (34
problems) — is **not** a Rune concept and will not be promoted, as one
concept or as the three (Recurrence/Stack/Pointer) an earlier split
proposed. Full argument in
`docs/language/research/2026-07-09-stateful-scan-dissolved.md`.

**Reason:** Re-classified by *intent* rather than mechanism, the 34 problems
scatter across ≥8 unrelated intent families. A single concept covering them
would need an arbitrary user-supplied step function (a `fold`/`scanl`), which
is precisely the closed-vocabulary escape hatch Rune's founding constraint
forbids. So it's not one concept; and split apart, its members already belong
to existing concepts or to a new one (objectives) now tracked separately. It
was an implementation shape — "a pass that keeps state," which Python renders
uniformly as `for` + a mutable variable — read as if it were an intent.

**Why this is a good outcome, not a setback:** it's the exact failure mode
the intent-over-implementation thesis predicts (the most Python-common
pattern looks like the most important concept, precisely because it's an
*implementation* commonality), and the evidence discipline caught it before
it became a keyword. The genuine signal — 15+ problems stating an objective
(max/min/count/exists) over a space — is now its own candidate
(`objective-over-scope.md`), where DP is the compiler's technique, not the
language's concept.

**Trade-offs:** The ledger's 34 "Stateful Scan" tags are left in place as
honest *mechanism* observations; a wholesale intent re-tag was declined as
premature (it would mean inventing objective-concept tags before those
concepts are defined — the fill-the-table guessing this project avoids).
Consequence: `rune mine` will keep listing Stateful Scan at 34 until that
re-tag happens. Acceptable, because the tool explicitly reports counts as
"go read these," not verdicts — and the verdict now lives in the research
journal and here.

---

## The closed-vocabulary ceiling: predicate-scoped optimization (much of DP)

**Category:** Research (the honest limit of the approach)
**Status:** Accepted (as a finding, not a resolution — see Revisit)
**Revisit:** If anyone finds a way to name a predicate-defined scope in
closed vocabulary. That would move the ceiling; nothing found so far does.
**Maintenance Cost:** Low — it's a boundary written down, not machinery.

**Decision / finding:** The whole-ledger objective sweep
(`docs/language/research/2026-07-09-objectives-scope-closure.md`) shows
objective-shaped problems split by *scope*: structural scopes (contiguous
subarrays, windows, pairs, rank) close cleanly and are a viable narrow
concept; predicate-defined scopes (subsets *summing to X*, *increasing*
subsequences, *palindromic* substrings, *dictionary* segmentations) do not —
naming them needs an arbitrary predicate, which the founding closed-vocabulary
rule forbids. The predicate group (~12–14) outnumbers the structural (~10).

**Why this matters as a project-level decision, not just a candidate note:**
this is the first concrete evidence of *where Rune's closed-vocabulary bet
ceilings out*. A whole class — optimization over a predicate-defined space,
i.e. much of classic DP — appears fundamentally inexpressible in Rune without
abandoning the property that lets its optimizer reason at all. So "solve the
DP-heavy portion of a standard problem set in Rune" is, on current
understanding, **not a reachable goal**, and should not be marketed or
planned as one. Naming this ceiling now prevents chasing it as a feature and
discovering it as a wall.

**Not fatal, and worth stating both halves honestly:** Rune still cleanly
covers grouping, aggregation, ordering, selection, traversal, and
structural-scope objectives — a real, useful, provable slice. The ceiling
bounds the ambition; it doesn't collapse it. (It's also arguably the most
*interesting* thing to report about a closed-vocabulary intent language:
precisely which problems it can and cannot express, and why.)

**Trade-offs:** Deflates the "objectives" excitement — the motivating DP
problems are the ones out of reach. Better known now.

---

## Identity fixed: Rune stays closed & provable (not "every DSA problem")

**Category:** Architecture (identity)
**Status:** Accepted — the user's explicit call
**Revisit:** Permanent, short of the user reversing it. This is the founding
bet; reversing it is a different project.
**Maintenance Cost:** Low — it's a boundary that *prevents* work (arbitrary
predicates), not one that adds any.

**Decision:** When the ambition "an exclusive DSA language where every hard
question can be solved" collided with the closed-vocabulary finding, the user
chose to keep Rune **closed and provable**: it expresses the closeable slice
of DSA and its superpower is that the compiler picks the algorithm from intent
*and proves it*. It explicitly does NOT aim to solve every DSA problem —
predicate-scoped DP is out (the ceiling), and that's accepted.

**Reason:** The two goals are mutually exclusive, and not by an engineering
limit but by Rice's theorem. "Solve every hard problem" requires arbitrary
user predicates; the moment those exist, the optimizer can't know what a
program does, and "the compiler chooses and proves the algorithm" — the entire
novel contribution, the reason to open-source it — stops being possible. A
language that does everything already exists (Python) and Rune would lose to
it. A language that provably chooses your algorithm from intent exists nowhere.
Narrow-but-novel beats broad-but-redundant.

**Trade-offs:** Rune will never be a general DSA solver, and that has to be
said plainly rather than implied away — "solve Striver's sheet in Rune" is not
a reachable goal for the DP-heavy portion. In exchange it keeps the one
property that makes it worth existing.

---

## Objective (`MAXIMIZE`/`MINIMIZE`) promoted — structural scope only

**Category:** Architecture (language)
**Status:** Accepted — the user's explicit call (delegated: "choose the best one")
**Revisit:** When evidence warrants another *structural* scope (`OVER PAIRS`,
`OVER WINDOWS`). Never for predicate scopes — that's the ceiling.
**Maintenance Cost:** Medium — a new plan node (KadaneScan), a naive baseline,
and an optimizer rule, all with the naive/optimized equivalence to maintain.

**Decision:** Promote `MAXIMIZE|MINIMIZE SUM OVER CONTIGUOUS` as the sixth
concept — the closeable first scope of the objective candidate. Sole measure
`SUM`, sole scope `CONTIGUOUS`, on purpose.

**Reason:** It's the concrete embodiment of the closed-and-provable identity:
a real intent (best sum over contiguous subarrays), a real, provable compiler
decision (recognize optimal substructure → Kadane O(n) vs naive O(n²)), and
zero predicate hatch. It's the third distinct optimizer proof and the first
DP-flavored one — evidence the "compiler picks the algorithm" thesis
generalizes past collections and graphs into optimization, at least for
structural scopes. ~1090x at n=4000, identical result, checked against the
naive baseline on 200 random arrays.

**Trade-offs:** Narrow (one measure, one scope). That narrowness is the point —
it's exactly the closeable boundary, not an MVP shortcut. Extending to other
*structural* scopes is future promotion work; extending to predicate scopes is
forbidden by the ceiling entry above.
