# O_Passeio_Turistico_Maximo

Este projeto implementa uma abordagem de backtracking para o problema do Passeio Turístico Máximo em grafos completos ponderados.

## Estrutura do projeto

- `src/passeio_turistico_maximo/algorithm.py`: geração de grafos completos ponderados e busca por backtracking com contagem de chamadas recursivas.
- `src/passeio_turistico_maximo/cli.py`: interface de linha de comando para rodar a busca em instâncias geradas.
- `benchmark.py`: benchmark de tempos e número de chamadas recursivas para `n = 5, 8, 10, 12, 15`.
- `tests/`: testes automatizados.

## Como executar a busca por backtracking

1. Instale o pacote no modo editável:

```powershell
pip install -e .
```

2. Execute a busca para um grafo completo de tamanho `n`:

```powershell
python -m passeio_turistico_maximo 5 --seed 42 --start v0 --end v4
```

- `n` deve ser um dos valores: `5, 8, 10, 12, 15`
- `--seed` define a semente para a geração de pesos aleatórios entre `1` e `100`
- `--start` e `--end` definem o vértice de origem e destino

## Benchmark

Para gerar gráficos de desempenho e chamadas recursivas:

```powershell
python benchmark.py
```

O benchmark mede:

- tempo médio de execução da busca por backtracking
- número médio de chamadas recursivas

Se `matplotlib` estiver instalado, ele salva dois arquivos:

- `benchmark_runtime.png`
- `benchmark_calls.png`

Caso não tenha `matplotlib`, instale com:

```powershell
pip install matplotlib
```
 
