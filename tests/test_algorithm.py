import pytest

from passeio_turistico_maximo.algorithm import max_tour_path


def test_max_tour_path_empty_graph():
    assert max_tour_path({}) == []


def test_max_tour_path_single_node():
    assert max_tour_path({"A": []}) == ["A"]


def test_max_tour_path_simple_line():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
    assert max_tour_path(graph) == ["A", "B", "C"]


def test_max_tour_path_cycle():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    }
    assert max_tour_path(graph) == ["A", "B", "C"]


def test_max_tour_path_with_branching():
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    assert max_tour_path(graph) in (["A", "B", "D"], ["A", "C", "D"])
