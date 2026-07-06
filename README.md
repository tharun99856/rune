# Rune

A language whose primitives correspond to algorithmic reasoning, not
implementation details.

```rune
GROUP nums BY value
COUNT EACH group
ORDER BY count DESC
TAKE 10
```

Rune is not pseudocode with prettier keywords, and it is not "the AI
language" — the eventual AI recovery layer is one feature of it, not its
identity. See `docs/language/decisions/DECISIONS.md`.

## Status

Early. A lexer and parser exist, producing a transformation graph — no
optimizer, no rewrite engine, no LLVM backend yet. The grammar is
deliberately frozen at four verbs (`GROUP...BY`, `COUNT EACH`, `ORDER
BY...[ASC|DESC]`, `TAKE`) until real problems, tested against the actual
parser, justify adding more. See `docs/language/atlas/algorithm-atlas.md`
for the evidence being collected, and `docs/language/primitives/candidates/`
for capabilities under investigation — none yet promoted.

## Documentation

- `docs/language/grammar/current.md` — exactly what the parser accepts today.
- `docs/language/philosophy/style-laws.md` — the design laws, each derived
  from testing against real examples, not decreed up front.
- `docs/language/atlas/algorithm-atlas.md` — problems tested against the
  frozen grammar, and what each one reveals (or doesn't) about what's missing.
- `docs/language/primitives/` — why each existing verb exists;
  `docs/language/primitives/candidates/` — open capability questions, named
  after the capability, never a presumed keyword spelling.
- `docs/language/decisions/DECISIONS.md` — why things are the way they are.

## Running the tests

```
python -m pytest
```
