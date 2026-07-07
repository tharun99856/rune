# Research journal

One problem at a time. Not a batch. The ritual, in order:

1. **Solve it in plain English first.** No Rune, no keywords in mind. Just
   how you'd explain the solution to another person.
2. **Translate that to today's Rune** (`docs/language/grammar/current.md`).
   If a plausible attempt exists, run it through the real parser and record
   whether it's `[verified]` (actually run) or, if no plausible attempt even
   exists, say so honestly rather than inventing a strawman to fail.
3. **If it doesn't work, don't invent syntax.** Log the wanted capability in
   `docs/language/research/LANGUAGE_GAPS.md` — and check first whether it's
   genuinely new or additional evidence for something already tracked in
   `docs/language/primitives/candidates/`. Most of the time it's the latter;
   say so, don't manufacture novelty.

Each entry lives at `docs/language/research/YYYY-MM-DD-problem-slug.md` and
answers exactly these sections:

```
Problem
Current Rune
Pain points
Candidate capabilities
Rejected capabilities
Decision
Next experiment
```

This is a journal, not a reference table — `docs/language/atlas/algorithm-atlas.md`
is the reference table. The journal exists so six months from now the *why*
behind a decision is still legible, not just the decision itself.
