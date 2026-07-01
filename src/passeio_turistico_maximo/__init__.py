"""Pacote principal do passeio turístico máximo."""

from .algorithm import (
    generate_complete_weighted_graph,
    longest_path_backtracking,
    path_weight,
)

__all__ = [
    "generate_complete_weighted_graph",
    "longest_path_backtracking",
    "path_weight",
]
