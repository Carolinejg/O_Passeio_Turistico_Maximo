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


def _optimistic_bound(
    graph: WeightedGraph,
    current: str,
    remaining_nodes: Set[str],
    current_weight: int,
) -> int:
    """Retorna um limite superior relaxado para o peso restante de um caminho."""
    if not remaining_nodes:
        return current_weight

    candidate_weights = []
    for node in remaining_nodes:
        outgoing_weights = list(graph.get(node, {}).values())
        if outgoing_weights:
            candidate_weights.append(max(outgoing_weights))

    candidate_weights.sort(reverse=True)
    remaining_steps = len(remaining_nodes)
    return current_weight + sum(candidate_weights[:remaining_steps])


def longest_path_branch_and_bound(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> List[str]:
    """Encontra o caminho de maior peso usando backtracking com branch and bound."""
    if start not in graph or end not in graph:
        return []

    greedy_result = greedy_path(graph, start, end)
    best_path = greedy_result if greedy_result and greedy_result[-1] == end else []
    best_weight = path_weight(graph, best_path) if best_path else -1

    visited: Set[str] = {start}
    current_path: List[str] = [start]

    def dfs(current: str, path: List[str], current_weight: int) -> None:
        nonlocal best_path, best_weight

        if current == end:
            if current_weight > best_weight:
                best_weight = current_weight
                best_path = list(path)
            return

        remaining_nodes = {node for node in graph if node not in visited}
        if remaining_nodes:
            optimistic = _optimistic_bound(graph, current, remaining_nodes, current_weight)
            if optimistic <= best_weight:
                return

        for neighbor, weight in graph[current].items():
            if neighbor in visited:
                continue
            visited.add(neighbor)
            path.append(neighbor)
            dfs(neighbor, path, current_weight + weight)
            path.pop()
            visited.remove(neighbor)

    dfs(start, current_path, 0)
    return best_path


def longest_path_branch_and_bound_with_metrics(
    graph: WeightedGraph,
    start: str,
    end: str,
) -> tuple[List[str], int, int, int, int]:
    """Encontra o caminho de maior peso com branch and bound e retorna métricas."""
    if start not in graph or end not in graph:
        return [], 0, 0, 0, 0

    greedy_result = greedy_path(graph, start, end)
    best_path = greedy_result if greedy_result and greedy_result[-1] == end else []
    best_weight = path_weight(graph, best_path) if best_path else -1

    visited: Set[str] = {start}
    current_path: List[str] = [start]
    call_count = 0
    pruned_count = 0

    def dfs(current: str, path: List[str], current_weight: int) -> None:
        nonlocal best_path, best_weight, call_count, pruned_count
        call_count += 1

        if current == end:
            if current_weight > best_weight:
                best_weight = current_weight
                best_path = list(path)
            return

        remaining_nodes = {node for node in graph if node not in visited}
        if remaining_nodes:
            optimistic = _optimistic_bound(graph, current, remaining_nodes, current_weight)
            if optimistic <= best_weight:
                pruned_count += 1
                return

        for neighbor, weight in graph[current].items():
            if neighbor in visited:
                continue
            visited.add(neighbor)
            path.append(neighbor)
            dfs(neighbor, path, current_weight + weight)
            path.pop()
            visited.remove(neighbor)

    dfs(start, current_path, 0)
    return best_path, call_count, pruned_count, path_weight(graph, best_path), len(best_path)


def max_tour_path(graph: Dict[str, object]) -> List[str]:
    """Compatibilidade com testes antigos para o nome do algoritmo."""
    if not graph:
        return []

    if isinstance(next(iter(graph.values())), dict):
        normalized_graph = {
            node: {neighbor: weight for neighbor, weight in neighbors.items()} 
            if isinstance(neighbors, dict) else {neighbor: 1 for neighbor in neighbors}
            for node, neighbors in graph.items()
        }
        start = next(iter(graph))
        end = list(graph)[-1]
        return longest_path_backtracking(normalized_graph, start, end)

    normalized_graph = {
        node: {neighbor: 1 for neighbor in neighbors}
        if isinstance(neighbors, list)
        else {neighbor: 1 for neighbor in []}
        for node, neighbors in graph.items()
    }
    start = next(iter(graph))
    end = list(graph)[-1]
    return longest_path_backtracking(normalized_graph, start, end)
