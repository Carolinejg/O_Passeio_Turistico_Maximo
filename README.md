# Passeio Turístico Máximo (Backtracking)

**Desenvolvido por Caroline Souza**

Este repositório contém a implementação e análise experimental de uma abordagem de **backtracking exaustivo** para o problema do **Passeio Turístico Máximo** em grafos completos ponderados.

O foco principal é estudar o comportamento do algoritmo em instâncias geradas aleatoriamente com pesos entre `1` e `100` e comparar métricas como tempo de execução, chamadas recursivas, peso do caminho e tamanho do caminho.

---

## 🚀 Destaques Técnicos

- **Backtracking (DFS recursivo):** busca exaustiva de todos os caminhos simples de `start` até `end` em grafos completos ponderados.
- **Geração de instâncias:** grafos completos com pesos randômicos entre `1` e `100` para `n = 5, 8, 10, 12, 15`.
- **Métricas coletadas:** tempo de execução, número de chamadas recursivas, peso do caminho encontrado e tamanho do caminho.
- **Benchmark automático:** script que gera gráficos de desempenho e qualidade para análise.

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

- `src/passeio_turistico_maximo/algorithm.py` — implementa a geração de grafos completos ponderados, o algoritmo de backtracking e funções auxiliares de métrica.
- `src/passeio_turistico_maximo/cli.py` — interface de linha de comando para rodar o algoritmo em instâncias geradas.
- `benchmark.py` — executa experimentos e gera gráficos para as métricas coletadas.
- `tests/` — testes unitários para validação do algoritmo e geração de grafos.

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

### Executar o benchmark e gerar gráficos

```powershell
python benchmark.py
```

Os gráficos gerados são:

- `benchmark_runtime.png`
- `benchmark_calls.png`
- `benchmark_weight.png`
- `benchmark_length.png`

---

## 📝 Observações sobre a abordagem

- O algoritmo atual utiliza **backtracking exaustivo** e não aplica podas heurísticas.
- A geração de pesos é determinística quando a mesma semente (`--seed`) é utilizada.
- O tempo de execução pode variar entre máquinas, mas as métricas de caminho e o número de chamadas recursivas são repetíveis para a mesma instância.

---

## 📚 Referências

- Garey, M. R. and Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness.* W. H. Freeman, San Francisco.
- Skiena, S. S. (1998). *The Algorithm Design Manual.* Springer, New York.
 
