"""Algoritmos para encontrar o passeio turístico máximo."""

from __future__ import annotations

import random
from typing import Dict, Iterable, List, Optional, Set

WeightedGraph = Dict[str, Dict[str, int]]


def generate_complete_weighted_graph(
    n: int,
    min_weight: int = 1,
    max_weight: int = 100,
    seed: Optional[int] = None,
) -> WeightedGraph:
    """Gera um grafo completo ponderado com pesos aleatórios entre min_weight e max_weight."""
    rng = random.Random(seed)
    nodes = [f"v{i}" for i in range(n)]
    graph: WeightedGraph = {}

    for u in nodes:
        graph[u] = {
            v: rng.randint(min_weight, max_weight)
            for v in nodes
            if v != u
        }

    return graph


def path_weight(graph: WeightedGraph, path: Iterable[str]) -> int:
    """Calcula o peso total de um caminho em um grafo ponderado."""
    path_list = list(path)
    if len(path_list) < 2:
        return 0
    return sum(
        graph[path_list[i]][path_list[i + 1]]
        for i in range(len(path_list) - 1)
    )


def greedy_path(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> List[str]:
    """Encontra um caminho usando uma heurística gulosa de maior peso local."""
    if start not in graph or end not in graph:
        return []

    current = start
    visited: Set[str] = {start}
    path: List[str] = [start]

    while current != end:
        candidates = [
            (neighbor, weight)
            for neighbor, weight in graph[current].items()
            if neighbor not in visited
        ]
        if not candidates:
            break
        next_node = max(candidates, key=lambda item: item[1])[0]
        visited.add(next_node)
        path.append(next_node)
        current = next_node

    return path


def greedy_path_with_metrics(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> tuple[List[str], int, int]:
    """Encontra um caminho guloso e retorna métricas de peso e tamanho."""
    path = greedy_path(graph, start, end)
    return path, path_weight(graph, path), len(path)


def longest_path_backtracking(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> List[str]:
    """Encontra o caminho de maior peso de start até end usando backtracking."""
    if start not in graph or end not in graph:
        return []

    best_path: List[str] = []
    best_weight = -1
    visited: Set[str] = {start}

    def dfs(current: str, path: List[str], current_weight: int) -> None:
        nonlocal best_path, best_weight

        if current == end:
            if current_weight > best_weight:
                best_weight = current_weight
                best_path = list(path)
            return

        for neighbor, weight in graph[current].items():
            if neighbor in visited:
                continue
            visited.add(neighbor)
            path.append(neighbor)
            dfs(neighbor, path, current_weight + weight)
            path.pop()
            visited.remove(neighbor)

    dfs(start, [start], 0)
    return best_path


def longest_path_backtracking_with_count(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> tuple[List[str], int]:
    """Encontra o caminho de maior peso de start até end e conta chamadas recursivas."""
    if start not in graph or end not in graph:
        return [], 0

    best_path: List[str] = []
    best_weight = -1
    visited: Set[str] = {start}
    call_count = 0

    def dfs(current: str, path: List[str], current_weight: int) -> None:
        nonlocal best_path, best_weight, call_count
        call_count += 1

        if current == end:
            if current_weight > best_weight:
                best_weight = current_weight
                best_path = list(path)
            return

        for neighbor, weight in graph[current].items():
            if neighbor in visited:
                continue
            visited.add(neighbor)
            path.append(neighbor)
            dfs(neighbor, path, current_weight + weight)
            path.pop()
            visited.remove(neighbor)

    dfs(start, [start], 0)
    return best_path, call_count


def longest_path_backtracking_with_metrics(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> tuple[List[str], int, int, int]:
    """Encontra o caminho de maior peso de start até end e retorna métricas."""
    path, call_count = longest_path_backtracking_with_count(graph, start, end)
    return path, call_count, path_weight(graph, path), len(path)
