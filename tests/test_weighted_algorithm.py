from passeio_turistico_maximo.algorithm import (
    generate_complete_weighted_graph,
    greedy_path,
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


def test_greedy_path_reaches_destiny_in_complete_graph():
    graph = generate_complete_weighted_graph(5, seed=7)
    start, end = "v0", "v4"
    path = greedy_path(graph, start, end)

    assert path[0] == start
    assert path[-1] == end
    assert len(path) >= 2
    assert len(path) == len(set(path))


def test_greedy_path_stops_at_dead_end():
    graph = {
        "A": {"B": 5},
        "B": {"C": 4},
        "C": {"A": 1},
        "D": {},
    }
    assert greedy_path(graph, "A", "D") == ["A", "B", "C"]


def test_path_weight_on_empty_path():
    assert path_weight(graph=generate_complete_weighted_graph(3, seed=1), path=[]) == 0
