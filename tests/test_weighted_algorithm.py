from passeio_turistico_maximo.algorithm import (
    generate_complete_weighted_graph,
    longest_path_backtracking,
    path_weight,
)


def test_generate_complete_weighted_graph():
    graph = generate_complete_weighted_graph(5, seed=42)
    assert len(graph) == 5
    for node, edges in graph.items():
        assert len(edges) == 4
        assert all(1 <= weight <= 100 for weight in edges.values())


def test_longest_path_backtracking():
    graph = generate_complete_weighted_graph(5, seed=7)
    start, end = "v0", "v4"
    path = longest_path_backtracking(graph, start, end)

    assert path[0] == start
    assert path[-1] == end
    assert set(path) <= set(graph)
    assert len(path) >= 2


def test_path_weight_on_empty_path():
    assert path_weight(graph=generate_complete_weighted_graph(3, seed=1), path=[]) == 0
