import pika, sys, os, json
from random import randrange
from time import sleep

# FORMATO DAS MENSAGENS:

# PUT = {'type': 'put', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}
# PUTOK = {'type': 'putok', 'key': 'key'}

# GET = {'type': 'get', 'key': 'key', 'node_id': 'node_id'}
# GETOK = {'type': 'getok', 'key': 'key', 'value': 'value'}

class NodeUser:
    def __init__(self):
        self.id = randrange(0, 2**32)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.retorno = None

        # Declara a Queue DHT e a Exchanges
        result = self.channel.queue_declare(queue='', exclusive=True, durable=True)
        self.channel.exchange_declare(exchange='dht', exchange_type='fanout')

        self.queue = result.method.queue

    # Envia um par chave-valor para o broker
    def put(self,key,value):
        self.subscribe()
        # Publica o par chave-valor
        data = { 'type': 'put', 'key': key, 'value': value, 'node_id': self.id }
        self.channel.basic_publish(exchange='dht', routing_key='', body=json.dumps(data))
        # Consome
        self.channel.start_consuming()

    # Recupera um par chave-valor do broker
    def get(self,key):
        self.subscribe()
        # Publica o get com a chave
        data = { 'type': 'get', 'key': key, 'node_id': self.id }
        self.channel.basic_publish(exchange='dht', routing_key='', body=json.dumps(data))
        # Consome
        self.channel.start_consuming()
        return self.retorno

    # Consome mensagens do broker
    def callback(self,ch, method, properties, body):
        data = json.loads(body)
        if (method.routing_key != str(self.id)): return

        # Se recebe um putok
        if (data['type'] == 'putok' and data['key']):
            print(f"Key {data['key']} armazenada.")
            self.channel.stop_consuming()

        # Se recebe um getok
        elif (data['type'] == 'getok' and data['key'] and data['value']):
            print(f"Key {data['key']} = {data['value']}")
            self.retorno = data['value']
            self.channel.stop_consuming()

    def subscribe(self):
        # Se inscreve no broker (na sua propria rota)
        self.channel.queue_bind(exchange='dht', queue=self.queue, routing_key=str(self.id))
        self.channel.basic_consume(on_message_callback=self.callback, queue=self.queue)


if __name__ == '__main__':
    try:
        node = NodeUser()
        key = randrange(0, 2**32)
        node.put(key, 'VALOR')
        sleep(5)
        node.get(key)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)