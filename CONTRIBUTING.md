# Contributing to Rune

Rune accepts three kinds of contribution. They are not equally easy to land,
and that's by design.

## 1. Research entries — always welcome, the lifeblood

Pick an algorithm problem not already in `docs/language/ledger.csv` and run
the ritual (`docs/language/research/README.md` is the authority):

1. **Solve it in plain English first.** No Rune in mind.
2. **Translate to today's grammar** (`docs/language/grammar/current.md`) and
   run the attempt through the real parser — `rune.parser.parse_program` —
   not through reasoning about it. Mark findings `[verified]` or `[reasoned]`
   honestly. If no plausible attempt even exists, say so rather than
   inventing a strawman to fail.
3. **End with exactly one outcome:** ✅ already expressible, 🔁 compiler
   rewrite, ✨ syntax sugar, 🧩 capability candidate (usually evidence for an
   *existing* page in `docs/language/primitives/candidates/` — don't
   manufacture novelty), or ❌ wrong abstraction (rare; needs ~20 problems in
   one category, never one).
4. Add the entry as `docs/language/research/YYYY-MM-DD-problem-slug.md`, add
   a ledger row, and update the candidate page if your problem is evidence
   for one.

"No new gap — this confirms an existing candidate" is a *successful* entry.
Most entries should end that way; that's the discipline working.

## 2. Implementation — welcome, with TDD

Bug fixes, smarter strategy selection, new optimizer rewrites over *existing*
syntax, better error messages, backends. The rules:

- **Failing test first, watch it fail, minimal code, watch it pass.** No
  production code without a failing test.
- Every `.rn` under `docs/language/examples/` must keep parsing
  (`tests/test_examples.py` enforces it). Breaking one is a regression, not
  a tradeoff.
- Optimizations must be verified against the naive baseline they replace,
  like the existing TOP_K/Kadane rewrites are.
- `python -m pytest` green before any PR.

## 3. Grammar changes — read this before opening the PR

**A PR that adds a keyword will be closed, however good the idea is.** Not
because it's wrong — because that's not how vocabulary enters this language.

The path a new capability actually takes:

1. Independent problems accumulate in the ledger, tagged with the concept.
2. `python -m rune.cli mine` shows the concept crossing the review threshold
   (currently 15 occurrences).
3. A capped investigation reads the problems and issues a verdict — promote,
   split, merge, or dissolve. (Both concepts ever promoted — `EXPLORE` and
   `MAXIMIZE`/`MINIMIZE` — went through exactly this. So did one that got
   *dissolved*: see `docs/language/research/2026-07-09-stateful-scan-dissolved.md`.)
4. Only then does anyone discuss spelling.

If you believe a capability is missing, the contribution is a **research
entry** (path 1), not a grammar patch. Fifty problems quietly asking for the
same thing is evidence; one problem loudly asking is a mood — see Law 9 in
`docs/language/philosophy/style-laws.md`.

## Orientation

- `CLAUDE.md` — the operating rules, including for AI-assisted contributions.
- `docs/language/LANGUAGE.md`, `ANTI_GOALS.md` — what Rune is and refuses to be.
- `docs/language/DATA_MODEL.md` — what each step consumes and produces.
- `docs/language/atlas/algorithm-atlas.md` — every problem studied so far.
- `python -m rune.cli` — `run`, `demo`, `proofs`, `verify`, `stats`, `mine`.
