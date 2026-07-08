from rune.complexity import measure_top_k_complexity
from rune.optimizer import optimize
from rune.parser import parse_program

_PROGRAM = "GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 10"


def format_explain_report(top_k_kwargs=None):
    """The consolidated "why did Rune do that" view for the TOP_K rewrite --
    presentation only. Every fact here comes from optimize() (the actual
    rewrite decision) and measure_top_k_complexity() (the actual measured
    numbers); nothing is computed or estimated here that isn't already
    proven correct elsewhere.
    """
    graph = parse_program(_PROGRAM)
    _optimized_steps, explanations = optimize(graph.steps)
    exp = explanations[0]

    metrics = measure_top_k_complexity(**(top_k_kwargs or {}))

    lines = []
    lines.append("Rune source:")
    for line in _PROGRAM.splitlines():
        lines.append(f"  {line}")
    lines.append("")
    lines.append("Rewrite applied")
    lines.append(f"  Before: {exp.before}")
    lines.append(f"  After:  {exp.after}")
    lines.append("")
    lines.append("Reason")
    lines.append(f"  {exp.reason}")
    lines.append("")
    lines.append("Complexity (this step only -- GROUP+COUNT's O(n) frequency table")
    lines.append("is built either way and isn't affected by this rewrite)")
    lines.append(f"  Before: O(n log n) time, +O(n) incremental space")
    lines.append(f"  After:  O(n log k) time, +O(k) incremental space")
    lines.append("")
    lines.append(f"Measured (n={metrics['n']:,}, k={metrics['k']})")
    lines.append(
        f"  Time:   {metrics['naive_time_ms']:.2f} ms -> {metrics['optimized_time_ms']:.2f} ms "
        f"({metrics['naive_time_ms'] / metrics['optimized_time_ms']:.2f}x)"
    )
    lines.append(
        f"  Space:  {metrics['naive_peak_kb']:,.1f} KB -> {metrics['optimized_peak_kb']:,.1f} KB "
        f"({metrics['naive_peak_kb'] / metrics['optimized_peak_kb']:.2f}x)"
    )
    lines.append(f"  Correctness verified: {metrics['correct']}")
    lines.append("")
    lines.append("The rewrite is the contribution. The benchmark is evidence for it,")
    lines.append("not the headline -- next run, on different data, the ratio will be")
    lines.append("a different number. That Rune picked the right algorithm because it")
    lines.append("recognized the pattern is the part that doesn't change.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_explain_report())
