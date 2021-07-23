# Middleware gRPC

## Python

### Instale os módulos necessários:
```shell
pip install -r requirements.txt
```

### Para utilizar:
- Execute o servidor;
- Defina o número de valores e de processos no arquivo "client.py";
- Execute o cliente;

### Resultados
Testes utilizando 1000 inteiros:
- 8 processos: 4.40s
- 4 processos: 3.44s
- 2 processos: 2.27s
- 1 processo:  1.93s