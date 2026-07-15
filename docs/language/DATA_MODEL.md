# The data model — what each step consumes and produces

The grammar (`grammar/current.md`) documents spelling. This documents the
*shapes* flowing through a pipeline. Like the grammar file, the runner
(`rune/runner.py`) is ground truth; if this file disagrees, this file is stale.

A program runs against exactly one input, supplied alongside it:

```
python -m rune.cli run program.rn --data data.json
```

## Input shapes

| JSON input | Becomes | Used by |
|---|---|---|
| `[1, 2, 2, 7]` | a sequence of values | `GROUP`, `ORDER`, `TAKE`, objectives |
| `"tree"` | a sequence of characters | same as a list |
| `{"a": [["b", 1]], "b": []}` | a graph: node → list of `[neighbor, weight]` edges | `EXPLORE` |

Identifiers in the program (`nums`, `text`, `graph`) name the input for the
reader; the runner binds whatever `--data` supplies. There is exactly one
input, so the names carry no lookup semantics — a deliberate simplification,
not an accident.

## Step signatures

| Step | Consumes | Produces |
|---|---|---|
| `GROUP <src> BY <key>` | sequence | buckets `(key, items)` — `value` keys each item by itself; any other key reads that attribute |
| `COUNT EACH <noun>` | buckets | counted buckets `(key, count)` |
| `ORDER BY <key> [ASC\|DESC]` | sequence or buckets | the same items, sorted |
| `TAKE <n>` | sequence or buckets | the first `n` |
| `EXPLORE <src> FROM <start>` | graph | `{node: distance}` for every reachable node |
| `EXPLORE <src> FROM <start> TO <target>` | graph | one distance, or nothing if unreachable |
| `MAXIMIZE\|MINIMIZE SUM OVER CONTIGUOUS <src>` | sequence of numbers | one number (nothing, if the sequence is empty) |

## Guarantees

- **Deterministic ties.** `ORDER` breaks ties by ascending bucket key, in both
  directions, for any orderable key type (numbers, characters, strings). The
  optimized `TOP_K` path and every backend must break ties identically — this
  is tested, because two backends disagreeing on which tied element survives
  is a correctness bug, not a rounding difference.
- **Data-driven strategy.** `EXPLORE` inspects the graph it is given:
  unweighted → BFS, weighted non-negative → Dijkstra, negative edges →
  Bellman-Ford. A reachable negative cycle is reported as an error
  ("shortest distances are undefined"), never an infinite loop.
- **Optimizations never change results.** Every rewrite (`TOP_K`, Kadane,
  TAKE-coalescing) is verified against the naive baseline it replaces —
  `python -m rune.cli proofs` demonstrates this end-to-end.

## Errors

Parse errors name the line, the offending text, and the expected form:

```
line 2: unrecognized step 'FILTER' -- every step starts with one of
COUNT, EXPLORE, GROUP, MAXIMIZE, MINIMIZE, ORDER, TAKE
```

Runtime errors (a negative cycle, an unsupported objective scope) raise
`ValueError` with the reason; `rune run` prints them as `runtime error: ...`
and exits nonzero.
