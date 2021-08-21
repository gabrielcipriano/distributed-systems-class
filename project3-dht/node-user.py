import pika, sys, os, json
from random import randrange

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

        # Declara a Queue DHT e a Exchanges
        result = self.channel.queue_declare(queue='', exclusive=True, durable=True)
        self.channel.exchange_declare(exchange='dht', exchange_type='fanout')

        # Se inscreve no broker (na sua propria rota)
        self.channel.queue_bind(exchange='dht', queue=result.method.queue, routing_key=str(self.id))
        self.channel.basic_consume(on_message_callback=self.callback, queue=result.method.queue)

    # Envia um par chave-valor para o broker
    def put(self,key,value):
        data = { 'type': 'put', 'key': key, 'value': value, 'node_id': self.id }
        self.channel.basic_publish(exchange='dht', routing_key='', body=json.dumps(data))
        self.channel.start_consuming()

    # Recupera um par chave-valor do broker
    def get(self,key):
        data = { 'type': 'get', 'key': key, 'node_id': self.id }
        self.channel.basic_publish(exchange='dht', routing_key='', body=json.dumps(data))
        self.channel.start_consuming()

    # Consome mensagens do broker
    def callback(self,ch, method, properties, body):
        data = json.loads(body)

        # Se recebe um putok
        if (data['type'] == 'putok' and data['key']):
            print(f"Key {data['key']} armazenada.")
            self.channel.stop_consuming()

        # Se recebe um getok
        elif (data['type'] == 'getok' and data['key'] and data['value']):
            print(f"Key {data['key']} = {data['value']}")
            self.channel.stop_consuming()


if __name__ == '__main__':
    try:
        node = NodeUser()
        key = randrange(0, 2**32)
        node.put(key, 'VALOR')
        node.get(key)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)