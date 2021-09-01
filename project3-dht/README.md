# DHT
## Distributed Hash Table

### Estrutura

O arquivo `node.py` implementa a classe `Node`, que representa um nó da DHT. Ele pode ser executado através do comando `python3 node.py` e o nó será inicializado e fará join automaticamente. Caso a DHT não exista, ela passa a existir com apenas este nó.

O arquivo `user.py` implementa a classe `NodeUser`, que representa um cliente da DHT. Ele pode ser executado através do comando `python3 user.py` e o usuário será inicializado, enviará um valor aleatório para a DHT e solicitará o mesmo valor após 5 segundos, encerrando sua execução.

### Teste

Para inicializar uma DHT com 8 nós, basta executar o comando `python3 dht.py`. Todos os nós serão inicalializados em processos diferentes e farão seus joins e sincronização. Você pode encerrar a execução de toda a DHT com a interrupção `Ctrl + C`.

A partir da DHT inicializada, um script de testes pode ser executado com o comando `python3 test.py`. Ele inicializará 1000 clientes que farão, cada um, o put de um par chave-valor e o get da mesma chave logo em seguida. Caso um erro aconteça, o cliente printará a mensagem "ERRO!!!" no terminal.

### Simulação

Para testar a integridade da DHT, inicializou-se a mesma com 8 nós e executou-se 5 instâncias consecultivas do script de testes, em terminais diferentes, totalizando 5000 clientes, sendo 5 execuções paralelas de 1000 clientes consumindo de forma procedural. Nenhum dos testes realizados retornou erro.
