import pika, sys, os, json
from random import randrange

# FORMATO DAS MENSAGENS:

# JOIN = {'type': 'join', 'node_id': 'node_id'}
# LEAVE = {'type': 'leave', 'node_id': 'node_id'}

# PUT = {'type': 'put', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}
# PUTOK = {'type': 'putok', 'key': 'key'}

# GET = {'type': 'get', 'key': 'key', 'node_id': 'node_id'}
# GETOK = {'type': 'getok', 'key': 'key', 'value': 'value'}

class Node:
    def __init__(self):
        self.id = randrange(0, 2**32)
        self.nodes = [self.id]
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

        # Declara a sua Queue
        result = self.channel.queue_declare(queue='', durable=True)
        queue = result.method.queue

        # Declara as exchanges
        self.channel.exchange_declare(exchange='config_individual', exchange_type='direct')
        self.channel.exchange_declare(exchange='config', exchange_type='fanout')
        self.channel.exchange_declare(exchange='dht', exchange_type='fanout')

        # Se publica no broker
        data = { 'type': 'join', 'node_id': self.id, 'confirm': 0 }
        self.channel.basic_publish(exchange='config', routing_key='', body=json.dumps(data))
        print(f"Entrou no broker ({self.id}).")

        # Se inscreve no broker
        self.channel.queue_bind(exchange='dht', queue=queue)
        self.channel.queue_bind(exchange='config', queue=queue)
        self.channel.queue_bind(exchange='config_individual', queue=queue, routing_key=str(self.id))
        self.channel.basic_consume(on_message_callback=self.callback, queue=queue)
        self.channel.start_consuming()


    # Sai do broker
    def leave(self):
        data = { 'type': 'leave', 'node_id': self.id }
        self.channel.basic_publish(exchange='config', routing_key='', body=json.dumps(data))
        print(f"Saiu do broker.")
        self.channel.stop_consuming()


    # Consome mensagens do broker
    def callback(self,ch, method, properties, body):
        data = json.loads(body)

        # Se recebe um join
        if (data['type'] == 'join' and data['node_id']):
            if 'confirm' in data and data['confirm'] == 1:
                self.process_join(data['node_id'], True)
            else:
                self.process_join(data['node_id'])

        # Se recebe um leave
        elif (data['type'] == 'leave' and data['node_id']):
            self.process_leave(data['node_id'])

        # Se recebe um put
        elif (data['type'] == 'put' and data['key'] and data['value']):
            if (int(data['key']) >= self.id and int(data['key']) < self.next):
                self.data.append((data['key'], data['value']))
                r_data = { 'type': 'putok', 'key': data['key'] }
                self.channel.basic_publish(exchange='dht', routing_key=str(data['node_id']), body=json.dumps(r_data))
                print(f"Received put from {data['key']}")

        # Se recebe um get
        elif (data['type'] == 'get' and data['key']):
            if (int(data['key']) >= self.id and int(data['key']) < self.next):
                k = data['key']
                v = self.data[k] if k in self.data else None
                r_data = { 'type': 'getok', 'key': k, 'value': v }
                self.channel.basic_publish(exchange='dht', routing_key=str(data['node_id']), body=json.dumps(r_data))
                print(f"Received get from {data['key']}")

    # Processa um join
    def process_join(self,id,confirm=False):
        if (id == self.id): return
        
        print(f"Received join from {id}")
        if not confirm:
            data = { 'type': 'join', 'node_id': self.id, 'confirm': 1 }
            self.channel.basic_publish(exchange='config_individual', routing_key=str(id), body=json.dumps(data))

        self.nodes.append(int(id))
        self.reorder_nodes()

    # Processa um leave
    def process_leave(self,id):
        idx = self.nodes.index(id)
        self.nodes.pop(idx)
        self.reorder_nodes()
        print(f"Received leave from {id}")

    # Reordena os nós da lista
    def reorder_nodes(self):
        self.nodes.sort()
        idx = self.nodes.index(self.id)
        self.prev = self.nodes[idx-1] if idx > 0 else self.nodes[-1]
        self.next = self.nodes[idx+1] if idx < len(self.nodes)-1 else self.nodes[0]

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