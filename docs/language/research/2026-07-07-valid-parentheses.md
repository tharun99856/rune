## Problem

Valid Parentheses. Given a string of brackets, determine whether it's
balanced and properly nested.

**Solved in English first, no Rune in mind:**

> Scan the string left to right. When you see an opening bracket, remember
> it. When you see a closing bracket, check that it matches the most
> recently remembered opening bracket, and forget that one. If at any point
> they don't match, or there's nothing remembered to match against, it's
> invalid. At the end, valid only if nothing is left unmatched.

## Current Rune

No plausible attempt exists. `GROUP`, `COUNT`, `ORDER`, `TAKE` all operate on
a flat collection as a whole (partition it, aggregate it, rank it, bound it)
— none of them have any notion of "the most recently remembered thing," which
is the entire mechanism this problem needs. Unlike earlier research entries,
there's no near-miss snippet worth actually running through the parser to
prove it fails — nothing in the grammar even superficially resembles an
attempt. Saying so plainly here rather than writing a strawman line just to
generate a `[verified] BREAKS` result.

## Pain points

The English solution's core mechanism — "remember the most recent unmatched
thing, check new input against it, discard it once matched" — is a stack.
State isn't a rolling scalar (Kadane's) and isn't a full table (LCS). It's a
*growing and shrinking* structure that the scan itself maintains.

## Candidate capabilities

**Not a new gap.** This is the 7th data point for the existing
`stateful-scan-or-recurrence` candidate
(`docs/language/primitives/candidates/stateful-scan-or-recurrence.md`), and
it sharpens the open sub-question already flagged there rather than
resolving it: that candidate now has at least three distinct state shapes
behind one name — O(1) rolling state (Kadane's, Climbing Stairs), a full
table (Coin Change, LCS), and now a stack (this problem). That's evidence
the candidate may be genuinely over-aggregated, not evidence it should be
promoted as-is.

## Rejected capabilities

Considered treating this as its own new candidate ("stack-based matching").
Rejected for now — one data point isn't enough to justify a fourth
bucket when the real open question is whether the *existing* bucket of six
is already too coarse. Splitting further before that's resolved would make
the over-aggregation problem worse, not better.

## Decision

No grammar change. Updated `stateful-scan-or-recurrence.md` with this data
point and the state-shape distinction. Logged in `LANGUAGE_GAPS.md` as
reinforcing evidence, not a new gap.

## Next experiment

A second stack-shaped problem (e.g. Daily Temperatures, or Largest Rectangle
in Histogram) would be a better next step than another Kadane's-shaped
problem — it would test whether "stack state" recurs independently, which is
exactly the kind of independent confirmation the over-aggregation question
needs before it can be resolved either way.
