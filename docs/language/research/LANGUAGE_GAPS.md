# Language Gaps

A running, numbered log. Each entry is deliberately short — full reasoning
lives in the linked research journal entry. A gap number does **not** mean
"approved for a keyword" — it means "logged, pending enough independent
evidence." Most entries should turn out to be additional evidence for an
existing candidate, not a brand new one; say so explicitly when that's true.

---

### Gap #1 — NOT a new gap (reinforcing evidence)

**Wanted capability:** Stack-based state during a left-to-right scan
(remember the most recent unmatched item, check against it, discard when
matched).

**Reason:** `GROUP`/`COUNT`/`ORDER`/`TAKE` have no notion of a scan carrying
forward mutable state at all, let alone a stack.

**Status:** This is the 7th data point for the existing
`docs/language/primitives/candidates/stateful-scan-or-recurrence.md`
candidate — not a new bucket. It sharpens that candidate's already-open
question (does "stateful scan" cover one shape or several distinct
state-retention needs — rolling scalar, full table, and now a stack?)
rather than resolving it.

**See:** `docs/language/research/2026-07-07-valid-parentheses.md`

---

## Tally (kept in sync with docs/language/atlas/algorithm-atlas.md)

This log and the atlas's "Grammar Pressure" section track the same
underlying evidence and should never be allowed to diverge into two
disconnected counts. As of this entry, no change to the atlas tally — Gap #1
adds a sub-case to an existing count, not a new row.
