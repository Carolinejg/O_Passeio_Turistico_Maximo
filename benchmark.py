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
    longest_path_backtracking_with_metrics,
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


def measure_runtime(n: int, seed: int, timeout: float = 60.0) -> Optional[tuple[float, int, int, int, List[int]]]:
    """Gera uma instância e mede a execução do backtracking com timeout."""
    graph = generate_complete_weighted_graph(n, seed=seed)
    edge_weights = collect_edge_weights(graph)
    start = "v0"
    end = f"v{n-1}"
    queue: multiprocessing.Queue[Any] = multiprocessing.Queue()
    process = multiprocessing.Process(target=worker, args=(graph, start, end, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return None

    if queue.empty():
        return None

    elapsed, calls, weight, length = queue.get()
    return elapsed, calls, weight, length, edge_weights


def run_benchmarks(sizes: List[int], trials: int = 3, timeout: float = 60.0) -> tuple[
    Dict[int, List[Optional[float]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[int]],
]:
    """Executa o benchmark para cada tamanho de grafo e coleta métricas."""
    runtime_data: Dict[int, List[Optional[float]]] = {}
    call_data: Dict[int, List[Optional[int]]] = {}
    weight_data: Dict[int, List[Optional[int]]] = {}
    length_data: Dict[int, List[Optional[int]]] = {}
    weight_distribution_data: Dict[int, List[int]] = {}
    for n in sizes:
        times: List[Optional[float]] = []
        calls: List[Optional[int]] = []
        weights: List[Optional[int]] = []
        lengths: List[Optional[int]] = []
        edge_weights_all: List[int] = []
        print(f"Executando n={n}...")
        for trial in range(1, trials + 1):
            print(f"  tentativa {trial}/{trials}", end="\r")
            result = measure_runtime(n, seed=trial * 17, timeout=timeout)
            if result is None:
                print(f"  tentativa {trial}/{trials}: timeout após {timeout} segundos")
                times.append(None)
                calls.append(None)
                weights.append(None)
                lengths.append(None)
            else:
                runtime, recursive_calls, weight, length, edge_weights = result
                print(f"  tentativa {trial}/{trials}: {runtime:.3f} s, chamadas={recursive_calls}, peso={weight}, tamanho={length}")
                times.append(runtime)
                calls.append(recursive_calls)
                weights.append(weight)
                lengths.append(length)
                edge_weights_all.extend(edge_weights)
        runtime_data[n] = times
        call_data[n] = calls
        weight_data[n] = weights
        length_data[n] = lengths
        weight_distribution_data[n] = edge_weights_all
    return runtime_data, call_data, weight_data, length_data, weight_distribution_data


def summarize(
    runtime_data: Dict[int, List[Optional[float]]],
    call_data: Dict[int, List[Optional[int]]],
    weight_data: Dict[int, List[Optional[int]]],
    length_data: Dict[int, List[Optional[int]]],
) -> None:
    """Imprime um resumo tabular das métricas coletadas."""
    print("\nResumo de tempos, chamadas recursivas, peso e tamanho do caminho:")
    print("n    tempos (s)                       média (s)    chamadas                      média chamadas    peso                      média peso    tamanho                      média tamanho")
    for n in runtime_data:
        times = runtime_data[n]
        calls = call_data[n]
        weights = weight_data[n]
        lengths = length_data[n]
        time_str = ", ".join(
            "timeout" if t is None else f"{t:.3f}"
            for t in times
        )
        call_str = ", ".join(
            "timeout" if c is None else str(c)
            for c in calls
        )
        weight_str = ", ".join(
            "timeout" if w is None else str(w)
            for w in weights
        )
        length_str = ", ".join(
            "timeout" if l is None else str(l)
            for l in lengths
        )
        valid_times = [t for t in times if t is not None]
        valid_calls = [c for c in calls if c is not None]
        valid_weights = [w for w in weights if w is not None]
        valid_lengths = [l for l in lengths if l is not None]
        valid_time_per_call = [t / c for t, c in zip(times, calls) if t is not None and c is not None and c > 0]
        avg_time = statistics.mean(valid_times) if valid_times else None
        avg_calls = statistics.mean(valid_calls) if valid_calls else None
        avg_weight = statistics.mean(valid_weights) if valid_weights else None
        avg_length = statistics.mean(valid_lengths) if valid_lengths else None
        avg_time_per_call = statistics.mean(valid_time_per_call) if valid_time_per_call else None
        avg_time_str = f"{avg_time:.3f}" if avg_time is not None else "timeout"
        avg_calls_str = f"{avg_calls:.0f}" if avg_calls is not None else "timeout"
        avg_weight_str = f"{avg_weight:.0f}" if avg_weight is not None else "timeout"
        avg_length_str = f"{avg_length:.0f}" if avg_length is not None else "timeout"
        avg_time_per_call_str = f"{avg_time_per_call:.6f}" if avg_time_per_call is not None else "timeout"
        print(
            f"{n:<4} {time_str:<30} {avg_time_str:<12} {call_str:<30} {avg_calls_str}" \
            f"    {weight_str:<30} {avg_weight_str}    {length_str:<30} {avg_length_str}    {avg_time_per_call_str}"
        )


def plot_data(
    runtime_data: Dict[int, List[Optional[float]]],
    call_data: Dict[int, List[Optional[int]]],
    weight_data: Dict[int, List[Optional[int]]],
    length_data: Dict[int, List[Optional[int]]],
    weight_distribution_data: Dict[int, List[int]],
    output_runtime: str = "benchmark_runtime.png",
    output_calls: str = "benchmark_calls.png",
    output_weight: str = "benchmark_weight.png",
    output_length: str = "benchmark_length.png",
    output_time_per_call: str = "benchmark_time_per_call.png",
    output_time_vs_calls: str = "benchmark_time_vs_calls.png",
    output_boxplot_times: str = "benchmark_boxplot_times.png",
    output_boxplot_weights: str = "benchmark_boxplot_weights.png",
    output_edge_weight_histogram: str = "benchmark_edge_weight_histogram.png",
) -> None:
    """Desenha gráficos para as métricas coletadas no benchmark."""
    if plt is None:
        print("matplotlib não encontrado. Instale com 'pip install matplotlib' para gerar o gráfico.")
        return

    sizes: List[int] = []
    runtime_averages: List[float] = []
    call_averages: List[float] = []
    weight_averages: List[float] = []
    length_averages: List[float] = []
    time_per_call_averages: List[float] = []
    for n in runtime_data:
        valid_times = [t for t in runtime_data[n] if t is not None]
        valid_calls = [c for c in call_data[n] if c is not None]
        valid_weights = [w for w in weight_data[n] if w is not None]
        valid_lengths = [l for l in length_data[n] if l is not None]
        valid_time_per_call = [t / c for t, c in zip(runtime_data[n], call_data[n]) if t is not None and c is not None and c > 0]
        if not valid_times or not valid_calls or not valid_weights or not valid_lengths or not valid_time_per_call:
            continue
        sizes.append(n)
        runtime_averages.append(statistics.mean(valid_times))
        call_averages.append(statistics.mean(valid_calls))
        weight_averages.append(statistics.mean(valid_weights))
        length_averages.append(statistics.mean(valid_lengths))
        time_per_call_averages.append(statistics.mean(valid_time_per_call))

    if not sizes:
        print("Nenhum tempo válido para plotar.")
        return

    # Gráfico de tempo médio
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, runtime_averages, marker="o", linestyle="-", color="blue")
    plt.title("Tempo de execução da busca por backtracking vs n")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Tempo médio de execução (s)")
    plt.grid(True)
    plt.xticks(sizes)
    plt.tight_layout()
    plt.savefig(output_runtime)
    print(f"Gráfico de tempo salvo em {output_runtime}")

    # Gráfico de chamadas recursivas médias
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, call_averages, marker="o", linestyle="-", color="green")
    plt.title("Número médio de chamadas recursivas da busca por backtracking vs n")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Chamadas recursivas médias")
    plt.grid(True)
    plt.xticks(sizes)
    plt.tight_layout()
    plt.savefig(output_calls)
    print(f"Gráfico de chamadas recursivas salvo em {output_calls}")

    # Gráfico de peso médio do melhor caminho
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, weight_averages, marker="o", linestyle="-", color="red")
    plt.title("Peso médio do melhor caminho por backtracking vs n")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Peso médio do melhor caminho")
    plt.grid(True)
    plt.xticks(sizes)
    plt.tight_layout()
    plt.savefig(output_weight)
    print(f"Gráfico de peso salvo em {output_weight}")

    # Gráfico de tamanho médio do melhor caminho
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, length_averages, marker="o", linestyle="-", color="purple")
    plt.title("Tamanho médio do melhor caminho por backtracking vs n")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Tamanho médio do melhor caminho")
    plt.grid(True)
    plt.xticks(sizes)
    plt.tight_layout()
    plt.savefig(output_length)
    print(f"Gráfico de tamanho salvo em {output_length}")

    # Gráfico de tempo médio por chamada recursiva
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, time_per_call_averages, marker="o", linestyle="-", color="orange")
    plt.title("Tempo médio por chamada recursiva vs n")
    plt.xlabel("Número de vértices n")
    plt.ylabel("Tempo médio por chamada (s)")
    plt.grid(True)
    plt.xticks(sizes)
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
        plt.title("Tempo de execução vs número de chamadas recursivas")
        plt.xlabel("Chamadas recursivas")
        plt.ylabel("Tempo de execução (s)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_time_vs_calls)
        print(f"Gráfico de tempo vs chamadas recursivas salvo em {output_time_vs_calls}")

    # Boxplot de variabilidade de tempo por semente
    valid_sizes_for_time = [n for n in sizes if any(t is not None for t in runtime_data[n])]
    times_by_n = [[t for t in runtime_data[n] if t is not None] for n in valid_sizes_for_time]
    if times_by_n and any(times_by_n):
        plt.figure(figsize=(8, 5))
        plt.boxplot(times_by_n, labels=[str(n) for n in valid_sizes_for_time], showmeans=True)
        plt.title("Variabilidade de tempo por semente para diferentes n")
        plt.xlabel("Número de vértices n")
        plt.ylabel("Tempo de execução (s)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_boxplot_times)
        print(f"Boxplot de tempo salvo em {output_boxplot_times}")

    # Boxplot de variabilidade de peso por semente
    valid_sizes_for_weight = [n for n in sizes if any(w is not None for w in weight_data[n])]
    weights_by_n = [[w for w in weight_data[n] if w is not None] for n in valid_sizes_for_weight]
    if weights_by_n and any(weights_by_n):
        plt.figure(figsize=(8, 5))
        plt.boxplot(weights_by_n, labels=[str(n) for n in valid_sizes_for_weight], showmeans=True)
        plt.title("Variabilidade de peso do melhor caminho por semente para diferentes n")
        plt.xlabel("Número de vértices n")
        plt.ylabel("Peso do melhor caminho")
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
    runtime_data, call_data, weight_data, length_data, weight_distribution_data = run_benchmarks(sizes, trials=2, timeout=60.0)
    summarize(runtime_data, call_data, weight_data, length_data)
    plot_data(
        runtime_data,
        call_data,
        weight_data,
        length_data,
        weight_distribution_data,
    )


if __name__ == "__main__":
    main()
