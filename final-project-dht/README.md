# DHT
## Distributed Hash Table

Trabalho implementado utilizando a biblioteca Pika, que é uma client library RabbitMQ

### Preparação do Environment
Antes de executar qualquer script, instale as bibliotecas necessárias através do comando ```pip install -r requirements.txt``` ou ```pip3 install -r requirements.txt```

É importante também ter instalado o message broker [RabbitMQ](https://rabbitmq.com/download.html):
[https://rabbitmq.com/download.html](https://rabbitmq.com/download.html)

Certifique-se que o broker RabbitMQ está em execução.

### Estrutura

O arquivo `node.py` implementa a classe `Node`, que representa um nó da DHT. Ele pode ser executado através do comando `python3 node.py` e o nó será inicializado e fará join automaticamente. Caso a DHT não exista, ela passa a existir com apenas este nó.

O arquivo `user.py` implementa a classe `NodeUser`, que representa um cliente da DHT. Ele pode ser executado através do comando `python3 user.py` e o usuário será inicializado, enviará um valor aleatório para a DHT e solicitará o mesmo valor após 5 segundos, encerrando sua execução.

As classes `Node` e `NodeUser` possuem o parâmetro `verbose` que é `True` por default. Quando ativo, vai imprimir na saida padrão todas as operações de get/put realizadas. Quando desativado, somente informações importantes e erros são printados.

#### Formato das mensagens
O formato de mensagens escolhido foi JSON com uma estrutura inspirada em RPC:

```
JOIN  : {'type': 'join', 'node_id': 'node_id'}
LEAVE : {'type': 'leave', 'node_id': 'node_id'}

PUT   : {'type': 'put', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}
PUTOK : {'type': 'putok', 'key': 'key'}

GET   : {'type': 'get', 'key': 'key', 'node_id': 'node_id'}
GETOK : {'type': 'getok', 'key': 'key', 'value': 'value'}
```

### Teste

Para inicializar uma DHT com 8 nós, basta executar o comando `python3 dht.py`. Todos os nós serão inicializados em processos diferentes e farão seus joins e sincronização. Você pode encerrar a execução de toda a DHT com a interrupção `Ctrl + C`. O modo verboso 

A partir da DHT inicializada, um script de testes pode ser executado com o comando `python3 test.py`. Ele inicializará 5 clientes (threads) que farão, cada um, 500 operações de put e get de pares chave-valor aleatórios. Caso um erro aconteça, o cliente printará uma mensagem de erro na saída padrão.

O número de clientes e operações que o script de teste executará bem como o modo verboso pode ser facilmente alterado, basta abrir o script `test.py` e alterar as seguintes variáveis conforme interesse:

`n_users = 5`
`n_operations = 500 #each`
`verbose = False `

O modo verboso nos scripts `dht.py` e `test.py` estão desativados por padrão, ative se achar necessário.

### Simulação

Para testar a integridade da DHT, inicializou-se a mesma com 8 nós e executou-se o script de teste configurado para 10 clientes e 500 operações cada, totalizando 5000 operações. O teste levou 149.8 segundos e não obteve nenhum erro.
