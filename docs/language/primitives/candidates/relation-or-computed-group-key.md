# Candidate: relation between pairs (naming undecided — NOT "MATCH"/"JOIN")

**Status:** Under investigation. One data point, two competing hypotheses.

**Why is this being considered?**
Two Sum needs to relate pairs of elements (does some other element's value
equal target - this value?), which no current concept expresses.

**Problems requiring it:** 012 (Two Sum) only.

**Two live hypotheses — deliberately not resolved yet:**
1. A new relation/join primitive, operating across pairs of elements.
2. Extending `GROUP` to accept a *computed* key (e.g. `GROUP nums BY (target - value)`) rather than only a literal field — which might get most of the way there without any new concept at all.

**Why this matters:** hypothesis 2 would mean the language doesn't need a new
primitive here, just a more expressive existing one. That's a materially
different, cheaper outcome than hypothesis 1, and shouldn't be skipped past.

**Alternative syntaxes considered:** none yet — resolve the hypothesis before
drafting syntax.

**Rejected designs:** None yet.

**Future work:** Try expressing Two Sum (and a few more relation-shaped
problems — e.g. finding pairs, triplets) under hypothesis 2 concretely before
assuming hypothesis 1 is needed. Only one data point exists; don't decide on
one data point.
