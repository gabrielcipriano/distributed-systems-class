import pika, sys, os, json
from random import randrange
from node import Node
from multiprocessing import Process

verbose = False

processos = []

def run_node():
    node = Node(verbose=verbose)
    node.join()

def kill_nodes():
    for p in processos:
        p.terminate()

def main():
    for _ in range(8):
        p = Process(target=run_node)
        p.start()
        processos.append(p)
    for p in processos:
        p.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupting...')
        kill_nodes()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)