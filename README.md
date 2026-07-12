# Rune

**You describe the algorithm. The compiler chooses the implementation — and
proves it correct.**

Rune is a small language whose keywords are *intents* (group, order, take,
explore, maximize), not implementation details. You never pick a heap vs. a
sort, or BFS vs. Dijkstra. You state what you want; the optimizer recognizes
the shape of the problem and selects the algorithm, then verifies its choice
against the naive baseline.

```rune
GROUP nums BY value
COUNT EACH group
ORDER BY count DESC
TAKE 10
```

## The one thing that makes Rune Rune

It makes three *structurally different kinds* of optimization decision across
three unrelated algorithm families — and that's the whole point. Not one
clever rewrite; a repeatable principle.

```
python -m rune.cli proofs
```

```
1. TOP_K   -- decision made at COMPILE TIME, from the syntax pattern
   intent:   GROUP...COUNT...ORDER BY count DESC / TAKE 3
   decision: TOP_K(count, 3) -- a heap of size k, not a full sort
   verified: True

2. BFS vs Dijkstra -- decision made at RUNTIME, from the actual data
   intent:   EXPLORE graph FROM a   (same source both times)
   unweighted data -> BFS   weighted data -> Dijkstra
   verified: True

3. Kadane  -- decision made from the OBJECTIVE's structure
   intent:   MAXIMIZE SUM OVER CONTIGUOUS nums
   decision: KADANE(maximize) -- O(n) single pass, not O(n^2)
   verified: True
```

Every line is produced by the real optimizer and self-checked against the
naive baseline before printing — a `MISMATCH` shows instead of a
plausible-looking wrong number if anything ever disagrees. At scale the
Kadane rewrite is ~1090x (O(n²)→O(n)); `python -m rune.cli complexity` shows
real measured time and space.

## What Rune deliberately is NOT

Rune is **closed and provable, not general.** It expresses a specific slice of
algorithmic work extremely well; it does **not** try to solve every DSA
problem. Optimization over a *predicate-defined* space (much of classic DP —
Coin Change, Edit Distance, "subsets summing to X") is a documented, permanent
ceiling: expressing it needs arbitrary predicates, which would destroy the
exact property that lets the optimizer reason at all. That trade — narrow but
provable, over broad but redundant — is the founding decision
(`docs/language/decisions/DECISIONS.md`). A language that does everything
already exists; a language that proves your algorithm choice does not.

## Status

Six concepts, frozen and evidence-driven (`GROUP`, `COUNT`, `ORDER`, `TAKE`,
`EXPLORE`, `MAXIMIZE`/`MINIMIZE`) — each earned by testing against 100 real
problems, not decreed. Three optimizer proofs. Two execution backends behind a
common interface (a reference Python interpreter, and a real LLVM-compiled
path via Numba). ~76 tests. See `docs/language/V0.1_FREEZE.md` for how the
vocabulary was frozen and what got promoted since.

## Documentation

- `docs/language/grammar/current.md` — exactly what the parser accepts today.
- `docs/language/philosophy/style-laws.md` — the design laws, each derived
  from testing against real examples, not decreed up front.
- `docs/language/atlas/algorithm-atlas.md` — problems tested against the
  frozen grammar, and what each one reveals (or doesn't) about what's missing.
- `docs/language/primitives/` — why each existing concept/keyword exists;
  `docs/language/primitives/candidates/` — open capability questions, named
  after the capability, never a presumed keyword spelling.
- `docs/language/decisions/DECISIONS.md` — why things are the way they are.

## Running the tests

```
python -m pytest
```
