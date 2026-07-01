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


def measure_runtime(n: int, seed: int, timeout: float = 60.0) -> Optional[tuple[float, int, int, int]]:
    """Gera uma instância e mede a execução do backtracking com timeout."""
    graph = generate_complete_weighted_graph(n, seed=seed)
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
    return elapsed, calls, weight, length


def run_benchmarks(sizes: List[int], trials: int = 3, timeout: float = 60.0) -> tuple[
    Dict[int, List[Optional[float]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
    Dict[int, List[Optional[int]]],
]:
    """Executa o benchmark para cada tamanho de grafo e coleta métricas."""
    runtime_data: Dict[int, List[Optional[float]]] = {}
    call_data: Dict[int, List[Optional[int]]] = {}
    weight_data: Dict[int, List[Optional[int]]] = {}
    length_data: Dict[int, List[Optional[int]]] = {}
    for n in sizes:
        times: List[Optional[float]] = []
        calls: List[Optional[int]] = []
        weights: List[Optional[int]] = []
        lengths: List[Optional[int]] = []
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
                runtime, recursive_calls, weight, length = result
                print(f"  tentativa {trial}/{trials}: {runtime:.3f} s, chamadas={recursive_calls}, peso={weight}, tamanho={length}")
                times.append(runtime)
                calls.append(recursive_calls)
                weights.append(weight)
                lengths.append(length)
        runtime_data[n] = times
        call_data[n] = calls
        weight_data[n] = weights
        length_data[n] = lengths
    return runtime_data, call_data, weight_data, length_data


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
        avg_time = statistics.mean(valid_times) if valid_times else None
        avg_calls = statistics.mean(valid_calls) if valid_calls else None
        avg_weight = statistics.mean(valid_weights) if valid_weights else None
        avg_length = statistics.mean(valid_lengths) if valid_lengths else None
        avg_time_str = f"{avg_time:.3f}" if avg_time is not None else "timeout"
        avg_calls_str = f"{avg_calls:.0f}" if avg_calls is not None else "timeout"
        avg_weight_str = f"{avg_weight:.0f}" if avg_weight is not None else "timeout"
        avg_length_str = f"{avg_length:.0f}" if avg_length is not None else "timeout"
        print(
            f"{n:<4} {time_str:<30} {avg_time_str:<12} {call_str:<30} {avg_calls_str}" \
            f"    {weight_str:<30} {avg_weight_str}    {length_str:<30} {avg_length_str}"
        )


def plot_data(
    runtime_data: Dict[int, List[Optional[float]]],
    call_data: Dict[int, List[Optional[int]]],
    weight_data: Dict[int, List[Optional[int]]],
    length_data: Dict[int, List[Optional[int]]],
    output_runtime: str = "benchmark_runtime.png",
    output_calls: str = "benchmark_calls.png",
    output_weight: str = "benchmark_weight.png",
    output_length: str = "benchmark_length.png",
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
    for n in runtime_data:
        valid_times = [t for t in runtime_data[n] if t is not None]
        valid_calls = [c for c in call_data[n] if c is not None]
        valid_weights = [w for w in weight_data[n] if w is not None]
        valid_lengths = [l for l in length_data[n] if l is not None]
        if not valid_times or not valid_calls or not valid_weights or not valid_lengths:
            continue
        sizes.append(n)
        runtime_averages.append(statistics.mean(valid_times))
        call_averages.append(statistics.mean(valid_calls))
        weight_averages.append(statistics.mean(valid_weights))
        length_averages.append(statistics.mean(valid_lengths))

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


def main() -> None:
    """Ponto de entrada do benchmark."""
    sizes = [5, 8, 10, 12, 15]
    runtime_data, call_data, weight_data, length_data = run_benchmarks(sizes, trials=2, timeout=60.0)
    summarize(runtime_data, call_data, weight_data, length_data)
    plot_data(runtime_data, call_data, weight_data, length_data)


if __name__ == "__main__":
    main()
