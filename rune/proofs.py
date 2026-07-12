"""The three-proofs showcase: Rune making three structurally different kinds
of optimizer decision across three unrelated algorithm families.

Every fact here is produced by the real optimizer/runner and self-verified
against a baseline before printing -- a MISMATCH line appears instead of a
plausible-looking wrong number if anything ever disagrees.
"""

from rune.model import Explore
from rune.optimizer import optimize
from rune.parser import parse_program
from rune.runner import explore_with_explanation, run_program, run_step


def _proof_top_k():
    lines = ["1. TOP_K -- decision made at COMPILE TIME, from the syntax pattern"]
    program = "GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 3"
    data = [5, 5, 5, 5, 2, 2, 2, 7, 7, 9, 9, 9, 9, 9]

    graph = parse_program(program)
    optimized, exps = optimize(graph.steps)
    naive_res = [(b.key, b.count) for b in run_program(graph.steps, data)]
    opt_res = [(b.key, b.count) for b in run_program(optimized, data)]

    lines.append("   intent:   GROUP...COUNT...ORDER BY count DESC / TAKE 3")
    lines.append(f"   decision: {exps[0].after} -- a heap of size k, not a full sort")
    lines.append(f"   verified: {naive_res == opt_res}"
                 + ("" if naive_res == opt_res else "   MISMATCH"))
    return "\n".join(lines)


def _proof_explore():
    lines = ["2. BFS vs Dijkstra -- decision made at RUNTIME, from the actual data"]
    unweighted = {"a": [("b", 1), ("c", 1)], "b": [("d", 1)], "c": [("d", 1)], "d": []}
    weighted = {"a": [("b", 5), ("c", 1)], "b": [("d", 1)], "c": [("b", 1), ("d", 10)], "d": []}
    step = Explore(source="graph", start="a", target=None)

    unw_res, unw_exp = explore_with_explanation(step, unweighted)
    w_res, w_exp = explore_with_explanation(step, weighted)

    # On the unweighted graph BFS is chosen; verify it agrees with Dijkstra
    # (so the cheaper pick is safe). On the weighted graph Dijkstra is chosen
    # (BFS would be wrong). Same intent, different algorithm, driven by data.
    from rune.runner import _bfs, _dijkstra

    unw_ok = unw_exp.strategy == "BFS" and _bfs(unweighted, "a") == _dijkstra(unweighted, "a")
    w_ok = w_exp.strategy == "Dijkstra" and w_res != _bfs(weighted, "a")

    lines.append("   intent:   EXPLORE graph FROM a   (same source both times)")
    lines.append(f"   unweighted data -> {unw_exp.strategy}   weighted data -> {w_exp.strategy}")
    lines.append(f"   verified: {unw_ok and w_ok}"
                 + ("" if unw_ok and w_ok else "   MISMATCH"))
    return "\n".join(lines)


def _proof_kadane():
    lines = ["3. Kadane -- decision made from the OBJECTIVE's structure"]
    program = "MAXIMIZE SUM OVER CONTIGUOUS nums"
    data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

    graph = parse_program(program)
    optimized, exps = optimize(graph.steps)
    naive_res = run_program(graph.steps, data)
    opt_res = run_program(optimized, data)

    lines.append("   intent:   MAXIMIZE SUM OVER CONTIGUOUS nums")
    lines.append(f"   decision: {exps[0].after} -- optimal substructure, one pass not O(n^2)")
    lines.append(f"   verified: {naive_res == opt_res}"
                 + ("" if naive_res == opt_res else "   MISMATCH"))
    return "\n".join(lines)


def format_proofs_report():
    header = [
        "Rune: three optimizer decisions, three different kinds of reasoning.",
        "You state intent. Rune picks the algorithm -- and proves it correct against",
        "the naive baseline. The point isn't any one speedup; it's that the SAME",
        "principle holds across three unrelated algorithm families.",
        "",
    ]
    return "\n\n".join(["\n".join(header), _proof_top_k(), _proof_explore(), _proof_kadane()])


if __name__ == "__main__":
    print(format_proofs_report())
