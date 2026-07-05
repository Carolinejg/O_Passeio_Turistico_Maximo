# Passeio Turístico Máximo (Backtracking + Heurística Gulosa)

**Desenvolvido por Caroline Souza**

Este repositório contém a implementação e análise experimental de duas abordagens para o problema do **Passeio Turístico Máximo** em grafos completos ponderados:

- **Backtracking exaustivo**, que busca o caminho ótimo entre `start` e `end`.
- **Heurística gulosa**, que escolhe localmente a aresta de maior peso a cada passo.

O foco principal é estudar o comportamento dessas abordagens em instâncias geradas aleatoriamente com pesos entre `1` e `100` e comparar métricas como tempo de execução, chamadas recursivas, peso do caminho e tamanho do caminho.

---

## 🚀 Destaques Técnicos

- **Backtracking (DFS recursivo):** busca exaustiva de todos os caminhos simples de `start` até `end` em grafos completos ponderados.
- **Heurística gulosa:** busca rápida que escolhe o próximo vértice com aresta de maior peso local até chegar em `end`.
- **Geração de instâncias:** grafos completos com pesos randômicos entre `1` e `100` para `n = 5, 8, 10, 12, 15`.
- **Métricas coletadas:** tempo de execução, número de chamadas recursivas, peso do caminho encontrado e tamanho do caminho.
- **Benchmark automático:** script que gera gráficos comparativos entre backtracking e guloso, além de métricas internas do backtracking.

---

## 📁 Estrutura do Projeto

```
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

## 🛠️ Configuração e Instalação

### Pré-requisitos

- Python 3.11+
- `pip`

### Instalação de dependências

```powershell
pip install -e .
pip install matplotlib
```

> `matplotlib` é opcional, mas necessário para gerar os gráficos do benchmark.

---

## 📊 Execução dos Experimentos

### Executar o algoritmo de backtracking

Use o CLI para gerar um grafo completo ponderado e rodar a busca de `start` até `end`:

```powershell
python -m passeio_turistico_maximo 5 --seed 42 --start v0 --end v4
```

Explicação dos parâmetros:

- `5`: número de vértices do grafo completo. Os valores suportados são `5`, `8`, `10`, `12` e `15`.
- `--seed 42`: semente para o gerador de números aleatórios. Mantém os pesos das arestas reproduzíveis entre execuções.
- `--start v0`: vértice de partida para a busca de backtracking. Neste caso, o início é o nó `v0`.
- `--end v4`: vértice de destino para a busca de backtracking. Neste caso, o alvo é o nó `v4`.

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

O comando gera um grafo completo com `n` vértices, apresenta a matriz de pesos das arestas e imprime o melhor caminho encontrado de `start` até `end` pelo algoritmo de backtracking.

### Diferença entre CLI e benchmark

- `python -m passeio_turistico_maximo ...` serve para testar um caso específico com `n`, `seed`, `start` e `end` definidos.
- Ele mostra a saída do algoritmo para essa instância, mas **não gera gráficos**.
- `python benchmark.py` serve para rodar várias instâncias e coletar métricas para os gráficos do relatório.
- Os gráficos são gerados pelo benchmark de forma independente dos parâmetros usados no CLI.


### Executar o benchmark e gerar gráficos

```powershell
python benchmark.py
```

Os gráficos gerados são:

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

## 📝 Abordagem com branch and bound

Além da versão clássica de backtracking e da heurística gulosa, o projeto também inclui uma variante baseada em **branch and bound**, concebida para reduzir o espaço de busca sem alterar a solução final. Nessa abordagem, a exploração recursiva é conduzida de forma semelhante ao backtracking, porém cada ramo é avaliado por meio de um limite superior estimado para o peso restante do caminho. Sempre que esse limite não puder superar a melhor solução já encontrada, o ramo é podado e não é mais explorado. Essa estratégia permite descartar porções do espaço de busca que não podem levar a uma melhoria, reduzindo significativamente o esforço computacional em instâncias maiores.

Na implementação adotada, o limite superior é obtido a partir de uma estimativa relaxada baseada nos maiores pesos disponíveis entre os vértices ainda não visitados. Embora essa estimativa não seja necessariamente exata, ela é suficiente para eliminar muitos ramos promissores de forma rápida. Como resultado, a versão com branch and bound preserva a corretude da solução, pois apenas ramos que não podem melhorar o valor atual são descartados, mas reduz de maneira expressiva o número de chamadas recursivas e o tempo de execução em relação ao backtracking puro.

Os gráficos adicionais gerados para essa abordagem são os seguintes:

- `benchmark_branch_and_bound_runtime.png`: compara o tempo de execução do backtracking puro com o branch and bound à medida que $n$ cresce. Os resultados mostram que a versão com podas é muito mais eficiente, especialmente para instâncias de tamanho intermediário e grande.
- `benchmark_branch_and_bound_calls.png`: apresenta a redução no número de chamadas recursivas quando a poda é aplicada. O gráfico evidencia que o branch and bound explora consideravelmente menos nós da árvore de busca do que o backtracking exaustivo.
- `benchmark_branch_and_bound_weight.png`: confirma que a solução encontrada pela abordagem com branch and bound preserva o mesmo peso ótimo do backtracking, demonstrando que a poda não compromete a corretude do algoritmo.
- `benchmark_branch_and_bound_pruning.png`: mostra o número médio de podas realizadas ao longo dos experimentos. O crescimento desse valor com $n$ ilustra o ganho obtido com a estratégia de eliminação de ramos inviáveis.

## 📝 Observações sobre a abordagem

- O algoritmo atual utiliza **backtracking exaustivo** e não aplica podas heurísticas.
- O benchmark também inclui uma **heurística gulosa** para comparação de qualidade e tempo.
- A heurística gulosa é mais rápida, mas não garante solução ótima porque faz escolhas locais sem considerar o caminho completo.
- A versão com **branch and bound** preserva a solução ótima, mas reduz o custo computacional por meio de poda baseada em limites superiores.
- A geração de pesos é determinística quando a mesma semente (`--seed`) é utilizada.
- O tempo de execução pode variar entre máquinas, mas as métricas de caminho e o número de chamadas recursivas são repetíveis para a mesma instância.

---

## 📚 Referências

- Garey, M. R. and Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness.* W. H. Freeman, San Francisco.
- Skiena, S. S. (1998). *The Algorithm Design Manual.* Springer, New York.
 
