# Passeio Turístico Máximo

**Desenvolvido por Caroline Souza**

Este projeto implementa e compara três abordagens para o problema do **Passeio Turístico Máximo** em grafos completos ponderados:

- **Backtracking exaustivo**, que busca a solução ótima entre `start` e `end`.
- **Heurística gulosa**, que escolhe localmente a aresta de maior peso a cada passo.
- **Branch and bound**, que aplica poda para reduzir o espaço de busca sem alterar a solução final.

---

## Visão geral do projeto

As instâncias são geradas aleatoriamente com pesos inteiros entre `1` e `100`. O objetivo é comparar tempo de execução, chamadas recursivas, peso do caminho e tamanho do caminho entre as abordagens.

---

## Como instalar e executar

### Pré-requisitos

- Python 3.11+
- `pip`

### Instalação

```powershell
pip install -e .
pip install matplotlib
```

### Executar o algoritmo em uma instância específica

```powershell
python -m passeio_turistico_maximo 5 --seed 42 --start v0 --end v4
```

Esse comando usa a CLI para gerar uma instância única, mostrar o grafo e exibir o caminho encontrado.

### Executar o benchmark

```powershell
python benchmark.py
```

Esse comando roda várias instâncias e gera os gráficos usados na análise experimental.

---

## Diferença entre CLI e benchmark

- A CLI serve para testar um caso específico com `n`, `seed`, `start` e `end` definidos.
- O benchmark serve para medir desempenho e qualidade em várias instâncias.
- A CLI mostra o resultado de uma execução isolada.
- O benchmark coleta métricas e salva os gráficos automaticamente.

---

## Lista dos gráficos

- `benchmark_runtime.png`
- `benchmark_calls.png`
- `benchmark_weight.png`
- `benchmark_length.png`
- `benchmark_time_per_call.png`
- `benchmark_backtracking_time_vs_calls.png`
- `benchmark_quality_ratio.png`
- `benchmark_boxplot_times.png`
- `benchmark_boxplot_weights.png`
- `benchmark_edge_weight_histogram.png`
- `benchmark_branch_and_bound_runtime.png`
- `benchmark_branch_and_bound_calls.png`
- `benchmark_branch_and_bound_weight.png`
- `benchmark_branch_and_bound_pruning.png`

---

## Resumo curto das abordagens

- **Backtracking:** explora todos os caminhos simples e garante a solução ótima, mas cresce rapidamente em custo computacional.
- **Heurística gulosa:** é muito rápida, mas não garante ótimo global.
- **Branch and bound:** mantém a garantia de otimalidade e reduz o número de estados explorados por meio de poda.

---

## Estrutura do projeto

```text
benchmark.py
pyproject.toml
README.md
src/
  passeio_turistico_maximo/
    __init__.py
    __main__.py
    algorithm.py
    cli.py
tests/
  test_algorithm.py
  test_weighted_algorithm.py
```

---

## Referências

- Garey, M. R. and Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness.* W. H. Freeman, San Francisco.
- Skiena, S. S. (1998). *The Algorithm Design Manual.* Springer, New York.
 
