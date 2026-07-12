"""The "proves" engine for "AI proposes, Rune proves".

An LLM (or a human) proposes a Rune program. This module is the deterministic
source of truth that either certifies it or rejects it with a precise,
machine-checkable reason -- catching hallucinated syntax and wrong claimed
outputs without any of the LLM's confidence. No model, no API key: the
verification is pure Rune.
"""

from dataclasses import dataclass, field
from typing import Any, List

from rune.optimizer import optimize
from rune.parser import parse_program
from rune.runner import CountedBucket, run_program


@dataclass(frozen=True)
class VerificationResult:
    status: str  # "verified" | "rejected" | "parsed_only"
    stage: str  # parse | execute | optimizer_equivalence | expected | ok
    reason: str
    algorithm_choices: List[str] = field(default_factory=list)
    result: Any = None

    @property
    def ok(self) -> bool:
        return self.status == "verified"


def _normalize(value):
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, CountedBucket):
        return (value.key, value.count)
    return value


def verify_program(source, test_input=None, expected=None) -> VerificationResult:
    # Stage 1 -- PARSE. Deterministically rejects anything that isn't real
    # Rune (unknown keywords, malformed lines). This is the first wall against
    # a confidently-wrong LLM proposal.
    try:
        graph = parse_program(source)
    except Exception as e:
        return VerificationResult("rejected", "parse", f"does not parse: {e}")

    optimized, explanations = optimize(graph.steps)
    choices = [f"{e.after}  ({e.reason})" for e in explanations]

    if test_input is None:
        return VerificationResult(
            "parsed_only", "parse",
            "parses and optimizes cleanly; provide test_input for a runtime proof.",
            algorithm_choices=choices,
        )

    # Stage 2 -- EXECUTE the naive (unoptimized) plan.
    try:
        naive = run_program(graph.steps, test_input)
    except Exception as e:
        return VerificationResult("rejected", "execute", f"failed to run: {e}", choices)

    # Stage 3 -- OPTIMIZER EQUIVALENCE. The optimized plan must produce the
    # exact same result. This is the core proof: the compiler's algorithm
    # choice is certified to preserve the answer, not merely assumed to.
    try:
        opt = run_program(optimized, test_input)
    except Exception as e:
        return VerificationResult(
            "rejected", "optimizer_equivalence", f"optimized plan failed to run: {e}", choices
        )
    if _normalize(naive) != _normalize(opt):
        return VerificationResult(
            "rejected", "optimizer_equivalence",
            f"optimized result {opt} != naive result {naive}", choices,
        )

    # Stage 4 -- EXPECTED. If a claimed output was given, it must match.
    if expected is not None and _normalize(naive) != _normalize(expected):
        return VerificationResult(
            "rejected", "expected", f"produced {naive}, expected {expected}", choices, result=naive
        )

    detail = "parsed, optimized, and the optimized plan provably matches the naive result"
    if expected is not None:
        detail += " and the claimed output"
    return VerificationResult("verified", "ok", detail, algorithm_choices=choices, result=naive)


# --- "AI proposes, Rune proves" demonstration --------------------------------

_CASES = [
    (
        "a correct proposal",
        "MAXIMIZE SUM OVER CONTIGUOUS nums",
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        6,
    ),
    (
        "a hallucinated proposal (keyword that doesn't exist)",
        "FILTER nums WHERE age > 18",
        [1, 2, 3],
        None,
    ),
    (
        "a plausible proposal with a WRONG claimed answer",
        "MAXIMIZE SUM OVER CONTIGUOUS nums",
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        99,
    ),
]


def format_verification_demo():
    lines = [
        "AI proposes, Rune proves.",
        "An LLM emits a Rune program (with confidence). Rune -- deterministically,",
        "no model involved -- certifies it or rejects it with a specific reason.",
        "",
    ]
    for label, source, test_input, expected in _CASES:
        r = verify_program(source, test_input=test_input, expected=expected)
        verdict = "VERIFIED" if r.ok else "REJECTED"
        lines.append(f"[{verdict}] {label}")
        lines.append(f"   proposed: {source.splitlines()[0]}"
                     + (" ..." if "\n" in source else ""))
        if r.ok:
            lines.append(f"   result:   {r.result}")
            for c in r.algorithm_choices:
                lines.append(f"   chose:    {c.split('  (')[0]}")
        else:
            lines.append(f"   rejected at [{r.stage}]: {r.reason}")
        lines.append("")
    lines.append("The LLM can be wrong. Rune cannot silently pass a wrong program --")
    lines.append("that's the point. The AI proposes; the compiler is the source of truth.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_verification_demo())
