import pika, sys, os, json
from random import randrange
from user import NodeUser
import time

# FORMATO DAS MENSAGENS:

# JOIN = {'type': 'join', 'node_id': 'node_id'}
# LEAVE = {'type': 'leave', 'node_id': 'node_id'}

# PUT = {'type': 'put', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}
# PUTOK = {'type': 'putok', 'key': 'key', 'node_id': 'node_id'}

# GET = {'type': 'get', 'key': 'key', 'node_id': 'node_id'}
# GETOK = {'type': 'getok', 'key': 'key', 'value': 'value', 'node_id': 'node_id'}

MAX_INT_ID = 2**32
# MAX_INT_ID = 1000

class Node:
    def __init__(self, verbose=True):
        self.id = randrange(0, MAX_INT_ID)
        self.nodes = [self.id]
        self.prev = None
        self.next = None
        self.data = {}
        self.connection = None
        self.channel = None
        self.verbose = verbose

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

        # Se inscreve no broker
        self.channel.queue_bind(exchange='dht', queue=queue)
        self.channel.queue_bind(exchange='config', queue=queue)
        self.channel.queue_bind(exchange='config_individual', queue=queue, routing_key=str(self.id))
        self.channel.basic_consume(on_message_callback=self.callback, queue=queue)

        # Se publica no broker
        data = { 'type': 'join', 'node_id': self.id, 'confirmation': 0 }
        self.channel.basic_publish(exchange='config', routing_key='', body=json.dumps(data))
        print(f"Entrou no broker ({self.scn(self.id)}).")

        # Inicia o consumo
        self.channel.start_consuming()


    # Sai do broker
    def leave(self):
        data = { 'type': 'leave', 'node_id': self.id, 'confirmation': 0 }
        self.channel.basic_publish(exchange='config', routing_key='', body=json.dumps(data))
        if len(self.nodes) > 1:
            self.channel.start_consuming()
        print(f"Node {self.id}: Left the network.")

    def is_in_range(self, key):
        if len(self.nodes) == 1:
            return True
        return ( 
            key >= self.id and key < self.next
            if (self.id < self.next)
            else key >= self.id or key < self.next
        )
        
    # Consome mensagens do broker
    def callback(self,ch, method, properties, body):
        data = json.loads(body)

        # Se recebe um join
        if (data['type'] == 'join' and 'node_id' in data):
            if 'confirmation' in data and data['confirmation'] == 1:
                self.process_join(data['node_id'], True)
            else:
                self.process_join(data['node_id'])

        # Se recebe um leave
        elif (data['type'] == 'leave' and 'node_id' in data):
            if 'confirmation' in data and data['confirmation'] == 1:
                self.process_leave(data['node_id'], True)
            else:
                self.process_leave(data['node_id'])

        # Se recebe um put
        elif (data['type'] == 'put' and 'key' in data and type(data['key']) is int and 'value' in data):
            if self.is_in_range(int(data['key'])):
                self.data[data['key']] = data['value']
                r_data = { 'type': 'putok', 'key': data['key'], 'node_id': self.id }
                self.channel.basic_publish(exchange='dht', routing_key=str(data['node_id']), body=json.dumps(r_data))
                if self.verbose: print(f"Received put from {self.scn(data['key'])}")

        # Se recebe um get
        elif (data['type'] == 'get' and 'key' in data and type(data['key']) is int):
            if self.is_in_range(int(data['key'])):
                k = data['key']
                v = self.data[k] if k in self.data else None
                r_data = { 'type': 'getok', 'key': k, 'value': v, 'node_id': self.id }
                self.channel.basic_publish(exchange='dht', routing_key=str(data['node_id']), body=json.dumps(r_data))
                if self.verbose: print(f"Received get from {self.scn(data['key'])}")

    # Processa um join
    def process_join(self,id,confirmation=False):
        if (id == self.id): return
        
        self.nodes.append(int(id))
        self.reorder_nodes()

        print(f"Node {self.id}: Received join from {self.scn(id)}")
        if not confirmation:
            data = { 'type': 'join', 'node_id': self.id, 'confirmation': 1 }
            self.channel.basic_publish(exchange='config_individual', routing_key=str(id), body=json.dumps(data))
            if id == self.next:
                repostKeys = [ key for key in self.data.keys() if not self.is_in_range(key) ]
                self.repostValues(repostKeys)
                
    def repostValues(self,keys):
        node = keys and NodeUser()
        for key in keys:
            print(f"Reposting {key}")
            node.put(key, self.data.pop(key))

    # Processa um leave
    def process_leave(self,id,confirmation=False):
        idx = self.nodes.index(id)
        self.nodes.pop(idx)
        if id == self.id: return

        if not confirmation:
            data = { 'type': 'leave', 'node_id': self.id, 'confirmation': 1 }
            self.channel.basic_publish(exchange='config_individual', routing_key=str(id), body=json.dumps(data))
            self.reorder_nodes()
            print(f"Received leave from {self.scn(id)}")
        else: # confirmation
            print(f"Node {self.id}: Received leave confirmation from {self.scn(id)}")
            
            if not self.nodes:
                self.channel.stop_consuming()
                repostKeys = list(self.data.keys())
                self.repostValues(repostKeys)
                self.connection.close()

    # Reordena os nós da lista
    def reorder_nodes(self):
        self.nodes.sort()
        idx = self.nodes.index(self.id)
        self.prev = self.nodes[idx-1] if idx > 0 else self.nodes[-1]
        self.next = self.nodes[idx+1] if idx < len(self.nodes)-1 else self.nodes[0]

    def scn(self,n):
        # return n
        return "{:e}".format(int(n))

if __name__ == '__main__':
    try:
        node = Node()
        node.join()

    except:
        if node:
            node.leave()
            print('Interrupted')