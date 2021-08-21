import pika, sys, os, json
from random import randrange

# FORMATO DAS MENSAGENS:
# JOIN = {'type': 'join', 'node_id': 'node_id'}
# LEAVE = {'type': 'leave', 'node_id': 'node_id'}


class Node:
    def __init__(self):
        self.id = randrange(0, 2**32)
        self.prev = None
        self.next = None
        self.data = []
        self.connection = None
        self.channel = None

    # Publish and subscribe to the queue
    def join(self):

        # Se conecta ao broker
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Declara a queue DHT
        self.channel.queue_declare(queue='dht',durable=True)

        # Se publica no broker
        data = { 'type': 'join', 'node_id': self.id }
        self.channel.basic_publish(exchange='', routing_key='dht', body=json.dumps(data))
        print(f"Entrou no broker.")

        # Se inscreve no broker
        self.channel.basic_consume(on_message_callback=self.callback, queue='dht')
        self.channel.start_consuming()


    # Sai do broker
    def leave(self):
        data = { 'type': 'leave', 'node_id': self.id }
        self.channel.basic_publish(exchange='', routing_key='dht', body=json.dumps(data))
        print(f"Saiu do broker.")
        self.channel.stop_consuming()


    # Consome mensagens do broker
    def callback(self,ch, method, properties, body):
        data = json.loads(body)

        # Se recebe um join
        if (data['type'] == 'join' and data['node_id']):
            self.process_join(data['node_id'])

        # Se recebe um leave
        elif (data['type'] == 'leave'):
            try:
                print(f"Received {data['type']} from {data['node_id']}")
            except:
                print("Formato incorreto")

        # Se recebe um forma incorreto
        else:
            print("Formato incorreto")

    # Processa um join
    def process_join(self,id):
        if (id == self.id): return
        
        print(f"Received join from {id}")
        if (id > self.id):
            if (self.next is None or id < self.next):
                self.next = id
                print(f"{self.prev} - {self.id} - {self.next}")
        elif (self.prev is None or id > self.prev):
            self.prev = id
            print(f"{self.prev} - {self.id} - {self.next}")

if __name__ == '__main__':
    try:
        node = Node()
        node.join()
    except KeyboardInterrupt:
        if node:
            node.leave()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)