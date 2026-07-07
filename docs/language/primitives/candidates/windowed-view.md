# Candidate: windowed view (naming undecided — NOT "WINDOW")

**Status:** Under investigation. Two confirmed data points, one possible third.

**Why is this being considered?**
A bounded, moving view over a sequence — fixed size or expanding/contracting
— cannot be expressed with any current concept.

**Problems requiring it:** 013 (Sliding Window Maximum, fixed size), 014
(Longest Substring Without Repeating Characters, variable size).

**Possibly related:** 017 (Container With Most Water) needs two positions
converging from opposite ends — unresolved whether that's the same shape
(a window that shrinks from both ends) or a genuinely different one
(two-ended convergence). See `two-ended-convergence.md`.

**Alternative syntaxes considered:** none yet.

**Rejected designs:** None yet.

**Future work:** More fixed- and variable-window problems, plus a deliberate
attempt to express Container-With-Water both ways, before deciding whether
017 belongs here or is separate.
