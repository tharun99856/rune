## Problem

Finish the Stateful Scan investigation. The 2026-07-08 entry split its
problems by *mechanism* (Recurrence / Stack / Pointer) and stopped at "3
clusters, promotion undecided." This entry does the thing that was actually
missing: re-classify all 34 by **intent** — what the human wants — because
Rune is an intent language, and a candidate concept has to be an intent, not
an implementation shape.

## The re-classification (all 34, by intent not mechanism)

| Intent family | Problems | Count |
|---|---|---|
| Optimize an objective (max/min) over a combinatorial space | Kadane's, Max Product Subarray, House Robber, Min Cost Climbing Stairs, Coin Change, LIS, LCS, Edit Distance, Longest Palindromic Substring, Largest Rectangle | 10 |
| Count / decide existence over a combinatorial space | Climbing Stairs, Unique Paths, Decode Ways, Partition Equal Subset, Word Break | 5 |
| Restructure / traverse a linked sequence | Reverse List, Merge Two Lists, Add Two Numbers, Reorder List, Copy w/ Random Ptr, Cycle II | 6 |
| Consolidate / measure overlapping intervals | Merge Intervals, Non-overlapping Intervals, Insert Interval, Meeting Rooms | 4 |
| Evaluate / validate a nested expression | Valid Parentheses, Evaluate RPN, Basic Calculator | 3 |
| Next-greater / span relation | Daily Temperatures | 1 |
| Reachability / feasible-start search | Jump Game, Gas Station | 2 |
| Per-element transform | Product of Array Except Self, Counting Bits, Sum of Two Integers | 3 |

**That's at least 8 unrelated intent families under one tag.** The mechanism
clustering from last time cross-cuts them badly:

- *Stack* mechanism holds Valid Parentheses (validate-nesting), Daily
  Temperatures (next-greater-relation, closer to Two Sum than to Valid
  Parentheses), and Largest Rectangle (maximize-area). Three different
  intents, one data structure.
- *Recurrence* mechanism holds Kadane's (maximize) but also Jump Game
  (reachability) and Merge Intervals (consolidate) — the 2026-07-08 entry
  itself noted Jump Game "looks like reachability, collapses to a scan under
  a monotonicity property." Its *intent* is reachability; the scan is how.
- Add Two Numbers spans two mechanisms at once (rolling carry + list
  pointers), already flagged last time.

## The decisive argument (not just the cross-cut)

The cross-cut alone could be dismissed as "then it's 8 concepts, fine." It
isn't, and here's the clean reason:

**A single `SCAN`/`FOLD` concept general enough to cover all 34 would have to
take arbitrary per-step logic** — Kadane's "add, reset if negative" is a
different step function from Valid Parentheses' "push opener / pop-and-match
closer" from Reverse List's "rewire next pointer." That is exactly what
`scanl :: (b -> a -> b) -> b -> [a] -> [b]` is in functional languages: a
primitive parameterized by a **user-supplied function**.

A user-supplied step function is the one thing Rune's founding constraint
forbids (the closed-vocabulary / no-arbitrary-lambda rule inherited from
verified-intent-ir — the moment you allow it, the optimizer can no longer
know what a program does, and provable reasoning collapses). So:

- As **one** concept, Stateful Scan requires the forbidden escape hatch.
- As **many** concepts, its members' intents are already covered by other
  concepts (reachability = EXPLORE) or point at concepts that don't exist yet
  (objectives — see below).

Either way, **"Stateful Scan" is not a Rune concept.** It's an implementation
shape — "a pass that maintains state" — that a *Python* programmer sees as
one thing because Python expresses all of them with `for` + a mutable
variable. That's a fact about Python, not about intent.

## What the tag was actually measuring

`rune mine` flagged Stateful Scan at 34 because it counts *pattern* frequency
and 34 problems share this implementation pattern. The tool did its job — it
said "go read these," and reading them is what produced this finding. The
34 was never 34 votes for one concept; it was 34 problems whose Python
solutions rhyme. The tool's own output already says "a count, not a verdict";
this is the verdict.

## The real signal underneath

The largest genuine thread — 15 of 34 (optimize + count/exists) — is problems
that state an **objective over a space**: MAXIMIZE sum, MINIMIZE edits, COUNT
paths, EXISTS a partition. No current concept expresses an objective. That's
a real candidate direction, opened as its own candidate
(`docs/language/primitives/candidates/objective-over-scope.md`), with its own
evidence to gather — not promoted here, just surfaced honestly. DP is the
*technique* the compiler would pick to satisfy such an objective, the same
way a heap is the technique it picks for ORDER+TAKE — implementation, not
language.

## Decision

- Stateful Scan: **dissolved as a candidate concept.** Not 1, not 3 — not a
  concept. See `stateful-scan-or-recurrence.md` (status updated).
- Ledger tags left as-is deliberately: they are honest *mechanism*
  observations, and wholesale re-tagging to intent now would mean inventing
  objective-concept tags before those concepts exist — the exact
  fill-the-table guessing this project avoids. The full intent re-tag is a
  deliberate future pass, once/if objective concepts are defined.
- Opened `objective-over-scope.md` as the real candidate this surfaced.

## Outcome

❌ for the candidate as posed — but a *productive* negative result: the
highest-"pressure" candidate resolves to a Python-shaped mirage, which is
exactly the failure mode the intent-over-implementation thesis predicts, and
the discipline caught it before it became a keyword. The genuine signal
(objectives) is now tracked where it belongs.

## Next experiment

Gather evidence for `objective-over-scope`: across the ledger (not just the
Stateful Scan rows), how many problems state a max/min/count/exists objective
that no current concept expresses? If it's broad, that — not "scan" — is the
next concept worth a promotion decision.
