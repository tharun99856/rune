import random
import time
import tracemalloc

from rune.backends.interpreter_backend import InterpreterBackend
from rune.optimizer import optimize
from rune.parser import parse_program
from rune.runner import _bfs, _dijkstra

_PROGRAM = "GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 10"


def _pairs(buckets):
    return sorted((b.key, b.count) for b in buckets)


def measure_top_k_complexity(data_size=3_000_000, domain_size=2_000_000, seed=42):
    """Compares ORDER+TAKE (O(n log n) time, O(n) space) against the
    optimizer's TOP_K rewrite (O(n log k) time, O(k) space), isolated from
    the shared GROUP+COUNT cost that both paths pay identically -- measuring
    the whole pipeline instead of isolating this step hides the difference
    almost entirely (see docs/language/decisions/DECISIONS.md).
    """
    rng = random.Random(seed)
    data = [rng.randint(0, domain_size - 1) for _ in range(data_size)]

    graph = parse_program(_PROGRAM)
    optimized_steps, _ = optimize(graph.steps)
    backend = InterpreterBackend()

    grouped_and_counted = backend.run(graph.steps[:2], data)
    n = len(grouped_and_counted)

    naive_steps = graph.steps[2:]  # Order, Take
    topk_steps = optimized_steps[-1:]  # TopK

    t0 = time.perf_counter()
    naive_result = backend.run(naive_steps, grouped_and_counted)
    naive_time_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    optimized_result = backend.run(topk_steps, grouped_and_counted)
    optimized_time_ms = (time.perf_counter() - t0) * 1000

    tracemalloc.start()
    backend.run(naive_steps, grouped_and_counted)
    _, naive_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    backend.run(topk_steps, grouped_and_counted)
    _, optimized_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "n": n,
        "k": optimized_steps[-1].count,
        "correct": _pairs(naive_result) == _pairs(optimized_result),
        "naive_time_ms": naive_time_ms,
        "optimized_time_ms": optimized_time_ms,
        "naive_peak_kb": naive_peak / 1024,
        "optimized_peak_kb": optimized_peak / 1024,
    }


def measure_graph_complexity(num_nodes=200_000, edges_per_node=3, seed=42):
    """Compares BFS (O(V+E) time/space) against Dijkstra (O((V+E) log V)
    time, O(V+E) space) on an unweighted graph -- the case where the
    optimizer's runtime choice (BFS, since all weights are 1) is cheaper
    than always defaulting to the more general Dijkstra.
    """
    rng = random.Random(seed)
    graph = {i: [] for i in range(num_nodes)}
    for i in range(num_nodes):
        for _ in range(edges_per_node):
            j = rng.randint(0, num_nodes - 1)
            graph[i].append((j, 1))

    t0 = time.perf_counter()
    bfs_result = _bfs(graph, 0)
    bfs_time_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    dijkstra_result = _dijkstra(graph, 0)
    dijkstra_time_ms = (time.perf_counter() - t0) * 1000

    tracemalloc.start()
    _bfs(graph, 0)
    _, bfs_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    _dijkstra(graph, 0)
    _, dijkstra_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "num_nodes": num_nodes,
        "correct": bfs_result == dijkstra_result,
        "bfs_time_ms": bfs_time_ms,
        "dijkstra_time_ms": dijkstra_time_ms,
        "bfs_peak_kb": bfs_peak / 1024,
        "dijkstra_peak_kb": dijkstra_peak / 1024,
    }


def format_complexity_report(top_k_kwargs=None, graph_kwargs=None):
    top_k = measure_top_k_complexity(**(top_k_kwargs or {}))
    graph = measure_graph_complexity(**(graph_kwargs or {}))

    lines = []
    lines.append("TOP_K: ORDER+TAKE vs. the optimizer's rewrite")
    lines.append(f"  n = {top_k['n']:,} groups, k = {top_k['k']}")
    lines.append("  GROUP+COUNT already built an O(n) frequency table before this step runs --")
    lines.append("  that cost is identical either way and is excluded below. What differs is")
    lines.append("  ONLY the incremental cost of the ORDER+TAKE step itself:")
    lines.append(f"    Naive (full sort)     O(n log n) time, +O(n) incremental space:  {top_k['naive_time_ms']:9.2f} ms, {top_k['naive_peak_kb']:12,.1f} KB peak")
    lines.append(f"    Optimized (heap TopK) O(n log k) time, +O(k) incremental space:  {top_k['optimized_time_ms']:9.2f} ms, {top_k['optimized_peak_kb']:12,.1f} KB peak")
    lines.append(f"  Time ratio (this step only):   {top_k['naive_time_ms'] / top_k['optimized_time_ms']:.2f}x")
    lines.append(f"  Space ratio (this step only):  {top_k['naive_peak_kb'] / top_k['optimized_peak_kb']:.2f}x")
    lines.append("  The pipeline's TOTAL memory is O(n) either way, dominated by GROUP+COUNT --")
    lines.append("  this optimization does not make the whole program O(k).")
    lines.append(f"  Correct: {top_k['correct']}")
    lines.append("")
    lines.append("EXPLORE: always-Dijkstra vs. the optimizer's choice of BFS")
    lines.append(f"  {graph['num_nodes']:,} nodes, unweighted")
    lines.append(f"  BFS        O(V+E) time, O(V+E) space:          {graph['bfs_time_ms']:9.2f} ms, {graph['bfs_peak_kb']:12,.1f} KB peak")
    lines.append(f"  Dijkstra   O((V+E) log V) time, O(V+E) space:  {graph['dijkstra_time_ms']:9.2f} ms, {graph['dijkstra_peak_kb']:12,.1f} KB peak")
    lines.append(f"  Time ratio:   {graph['dijkstra_time_ms'] / graph['bfs_time_ms']:.2f}x")
    lines.append(f"  Space ratio:  {graph['dijkstra_peak_kb'] / graph['bfs_peak_kb']:.2f}x")
    lines.append(f"  Correct: {graph['correct']}")
    lines.append("")
    lines.append("Note the asymmetry, and it's the honest finding, not a talking point:")
    lines.append("TOP_K's space ratio is dramatic because O(n) and O(k) are different")
    lines.append("complexity classes when k << n. BFS vs Dijkstra's ratio is modest")
    lines.append("because both are O(V+E) -- same class, different constant factor.")
    lines.append("Both are real wins. Only one of them is a big number.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_complexity_report())
