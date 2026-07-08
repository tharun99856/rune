from rune.complexity import measure_graph_complexity, measure_top_k_complexity


def test_measure_top_k_complexity_returns_correct_and_positive_metrics():
    result = measure_top_k_complexity(data_size=2000, domain_size=200, seed=1)

    assert result["correct"] is True
    assert result["n"] > 0
    assert result["naive_time_ms"] >= 0
    assert result["optimized_time_ms"] >= 0
    assert result["naive_peak_kb"] >= 0
    assert result["optimized_peak_kb"] >= 0


def test_measure_graph_complexity_returns_correct_and_positive_metrics():
    result = measure_graph_complexity(num_nodes=500, edges_per_node=3, seed=1)

    assert result["correct"] is True
    assert result["bfs_time_ms"] >= 0
    assert result["dijkstra_time_ms"] >= 0
    assert result["bfs_peak_kb"] >= 0
    assert result["dijkstra_peak_kb"] >= 0
