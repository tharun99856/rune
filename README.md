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

v0.1 grammar is frozen: four concepts, four keywords (`GROUP...BY`, `COUNT
EACH`, `ORDER BY...[ASC|DESC]`, `TAKE`), settled after testing against 100
real problems — see `docs/language/V0.1_FREEZE.md`. See
`docs/language/atlas/algorithm-atlas.md` for the evidence, and
`docs/language/primitives/candidates/` for capabilities still under
investigation — none yet promoted.

On top of that frozen surface, there's now a real pipeline: a parser, an
optimizer that rewrites `ORDER DESC + TAKE k` into a heap-based `TOP_K` and
explains why, and two backends behind a common interface — a reference
Python interpreter, and a real LLVM-compiled path (via Numba). Run it:

```
python -m rune.cli demo
```

Sample output, run for real, not simulated:

```
Rewrote: ORDER BY count DESC + TAKE 10
    ->   TOP_K(count, 10)
Reason:  ORDER immediately followed by TAKE recognized as top-k selection;
         a heap of size k avoids fully sorting the input.

Data: 500,000 items, domain [0, 1000)
Naive interpreter    (full sort):     68.31 ms
Optimized interpreter (heap top-k):   52.81 ms
Speedup from the optimizer alone: 1.29x (no compilation involved)

Numba-compiled (real LLVM, same TOP_K plan): 13.94 ms
Speedup over naive interpreted: 4.90x
```

Two numbers worth separating: **1.29x comes from the optimizer alone** —
recognizing intent and picking a better algorithm, no compilation involved.
**4.90x comes from compiling that same choice.** The first number is the
actual thesis (Rune reasons about intent, not just syntax); the second is
what a real backend adds once one exists. Neither is fabricated — both are
`assert`ed correct against the reference interpreter before being printed
(see `tests/test_demo.py`, and the tie-breaking bug this caught in
`docs/language/decisions/DECISIONS.md`).

`docs/language/primitives/` documents why each existing concept/keyword
exists; nothing else is implemented in the grammar yet by design.

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
