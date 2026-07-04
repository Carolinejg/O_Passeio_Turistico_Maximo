import multiprocessing
import statistics
import time
from typing import Any, Dict, List, Optional

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None  # type: ignore

from passeio_turistico_maximo.algorithm import (
    generate_complete_weighted_graph,
    greedy_path,
    longest_path_backtracking_with_metrics,
    path_weight,
)

# worker() executa o algoritmo de backtracking em um processo separado.
# Isso ajuda a impor timeout para casos de execução muito longa.
# O resultado inclui tempo, número de chamadas recursivas, peso do caminho e tamanho do caminho.
def worker(graph: Dict[str, Dict[str, int]], start: str, end: str, result_queue: multiprocessing.Queue) -> None:
    start_time = time.perf_counter()
    path, calls, weight, length = longest_path_backtracking_with_metrics(graph, start, end)
    elapsed = time.perf_counter() - start_time
    result_queue.put((elapsed, calls, weight, length))


def collect_edge_weights(graph: Dict[str, Dict[str, int]]) -> List[int]:
    return [weight for edges in graph.values() for weight in edges.values()]


def measure_runtime(n: int, seed: int, timeout: float = 60.0) -> tuple[
    Optional[float], Optional[int], Optional[int], Optional[int],
    Optional[float], Optional[int], Optional[int],
    List[int]
]:
    """Gera uma instância e mede a execução do backtracking e da heurística gulosa."""
    graph = generate_complete_weighted_graph(n, seed=seed)
    edge_weights = collect_edge_weights(graph)
    start = "v0"
    end = f"v{n-1}"

    greedy_start = time.perf_counter()
    greedy_path_result = greedy_path(graph, start, end)
    greedy_elapsed = time.perf_counter() - greedy_start
    greedy_weight = path_weight(graph, greedy_path_result)
    greedy_length = len(greedy_path_result)

    queue: multiprocessing.Queue[Any] = multiprocessing.Queue()
    process = multiprocessing.Process(target=worker, args=(graph, start, end, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return None, None, None, None, greedy_elapsed, greedy_weight, greedy_length, edge_weights

    if queue.empty():
        return None, None, None, None, greedy_elapsed, greedy_weight, greedy_length, edge_weights

    elapsed, calls, weight, length = queue.get()
    return elapsed, calls, weight, length, greedy_elapsed, greedy_weight, greedy_length, edge_weights


def run_benchmarks(sizes: List[int], trials: int = 3, timeout: float = 60.0) -> tuple[
    Dict[int, List[Optional[float]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[float]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[int]],
]:
    """Executa o benchmark para cada tamanho de grafo e coleta métricas."""
    runtime_data: Dict[int, List[Optional[float]]] = {}
    call_data: Dict[int, List[Optional[int]]] = {}
    weight_data: Dict[int, List[Optional[int]]] = {}
    length_data: Dict[int, List[Optional[int]]] = {}
    runtime_greedy_data: Dict[int, List[Optional[float]]] = {}
    weight_greedy_data: Dict[int, List[Optional[int]]] = {}
    length_greedy_data: Dict[int, List[Optional[int]]] = {}
    weight_distribution_data: Dict[int, List[int]] = {}
    for n in sizes:
        times: List[Optional[float]] = []
        calls: List[Optional[int]] = []
        weights: List[Optional[int]] = []
        lengths: List[Optional[int]] = []
        greedy_times: List[Optional[float]] = []
        greedy_weights: List[Optional[int]] = []
        greedy_lengths: List[Optional[int]] = []
        edge_weights_all: List[int] = []
        print(f"Executando n={n}...")
        for trial in range(1, trials + 1):
            print(f"  tentativa {trial}/{trials}", end="\r")
            (
                runtime,
                recursive_calls,
                weight,
                length,
                greedy_runtime,
                greedy_weight,
                greedy_length,
                edge_weights,
            ) = measure_runtime(n, seed=trial * 17, timeout=timeout)
            if runtime is None and greedy_runtime is None:
                print(f"  tentativa {trial}/{trials}: timeout após {timeout} segundos")
                times.append(None)
                calls.append(None)
                weights.append(None)
                lengths.append(None)
                greedy_times.append(None)
                greedy_weights.append(None)
                greedy_lengths.append(None)
            else:
                if runtime is None:
                    print(f"  tentativa {trial}/{trials}: backtracking timeout; greedy finalizado em {greedy_runtime:.3f} s")
                else:
                    print(f"  tentativa {trial}/{trials}: backtracking {runtime:.3f} s, chamadas={recursive_calls}, peso={weight}, tamanho={length}; greedy {greedy_runtime:.3f} s, peso={greedy_weight}, tamanho={greedy_length}")
                times.append(runtime)
                calls.append(recursive_calls)
                weights.append(weight)
                lengths.append(length)
                greedy_times.append(greedy_runtime)
                greedy_weights.append(greedy_weight)
                greedy_lengths.append(greedy_length)
                edge_weights_all.extend(edge_weights)
        runtime_data[n] = times
        call_data[n] = calls
        weight_data[n] = weights
        length_data[n] = lengths
        runtime_greedy_data[n] = greedy_times
        weight_greedy_data[n] = greedy_weights
        length_greedy_data[n] = greedy_lengths
        weight_distribution_data[n] = edge_weights_all
    return (
        runtime_data,
        call_data,
        weight_data,
        length_data,
        runtime_greedy_data,
        weight_greedy_data,
        length_greedy_data,
        weight_distribution_data,
    )


def summarize(
    runtime_data: Dict[int, List[Optional[float]]],
    call_data: Dict[int, List[Optional[int]]],
    weight_data: Dict[int, List[Optional[int]]],
    length_data: Dict[int, List[Optional[int]]],
    runtime_greedy_data: Dict[int, List[Optional[float]]],
    weight_greedy_data: Dict[int, List[Optional[int]]],
    length_greedy_data: Dict[int, List[Optional[int]]],
) -> None:
    """Imprime um resumo tabular das métricas coletadas."""
    print("\nResumo comparativo: backtracking vs guloso")
    print(
        "n | BT tempo médio (s) | GR tempo médio (s) | BT peso médio | GR peso médio | "
        "razão peso (GR/BT) | BT tamanho médio | GR tamanho médio"
    )
    for n in sorted(runtime_data):
        bt_times = [t for t in runtime_data[n] if t is not None]
        bt_weights = [w for w in weight_data[n] if w is not None]
        bt_lengths = [l for l in length_data[n] if l is not None]
        gr_times = [t for t in runtime_greedy_data[n] if t is not None]
        gr_weights = [w for w in weight_greedy_data[n] if w is not None]
        gr_lengths = [l for l in length_greedy_data[n] if l is not None]

        avg_bt_time = statistics.mean(bt_times) if bt_times else None
        avg_gr_time = statistics.mean(gr_times) if gr_times else None
        avg_bt_weight = statistics.mean(bt_weights) if bt_weights else None
        avg_gr_weight = statistics.mean(gr_weights) if gr_weights else None
        avg_bt_length = statistics.mean(bt_lengths) if bt_lengths else None
        avg_gr_length = statistics.mean(gr_lengths) if gr_lengths else None
        quality_ratios = [gr / bt for gr, bt in zip(gr_weights, bt_weights) if gr is not None and bt is not None and bt > 0]
        avg_quality_ratio = statistics.mean(quality_ratios) if quality_ratios else None

        avg_bt_time_str = f"{avg_bt_time:.3f}" if avg_bt_time is not None else "timeout"
        avg_gr_time_str = f"{avg_gr_time:.3f}" if avg_gr_time is not None else "timeout"
        avg_bt_weight_str = f"{avg_bt_weight:.0f}" if avg_bt_weight is not None else "timeout"
        avg_gr_weight_str = f"{avg_gr_weight:.0f}" if avg_gr_weight is not None else "timeout"
        avg_bt_length_str = f"{avg_bt_length:.0f}" if avg_bt_length is not None else "timeout"
        avg_gr_length_str = f"{avg_gr_length:.0f}" if avg_gr_length is not None else "timeout"
        avg_quality_ratio_str = f"{avg_quality_ratio:.3f}" if avg_quality_ratio is not None else "n/a"

        print(
            f"{n:<2} | {avg_bt_time_str:<15} | {avg_gr_time_str:<15} | {avg_bt_weight_str:<12} | {avg_gr_weight_str:<12} | {avg_quality_ratio_str:<15} | {avg_bt_length_str:<14} | {avg_gr_length_str:<14}"
        )


def plot_data(
    runtime_data: Dict[int, List[Optional[float]]],
    call_data: Dict[int, List[Optional[int]]],
    weight_data: Dict[int, List[Optional[int]]],
    length_data: Dict[int, List[Optional[int]]],
    runtime_greedy_data: Dict[int, List[Optional[float]]],
    weight_greedy_data: Dict[int, List[Optional[int]]],
    length_greedy_data: Dict[int, List[Optional[int]]],
    weight_distribution_data: Dict[int, List[int]],
    output_runtime: str = "benchmark_runtime.png",
    output_calls: str = "benchmark_calls.png",
    output_weight: str = "benchmark_weight.png",
    output_length: str = "benchmark_length.png",
    output_time_per_call: str = "benchmark_time_per_call.png",
    output_time_vs_calls: str = "benchmark_backtracking_time_vs_calls.png",
    output_quality_ratio: str = "benchmark_quality_ratio.png",
    output_boxplot_times: str = "benchmark_boxplot_times.png",
    output_boxplot_weights: str = "benchmark_boxplot_weights.png",
    output_edge_weight_histogram: str = "benchmark_edge_weight_histogram.png",
) -> None:
    """Desenha gráficos para as métricas coletadas no benchmark."""
    if plt is None:
        print("matplotlib não encontrado. Instale com 'pip install matplotlib' para gerar o gráfico.")
        return

    sizes_bt: List[int] = []
    runtime_bt_averages: List[float] = []
    weight_bt_averages: List[float] = []
    length_bt_averages: List[float] = []
    time_per_call_averages: List[float] = []
    sizes_gr: List[int] = []
    runtime_gr_averages: List[float] = []
    weight_gr_averages: List[float] = []
    length_gr_averages: List[float] = []
    for n in sorted(runtime_data):
        valid_bt_times = [t for t in runtime_data[n] if t is not None]
        valid_bt_calls = [c for c in call_data[n] if c is not None]
        valid_bt_weights = [w for w in weight_data[n] if w is not None]
        valid_bt_lengths = [l for l in length_data[n] if l is not None]
        valid_bt_time_per_call = [t / c for t, c in zip(runtime_data[n], call_data[n]) if t is not None and c is not None and c > 0]
        valid_gr_times = [t for t in runtime_greedy_data[n] if t is not None]
        valid_gr_weights = [w for w in weight_greedy_data[n] if w is not None]
        valid_gr_lengths = [l for l in length_greedy_data[n] if l is not None]

        if valid_bt_times:
            sizes_bt.append(n)
            runtime_bt_averages.append(statistics.mean(valid_bt_times))
        if valid_bt_weights:
            weight_bt_averages.append(statistics.mean(valid_bt_weights))
        if valid_bt_lengths:
            length_bt_averages.append(statistics.mean(valid_bt_lengths))
        if valid_bt_time_per_call:
            time_per_call_averages.append(statistics.mean(valid_bt_time_per_call))
        if valid_gr_times:
            sizes_gr.append(n)
            runtime_gr_averages.append(statistics.mean(valid_gr_times))
        if valid_gr_weights:
            weight_gr_averages.append(statistics.mean(valid_gr_weights))
        if valid_gr_lengths:
            length_gr_averages.append(statistics.mean(valid_gr_lengths))

    if not sizes_gr:
        print("Nenhum tempo válido para plotar.")
        return

    sizes_all = sorted(set(sizes_bt + sizes_gr))

    # Gráfico de tempo médio comparando backtracking e guloso
    plt.figure(figsize=(8, 5))
    if sizes_bt:
        plt.plot(sizes_bt, runtime_bt_averages, marker="o", linestyle="-", color="blue", label="Backtracking")
    if sizes_gr:
        plt.plot(sizes_gr, runtime_gr_averages, marker="o", linestyle="--", color="orange", label="Guloso")
    plt.title("Tempo médio de execução: Backtracking vs Guloso")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Tempo médio de execução (s)")
    plt.grid(True)
    plt.legend()
    plt.xticks(sizes_all)
    plt.tight_layout()
    plt.savefig(output_runtime)
    print(f"Gráfico de tempo salvo em {output_runtime}")

    # Gráfico de peso médio comparando backtracking e guloso
    plt.figure(figsize=(8, 5))
    if sizes_bt:
        plt.plot(sizes_bt, weight_bt_averages, marker="o", linestyle="-", color="red", label="Backtracking")
    if sizes_gr:
        plt.plot(sizes_gr, weight_gr_averages, marker="o", linestyle="--", color="purple", label="Guloso")
    plt.title("Peso médio do caminho: Backtracking vs Guloso")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Peso médio do caminho")
    plt.grid(True)
    plt.legend()
    plt.xticks(sizes_all)
    plt.tight_layout()
    plt.savefig(output_weight)
    print(f"Gráfico de peso salvo em {output_weight}")

    # Gráfico de comparação de qualidade relativa (somente quando o backtracking terminou)
    quality_ratios: List[float] = []
    quality_sizes: List[int] = []
    for n in sorted(runtime_data):
        completed_pairs: List[tuple[float, float]] = []
        for bt_time, bt_weight, gr_weight in zip(runtime_data[n], weight_data[n], weight_greedy_data[n]):
            if bt_time is not None and bt_weight is not None and gr_weight is not None and bt_weight > 0:
                completed_pairs.append((float(bt_weight), float(gr_weight)))

        if completed_pairs:
            bt_weights = [bt_weight for bt_weight, _ in completed_pairs]
            gr_weights = [gr_weight for _, gr_weight in completed_pairs]
            quality_sizes.append(n)
            quality_ratios.append(statistics.mean(gr_weights) / statistics.mean(bt_weights))

    if quality_sizes:
        plt.figure(figsize=(8, 5))
        plt.plot(quality_sizes, quality_ratios, marker="o", linestyle="-", color="brown")
        plt.title("Qualidade relativa (somente casos concluídos): peso guloso / peso ótimo vs n")
        plt.xlabel("Número de vértices n")
        plt.ylabel("Razão de peso (guloso / ótimo)")
        plt.grid(True)
        plt.xticks(quality_sizes)
        plt.tight_layout()
        plt.savefig(output_quality_ratio)
        print(f"Gráfico de qualidade relativa salvo em {output_quality_ratio}")

    # Gráfico de tamanho médio comparando backtracking e guloso
    plt.figure(figsize=(8, 5))
    if sizes_bt:
        plt.plot(sizes_bt, length_bt_averages, marker="o", linestyle="-", color="purple", label="Backtracking")
    if sizes_gr:
        plt.plot(sizes_gr, length_gr_averages, marker="o", linestyle="--", color="green", label="Guloso")
    plt.title("Tamanho médio do caminho: Backtracking vs Guloso")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Tamanho médio do caminho")
    plt.grid(True)
    plt.legend()
    plt.xticks(sizes_all)
    plt.tight_layout()
    plt.savefig(output_length)
    print(f"Gráfico de tamanho salvo em {output_length}")

    # Gráfico de tempo médio por chamada recursiva (backtracking apenas)
    if sizes_bt and time_per_call_averages:
        plt.figure(figsize=(8, 5))
        plt.plot(sizes_bt, time_per_call_averages, marker="o", linestyle="-", color="orange")
        plt.title("Tempo médio por chamada recursiva vs n")
        plt.xlabel("Número de vértices n")
        plt.ylabel("Tempo médio por chamada (s)")
        plt.grid(True)
        plt.xticks(sizes_bt)
        plt.tight_layout()
        plt.savefig(output_time_per_call)
        print(f"Gráfico de tempo por chamada recursiva salvo em {output_time_per_call}")

    # Gráfico tempo x chamadas recursivas
    all_times: List[float] = []
    all_calls: List[int] = []
    for n in runtime_data:
        for time_value, call_value in zip(runtime_data[n], call_data[n]):
            if time_value is not None and call_value is not None:
                all_times.append(time_value)
                all_calls.append(call_value)
    if all_times and all_calls:
        plt.figure(figsize=(8, 5))
        plt.scatter(all_calls, all_times, c="blue", alpha=0.7)
        plt.title("Tempo de execução vs número de chamadas recursivas (backtracking)")
        plt.xlabel("Chamadas recursivas")
        plt.ylabel("Tempo de execução (s)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_time_vs_calls)
        print(f"Gráfico de tempo vs chamadas recursivas salvo em {output_time_vs_calls}")

    # Boxplot de variabilidade de tempo por semente comparando backtracking e guloso
    boxplot_time_groups: List[List[float]] = []
    boxplot_time_labels: List[str] = []
    positions: List[int] = []
    for idx, n in enumerate(sorted(runtime_data), start=1):
        bt_times = [t for t in runtime_data[n] if t is not None]
        gr_times = [t for t in runtime_greedy_data[n] if t is not None]
        if bt_times:
            boxplot_time_groups.append(bt_times)
            positions.append(idx * 3 - 2)
            boxplot_time_labels.append(f"{n}-BT")
        if gr_times:
            boxplot_time_groups.append(gr_times)
            positions.append(idx * 3 - 1)
            boxplot_time_labels.append(f"{n}-GR")
    if boxplot_time_groups:
        plt.figure(figsize=(12, 6))
        plt.boxplot(boxplot_time_groups, positions=positions, labels=boxplot_time_labels, showmeans=True)
        plt.title("Variabilidade de tempo por semente: Backtracking vs Guloso")
        plt.xlabel("n e método")
        plt.ylabel("Tempo de execução (s)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_boxplot_times)
        print(f"Boxplot de tempo salvo em {output_boxplot_times}")

    # Boxplot de variabilidade de peso por semente comparando backtracking e guloso
    boxplot_weight_groups: List[List[float]] = []
    boxplot_weight_labels: List[str] = []
    positions = []
    for idx, n in enumerate(sorted(weight_data), start=1):
        bt_weights = [w for w in weight_data[n] if w is not None]
        gr_weights = [w for w in weight_greedy_data[n] if w is not None]
        if bt_weights:
            boxplot_weight_groups.append(bt_weights)
            positions.append(idx * 3 - 2)
            boxplot_weight_labels.append(f"{n}-BT")
        if gr_weights:
            boxplot_weight_groups.append(gr_weights)
            positions.append(idx * 3 - 1)
            boxplot_weight_labels.append(f"{n}-GR")
    if boxplot_weight_groups:
        plt.figure(figsize=(12, 6))
        plt.boxplot(boxplot_weight_groups, positions=positions, labels=boxplot_weight_labels, showmeans=True)
        plt.title("Variabilidade de peso por semente: Backtracking vs Guloso")
        plt.xlabel("n e método")
        plt.ylabel("Peso do caminho")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_boxplot_weights)
        print(f"Boxplot de peso salvo em {output_boxplot_weights}")

    # Histograma da distribuição de pesos das arestas
    all_edge_weights = [w for weights in weight_distribution_data.values() for w in weights]
    if all_edge_weights:
        plt.figure(figsize=(8, 5))
        plt.hist(all_edge_weights, bins=20, color="skyblue", edgecolor="black")
        plt.title("Histograma da distribuição de pesos das arestas")
        plt.xlabel("Peso da aresta")
        plt.ylabel("Frequência")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_edge_weight_histogram)
        print(f"Histograma de pesos das arestas salvo em {output_edge_weight_histogram}")


def main() -> None:
    """Ponto de entrada do benchmark."""
    sizes = [5, 8, 10, 12, 15]
    (
        runtime_data,
        call_data,
        weight_data,
        length_data,
        runtime_greedy_data,
        weight_greedy_data,
        length_greedy_data,
        weight_distribution_data,
    ) = run_benchmarks(sizes, trials=2, timeout=60.0)
    summarize(
        runtime_data,
        call_data,
        weight_data,
        length_data,
        runtime_greedy_data,
        weight_greedy_data,
        length_greedy_data,
    )
    plot_data(
        runtime_data,
        call_data,
        weight_data,
        length_data,
        runtime_greedy_data,
        weight_greedy_data,
        length_greedy_data,
        weight_distribution_data,
    )


if __name__ == "__main__":
    main()
