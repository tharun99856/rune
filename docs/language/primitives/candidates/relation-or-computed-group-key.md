# Candidate: relation between pairs (naming undecided — NOT "MATCH"/"JOIN")

**Status:** Under investigation. Two data points, two hypotheses — with first
evidence (2026-07-16) that the hypotheses may be *sub-shapes*, not rivals.

**Why is this being considered?**
Two Sum needs to relate pairs of elements (does some other element's value
equal target - this value?), which no current concept expresses.

**Problems requiring it:** 012 (Two Sum); 047 (Daily Temperatures — re-filed
here by intent in the 2026-07-09 Stateful Scan dissolution: a
next-greater/span relation, closer to Two Sum than to Valid Parentheses;
journaled 2026-07-16).

**Two live hypotheses — deliberately not resolved yet:**
1. A new relation/join primitive, operating across pairs of elements.
2. Extending `GROUP` to accept a *computed* key (e.g. `GROUP nums BY (target - value)`) rather than only a literal field — which might get most of the way there without any new concept at all.

**Why this matters:** hypothesis 2 would mean the language doesn't need a new
primitive here, just a more expressive existing one. That's a materially
different, cheaper outcome than hypothesis 1, and shouldn't be skipped past.

**Hypothesis tension (new, 2026-07-16):** Two Sum relates *values* — a
computed key can plausibly express it. Daily Temperatures relates *positions
with a direction* ("nearest LATER element greater than me") — relative to
each element, ordered, asymmetric: not obviously any key a grouping could
compute. If that holds up, the two hypotheses cover different relation
sub-shapes (value vs. positional), and this candidate may need to split
before its count means anything. Daily Temperatures also needs *per-element
output* — a separable absence (see the 2026-07-16 entry) shared with
Product-of-Array-Except-Self-shaped problems and tracked by no candidate yet.

**Alternative syntaxes considered:** none yet — resolve the hypothesis before
drafting syntax.

**Rejected designs:** None yet.

**Future work:** Try expressing Two Sum under hypothesis 2 concretely and run
it through the real parser — then attempt the same phrasing for
Daily Temperatures' next-greater relation and record *where* it breaks. If
hypothesis 2 handles value relations but cannot state positional ones, split
this candidate along that line before gathering further count. Two data
points; still nowhere near a promotion decision.
