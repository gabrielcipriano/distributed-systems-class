import asyncio
import grpc
from time import time
from statistics import mean, median, pstdev
import hashtable_pb2
import hashtable_pb2_grpc

from multiprocessing import Pool, Process

def runGrpcSyncList(keys, values) -> None:
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hashtable_pb2_grpc.HashtableStub(channel)
        for key, value in zip(keys, values):
            stub.put(hashtable_pb2.putRequest(key=key, value=value))
            response = stub.get(hashtable_pb2.getRequest(key=key))
            if(response.value != value):
                print("ERRO: Valor do servidor não era o esperado", response.value, value)

if __name__ == '__main__':

    tempo = []

    m = 10000
    n_process = 4
    keys = []
    values = []

    # gera os valores
    for i in range(m):
        keys.append(str(i))
        values.append(i)

    sz = m//n_process

    processos = [None] * n_process
    for t in range(5):
        start = time()
        for i in range(n_process):
            processos[i] = Process(target=runGrpcSyncList, args=(keys[i*sz:(i+1)*sz-1], values[i*sz:(i+1)*sz-1]))
            processos[i].start()
        
        for p in processos:
            p.join()

        tempo.append(time() - start)
        print(f"Tempo({t}): ", tempo[t])

    print(f"\n{n_process} processos:")
    print(f"Média: {mean(tempo)}")
    print(f"Mediana: {median(tempo)}")
    print(f"Desvio Padrão: {pstdev(tempo)}")


    # print("Acabou.")
