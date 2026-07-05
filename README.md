# Passeio Turístico Máximo

**Desenvolvido por Caroline Souza**

Este projeto implementa e compara três abordagens para o problema do **Passeio Turístico Máximo** em grafos completos ponderados:

- **Backtracking exaustivo**, que busca a solução ótima entre `start` e `end`.
- **Heurística gulosa**, que escolhe localmente a aresta de maior peso a cada passo.
- **Branch and bound**, que aplica poda para reduzir o espaço de busca sem alterar a solução final.

---

## Visão geral do projeto

As instâncias são geradas aleatoriamente com pesos inteiros entre `1` e `100`. O objetivo é comparar tempo de execução, chamadas recursivas, peso do caminho e tamanho do caminho entre as abordagens.

## Execução dos experimentos

### Executar o algoritmo de backtracking

Use a CLI para gerar um grafo completo ponderado e rodar a busca de `start` até `end`:

```powershell
python -m passeio_turistico_maximo 5 --seed 42 --start v0 --end v4
```

Explicação dos parâmetros:

- `5`: número de vértices do grafo completo. Os valores suportados são `5`, `8`, `10`, `12` e `15`.
- `--seed 42`: semente para o gerador de números aleatórios.
- `--start v0`: vértice de partida para a busca.
- `--end v4`: vértice de destino para a busca.

Exemplo de saída esperada:

```text
Grafo completo com 5 nós
Início: v0, Destino: v4
Pesos de arestas:
v0 {'v1': 82, 'v2': 15, 'v3': 4, 'v4': 95}
v1 {'v0': 36, 'v2': 32, 'v3': 29, 'v4': 18}
v2 {'v0': 95, 'v1': 14, 'v3': 87, 'v4': 28}
v3 {'v0': 94, 'v1': 13, 'v2': 86, 'v4': 48}
v4 {'v0': 14, 'v1': 20, 'v2': 24, 'v3': 71}

Melhor caminho por backtracking (S→D):
v0 -> v4
Peso total: 95
```

> Os valores acima são ilustrativos. A saída real depende da semente e da implementação exata do gerador.

## Diferença entre CLI e benchmark

- A CLI serve para testar um caso específico com `n`, `seed`, `start` e `end` definidos.
- O benchmark serve para medir desempenho e qualidade em várias instâncias.
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

- `benchmark.py` — script de benchmark que executa experimentos, coleta métricas e gera gráficos de desempenho e qualidade.
- `pyproject.toml` — configuração do pacote Python, metadados do projeto e definição de dependências e entrada CLI.
- `README.md` — documentação do projeto, instruções de uso e explicação das métricas e dos resultados.
- `src/passeio_turistico_maximo/__init__.py` — exporta a API do pacote e permite a instalação como módulo Python.
- `src/passeio_turistico_maximo/__main__.py` — torna o pacote executável com `python -m passeio_turistico_maximo`.
- `src/passeio_turistico_maximo/algorithm.py` — gera grafos completos ponderados e implementa o algoritmo de backtracking com métricas.
- `src/passeio_turistico_maximo/cli.py` — define a interface de linha de comando para executar o algoritmo em instâncias geradas.
- `tests/test_algorithm.py` — testes de unidade para validar a lógica de caminho em grafos simples.
- `tests/test_weighted_algorithm.py` — testes de unidade para validar a geração de grafos ponderados e métricas do backtracking.

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
 
