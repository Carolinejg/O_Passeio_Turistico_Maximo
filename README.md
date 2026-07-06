# Passeio Turístico Máximo

**Desenvolvido por Caroline Souza**

Este projeto implementa e compara três abordagens para o problema do **Passeio Turístico Máximo** em grafos completos ponderados:

- **Backtracking exaustivo**, que busca a solução ótima entre `start` e `end`.
- **Heurística gulosa**, que escolhe localmente a aresta de maior peso a cada passo.
- **Branch and bound**, que aplica poda para reduzir o espaço de busca sem alterar a solução final.

---

## Visão geral do projeto

As instâncias são geradas aleatoriamente com pesos inteiros entre `1` e `100`. O objetivo é comparar tempo de execução, chamadas recursivas, peso do caminho e tamanho do caminho entre as abordagens.

## Execução

### Pré-requisitos

- Python 3.11+
- `pip`

### CLI

Use a interface de linha de comando para executar uma instância específica do problema:

```powershell
python -m passeio_turistico_maximo 5 --seed 42 --start v0 --end v4
```

Esse comando gera um grafo completo ponderado, executa a busca e exibe o caminho encontrado com o respectivo peso total.

### Benchmark

```powershell
python benchmark.py
```

Esse é o script principal de experimentação. Ele roda múltiplas instâncias, coleta métricas e gera os gráficos comparativos do relatório.

### CLI x Benchmark

- A CLI serve para testar um caso específico com `n`, `seed`, `start` e `end` definidos.
- O benchmark serve para avaliar desempenho e qualidade em várias instâncias.
- A CLI mostra o resultado de uma execução isolada.
- O benchmark coleta métricas e salva os gráficos automaticamente.

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

### Descrição dos arquivos principais

- `benchmark.py` — script de benchmark que executa experimentos, coleta métricas e gera gráficos de desempenho, qualidade e comparação entre as abordagens.
- `pyproject.toml` — configuração do pacote Python, metadados do projeto e definição de dependências e entrada CLI.
- `README.md` — documentação do projeto, instruções de uso e explicação das métricas e dos resultados.
- `src/passeio_turistico_maximo/__init__.py` — exporta a API do pacote e permite a instalação como módulo Python.
- `src/passeio_turistico_maximo/__main__.py` — torna o pacote executável com `python -m passeio_turistico_maximo`.
- `src/passeio_turistico_maximo/algorithm.py` — gera grafos completos ponderados e implementa as abordagens de backtracking, heurística gulosa e branch and bound com métricas.
- `src/passeio_turistico_maximo/cli.py` — define a interface de linha de comando para executar o algoritmo em instâncias geradas.
- `tests/test_algorithm.py` — testes de unidade para validar a lógica de caminho em grafos simples e compatibilidade com a API principal.
- `tests/test_weighted_algorithm.py` — testes de unidade para validar a geração de grafos ponderados, a heurística gulosa e as métricas das buscas.

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

## Referências

- Cormen, T. H.; Leiserson, C. E.; Rivest, R. L.; Stein, C. (2009). *Introduction to Algorithms*. 3. ed. The MIT Press.
- Garey, M. R. and Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness.* W. H. Freeman, San Francisco.
- Skiena, S. S. (1998). *The Algorithm Design Manual.* Springer, New York.
 
