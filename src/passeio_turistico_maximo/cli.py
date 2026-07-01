"""CLI para o passeio turístico máximo."""

from __future__ import annotations

import argparse

from .algorithm import (
    generate_complete_weighted_graph,
    longest_path_backtracking,
    path_weight,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa o algoritmo do passeio turístico máximo em um grafo completo ponderado."
    )
    parser.add_argument(
        "n",
        type=int,
        choices=[5, 8, 10, 12, 15],
        help="Número de vértices do grafo completo ponderado.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semente para gerar pesos aleatórios.",
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Vértice de início para a busca de backtracking.",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="Vértice de destino para a busca de backtracking.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    graph = generate_complete_weighted_graph(args.n, seed=args.seed)
    nodes = list(graph.keys())
    start = args.start or nodes[0]
    end = args.end or nodes[-1]

    backtracking_path = longest_path_backtracking(graph, start, end)

    print(f"Grafo completo com {args.n} nós")
    print(f"Início: {start}, Destino: {end}")
    print("Pesos de arestas:")
    for node, edges in graph.items():
        print(node, edges)

    print("\nMelhor caminho por backtracking (S→D):")
    print(" -> ".join(backtracking_path) if backtracking_path else "Nenhum caminho encontrado.")
    print("Peso total:", path_weight(graph, backtracking_path) if backtracking_path else 0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
