# Anti-goals

Things Rune will never become. Languages die from feature creep, not from
having too few features — this list exists to make that an explicit, checkable
constraint, not a vague intention.

**Rune is not:**

- **A replacement for C++ or a systems language.** Once a backend exists,
  instruction-level performance is LLVM's job, not Rune's. See
  `docs/language/decisions/DECISIONS.md`.
- **A general natural-language programming system.** No free-form English
  parsing. "Find the shortest safe route" is a stated long-term ambition, not
  a v1 target — realizing it in general is algorithm synthesis, a much harder
  problem than compiling a closed grammar.
- **A Python wrapper or a pseudocode formatter.** Concepts express intent,
  not Python idioms with different spelling. See Law 4 and Law 7 in
  `docs/language/philosophy/style-laws.md`.
- **A query language competing with SQL.** Rune borrows relational algebra's
  compositional discipline (small concept set, provable equivalences) as a
  pattern, not as a target to out-feature.
- **An AI coding assistant, or "the AI language."** The eventual recovery
  layer is one feature of Rune, not its identity. Explicitly decided — see
  `docs/language/decisions/DECISIONS.md`.
- **A dumping ground for every named algorithm.** No `DIJKSTRA`, `TARJAN`,
  `KMP` as primitives, ever — goal-level names only (`SHORTEST_PATH`, not the
  algorithm that implements it), and even those must earn their place through
  atlas pressure, not familiarity.
- **A place where syntax gets added because it "feels missing."** The
  recurring failure mode this whole project exists to prevent. A keyword is
  earned by repeated, independent, verified pressure from real problems — see
  the four-question discipline in `docs/language/atlas/algorithm-atlas.md`
  and Law 8.

If a proposed feature doesn't clearly fail this list, that's necessary but
not sufficient — it still has to clear the atlas discipline before it enters
the grammar.
