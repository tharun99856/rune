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

**Status (updated 2026-07-09):** Logged at the time as a 7th data point for
the stateful-scan candidate. That candidate has since been **dissolved** —
it was an implementation shape, not an intent concept (see
`docs/language/research/2026-07-09-stateful-scan-dissolved.md`). Valid
Parentheses' actual *intent* is "validate a nested expression," unrelated to
the *intent* of the other problems that shared its stack mechanism. Kept here
as an honest record of a data point that pointed at a mirage — that's what
the log is for, not just the ones that panned out.

**See:** `docs/language/research/2026-07-07-valid-parentheses.md`,
then `docs/language/research/2026-07-09-stateful-scan-dissolved.md`

---

## Tally (kept in sync with docs/language/atlas/algorithm-atlas.md)

This log and the atlas's "Grammar Pressure" section track the same
underlying evidence and should never be allowed to diverge into two
disconnected counts. As of this entry, no change to the atlas tally — Gap #1
adds a sub-case to an existing count, not a new row.
