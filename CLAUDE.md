# Instructions for Claude working in this repository

Read `docs/language/LANGUAGE.md`, `docs/language/philosophy/style-laws.md`,
and `docs/language/ANTI_GOALS.md` before touching the grammar, parser, or IR.
This file is the operational summary; those are the actual authority.

## The one rule that matters most

**Do not add a keyword to the grammar because a problem seems to need one.**

The grammar (`docs/language/grammar/current.md`) is frozen. It changes only
after `docs/language/atlas/algorithm-atlas.md` shows repeated, independent,
*verified-against-the-real-parser* pressure for a specific missing
capability — not because it seems missing, sounds elegant, or would make one
example read more naturally.

If you believe a new keyword or grammar change is needed:

1. **Stop. Do not implement it.**
2. Check `docs/language/primitives/candidates/` — is this capability already
   being tracked? If not, add a candidate page named after the *capability*,
   never a presumed keyword spelling (`sequence-filter-with-fallback.md`,
   not `WHERE.md`).
3. Test the claim against the actual running parser (`rune.parser.parse_program`),
   not by reasoning about it in the abstract. Mark findings `[verified]` or
   `[reasoned]` honestly — don't blur the two.
4. Apply the four-question order, in this order, every time:
   - Can the current grammar already express this (even awkwardly)?
   - Can it be a compiler-side rewrite of something already expressible?
   - Can it be syntax sugar over existing verbs?
   - Only then: is a genuinely new capability needed — and even so, name the
     *capability*, not a keyword. Syntax comes last, after the capability is
     confirmed by multiple independent problems, not the first one that fails.
5. Explain your finding to the user. Let them decide whether to promote it.
   Do not implement the new keyword yourself, even if the case looks strong.

**Bad instruction to follow literally:** "Build the next version of Rune."
**Good instruction:** "Implement exactly the grammar in
`docs/language/grammar/current.md`. Do not add keywords. If you believe one
is needed, stop and explain why instead of implementing it."

If a user's request reads like the first kind, ask which specific,
already-scoped piece they mean rather than inferring the widest possible
interpretation.

## Everything else

- TDD for all parser/IR/optimizer/backend work: failing test first, minimal
  code, verify green, then commit. Same discipline as the sibling
  verified-intent-ir project.
- Every `.rn` file under `docs/language/examples/` must keep parsing after
  any change — that's what `tests/test_examples.py` enforces. A grammar or
  parser change that breaks an existing example is a regression, not a
  tradeoff to wave through.
- Rune is a separate project from verified-intent-ir. Reuse discipline
  (TDD, structured decisions, ADR logging), never code, never scope.
- Rune's identity is not "the AI language" — see
  `docs/language/decisions/DECISIONS.md`. Don't frame features that way.
