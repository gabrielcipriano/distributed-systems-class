# DHT
## Distributed Hash Table

Trabalho implementado utilizando a biblioteca Pika, que é uma client library RabbitMQ

Vídeo de apresentação: [https://youtu.be/wZ_UKRfIQsg](https://youtu.be/wZ_UKRfIQsg)

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
JOIN = {'type': 'join', 'node_id': 'node_id'}
LEAVE = {'type': 'leave', 'node_id': 'node_id'}

PUT = {'type': 'put', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}
PUTOK = {'type': 'putok', 'key': 'key', 'node_id': 'node_id'}

GET = {'type': 'get', 'key': 'key', 'node_id': 'node_id'}
GETOK = {'type': 'getok', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}
```

### Teste

Para inicializar a DHT, basta que exista ao menos um nó inicializado que a componha (isto é, `n = Node()` e `n.join()`). O script `node.py` inicializa um nó e direciona o SIGINT (`Ctrl + C`) para a função de desligar o nó da DHT (isto é, `n.leave()`).

Alternativamente você pode inicializar uma DHT com 8 nós executando o script `dht.py`. Todos os nós serão inicializados em processos diferentes e a interrupção `Ctrl + C` remove todos os nós da DHT de uma só vez. 

A partir da DHT inicializada, pode-se inicializar usuários a partir do script `user.py`, que cria um nó, faz o `put` de um valor aleatório e após 5 segundos faz o `get` do mesmo valor, encerrando a execucão. 

Alternativamente você pode utilizar o script `test.py` para inicializar um usuário e realizar a inserção de 1000 valores aleatórios, seguida da recuperação destes valores após o comando do usuário. Durante a recuperação, o script checa se os valores estão corretos e gera erro na saída padrão caso negativo.

O número de clientes e operações que o script de teste executará bem como o modo verboso pode ser facilmente alterado, bastando abrir o script `test.py` e alterar as seguintes variáveis conforme interesse:

`n_users = 1`
`n_operations = 1000 #each`
`verbose = False `

O modo verboso nos scripts `dht.py` e `test.py` estão desativados por padrão, ative se achar necessário.

### Simulação

A simulação pode ser conferida no [vídeo de apresentação](https://youtu.be/wZ_UKRfIQsg) a partir do tempo 6:32.

Durante o processo foi utilizada uma DHT com 3 nós, inseridos e removidos em momentos distintos para que se conferisse a redistribuição dos valores. Para os clientes foi utilizado o script individual (onde 1 cliente inseriu 1 valor) e o de testes (onde 2 clientes inseriram 1000 valores cada).

Em todas as simulações não houveram erros.
