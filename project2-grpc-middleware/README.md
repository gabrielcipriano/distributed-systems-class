# Middleware gRPC

### Resultados dos testes

O script foi executado 10 vezes em um computador com processador ARM 8-core (Apple M1) e os resultados podem ser observados abaixo:

| Nº de Threads |    1    |    2    |    4    |    8    |
| ------------- | ------- | ------- | ------- | ------- |
|     Média     | 6.83620 | 3.87353 | 2.95023 | 2.87331 |
|    Mediana    | 6.76131 | 3.87214 | 2.97024 | 2.85702 |
|  Desv. Padrão | 0.12837 | 0.03846 | 0.08285 | 0.07714 |

<p align="left">
  <img src="results.png" width="500" title="Resultados">
</p>
