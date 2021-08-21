import pika, sys, os, json
from random import randrange
from node_dht import Node

def main():

    # Entra no broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Limpa a fila de mensagens
    channel.queue_delete(queue='dht')

    # Cria uma nova fila de mensagens
    channel.queue_declare(queue='dht', durable=True)

    # Inicializa os nós
    # Falta colocar cada um em uma thread ou processo
    nodes = [ Node() for _ in range(8) ] 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)