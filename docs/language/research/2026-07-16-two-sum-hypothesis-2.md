## Problem

Not a new algorithm — the experiment the relation candidate's Future Work
prescribes: attempt Two Sum (ledger 012) under **hypothesis 2** (a *computed*
GROUP key) against the real parser, then attempt the same phrasing for Daily
Temperatures' next-greater relation and record where each breaks.

## Current Rune

`[verified]`, all four attempts run through `rune.parser.parse_program`:

```
GROUP nums BY (target - value)   -> mis-parsed: Group(key='(target'), rest DROPPED
GROUP nums BY target-value       -> "parses": key is the opaque IDENT 'target-value'
GROUP nums BY value extra junk   -> parsed, trailing tokens silently dropped
TAKE 5 please                    -> parsed as TAKE 5
```

Hypothesis 2 is **not expressible today** — but the experiment's real finding
is *how* it fails. The parser didn't reject the computed key; it silently
mangled it. And the control lines showed this was general: **every step
silently ignored trailing tokens.**

## Pain points

The silent tolerance was a hole in the project's central claim. "AI proposes,
Rune proves" depends on malformed proposals being REJECTED — but a
hallucinated proposal with trailing junk (`TAKE 5 please`) sailed through
parse and could come back VERIFIED. A verifier that ignores parts of what it
verifies isn't proving what it claims to prove.

**Fixed same day, TDD:** `_parse_line` now validates each step's exact shape —
arity, inner keywords (`EACH`, `BY`, `FROM`/`TO`, `SUM OVER CONTIGUOUS`,
`ASC|DESC`) — so a line either matches the documented form or names the line
and the expected form. All four lines above now reject. Zero grammar change:
nothing that ever *meant* anything stopped parsing; garbage stopped being
quietly tolerated. (`ORDER BY count BANANA` previously parsed as *ascending*,
silently. It no longer parses.)

## Candidate capabilities

For the relation candidate, the experiment sharpens both hypotheses without
resolving them:

- **Hypothesis 2 (computed GROUP key) is itself a grammar question.** There is
  no spelling of a computed key inside the frozen vocabulary — `(target -
  value)` isn't tokens the grammar knows, and `target-value` is just an opaque
  identifier the runner would treat as an attribute name. So hypothesis 2 is
  not "cheaper than a new primitive, available today"; it's a smaller grammar
  extension vs. a bigger one. The candidate page's cost comparison was framed
  optimistically and is now corrected.
- **Next-greater can't be phrased as any key even in principle** `[reasoned]`:
  a grouping key is a function of the element alone, but "nearest LATER
  element greater than me" depends on *other elements and their positions* —
  no per-element key computes it. The value-vs-positional split from the
  Daily Temperatures entry stands, now with a mechanical argument.

## Rejected capabilities

Splitting the candidate today. Two data points still — the tension is real
but recorded; splitting needs a third relation-shaped problem landing clearly
on one side. Also rejected: designing computed-key syntax now (capability
before syntax, and the capability count is 2).

## Decision

No grammar change. Parser strictness fixed (implementation, TDD, examples all
still parse). Relation candidate page updated: hypothesis 2's true cost
corrected, mechanical argument recorded. The C++ backend's negative-weight
refusal landed alongside (same session, same "backends must not silently
disagree" principle).

## Outcome

🧩 Evidence for the existing `relation-or-computed-group-key` candidate — and
a concrete byproduct: the experiment caught a verifier-integrity bug the
project's whole pitch depended on. Running the experiment *was* the discipline
working; reasoning about hypothesis 2 in the abstract would have concluded
"needs new syntax" and missed the silent-tolerance hole entirely.

## Next experiment

A third relation-shaped problem (3Sum, ledger 050, is already tagged) to test
which side of the value/positional line it lands on. If value: hypothesis 2
gains its second point and the split question gets real. Separately: the
ledger-wide objective-evidence sweep the dissolution prescribed remains open.
