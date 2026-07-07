# Research journal

One problem at a time. Not a batch. The ritual, in order:

1. **Solve it in plain English first.** No Rune, no keywords in mind. Just
   how you'd explain the solution to another person.
2. **Translate that to today's Rune** (`docs/language/grammar/current.md`).
   If a plausible attempt exists, run it through the real parser and record
   whether it's `[verified]` (actually run) or, if no plausible attempt even
   exists, say so honestly rather than inventing a strawman to fail.
3. **Every entry ends with exactly one outcome — never invent syntax to force one:**
   - ✅ Already expressible
   - 🔁 Expressible via a future compiler rewrite
   - ✨ Needs syntax sugar only (composes today, just reads badly)
   - 🧩 New capability candidate — and say explicitly whether it's a *new*
     candidate or additional evidence for an existing one in
     `docs/language/primitives/candidates/`. Most of the time it's the
     latter; don't manufacture novelty.
   - ❌ Wrong abstraction — the pipeline model itself doesn't fit this
     *category* of problem, not just this one problem. This is the rarest
     and most important outcome. It is never declared from a single
     problem — see `docs/language/research/ABSTRACTION_QUESTIONS.md` for
     what evidence threshold triggers it.

Each entry lives at `docs/language/research/YYYY-MM-DD-problem-slug.md` and
answers exactly these sections:

```
Problem
Current Rune
Pain points
Candidate capabilities
Rejected capabilities
Decision
Outcome            (one of: ✅ 🔁 ✨ 🧩 ❌)
Next experiment
```

This is a journal, not a reference table — `docs/language/atlas/algorithm-atlas.md`
is the reference table. The journal exists so six months from now the *why*
behind a decision is still legible, not just the decision itself.

## The governing rule

**Never design Rune for tomorrow's problem. Design Rune for yesterday's 50
problems.** If today's problem screams for a new concept, that's not evidence —
it's a mood. If fifty independently-solved problems quietly ask for the same
capability, that's evidence. See Law 9 in
`docs/language/philosophy/style-laws.md`.

**An investigation (splitting/merging a candidate) is capped, not open-ended.**
Collect evidence, split or merge, write the verdict, move on — this should
take about an hour, not become its own research project. `python -m
rune.cli mine` exists specifically to shorten this loop: it flags which
concept is under the most pressure so the next investigation doesn't start
from "what should I even look at."
