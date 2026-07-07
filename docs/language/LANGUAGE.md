# Language governance hierarchy

```
LANGUAGE.md            (this file -- governs everything below)
        │
        ▼
     Grammar            docs/language/grammar/current.md
        │
        ▼
     Parser             rune/lexer.py, rune/parser.py
        │
        ▼
       IR                rune/model.py (TransformationGraph)
        │
        ▼
    Optimizer            not yet built
        │
        ▼
     Backend             not yet built
```

**Nothing below may contradict anything above.** If the parser's
implementation becomes inconvenient, the parser changes — the grammar does
not bend to make implementation easier. If a future backend (LLVM or
otherwise) wants something the grammar doesn't express, the backend loses:
either it's built to honor the grammar as specified, or the grammar changes
through the same evidence-based process as any other change — never silently,
never to accommodate a backend's convenience.

This is why languages have specifications separate from their
implementation: without one, the implementation quietly *becomes* the spec,
and nobody notices until it's already happened.

## What sits at each layer today

- **Grammar** (`docs/language/grammar/current.md`): four verbs, frozen. The
  authoritative description of what a valid Rune program looks like.
- **Parser**: `rune/lexer.py` tokenizes, `rune/parser.py` builds the IR.
  Implements the grammar; does not extend it. If parsing something requires
  a capability the grammar doesn't describe, that's a grammar question,
  raised through the atlas — not a parser workaround.
- **IR**: `rune/model.py`'s `TransformationGraph` — an ordered list of typed
  steps (`Group`, `Count`, `Order`, `Take`). The surface language disappears
  here; nothing downstream should need to know the program was ever spelled
  `GROUP...BY`.
- **Optimizer / Backend**: not built. When they exist, the same rule applies
  — they consume the IR as specified, they don't reach back up and demand the
  grammar change to suit them.

## How to work on Rune without breaking this

The right instruction to a builder (human or AI) is never "build the next
version of Rune." It's scoped, and it names the constraint explicitly:

> Implement exactly the grammar described in `docs/language/grammar/current.md`.
> Do not add keywords. If you believe a new keyword is needed, stop and
> explain why instead of implementing it.

See `CLAUDE.md` at the repo root for the operational form of this rule.
