import asyncio
import grpc
from time import time
from statistics import mean, median, pstdev
import hashtable_pb2
import hashtable_pb2_grpc

from multiprocessing import Pool

async def runGrpc(key: str, value: int) -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = hashtable_pb2_grpc.HashtableStub(channel)
        await stub.put(hashtable_pb2.putRequest(key=key, value=value))
        response = await stub.get(hashtable_pb2.getRequest(key=key))
        if(response.value != value):
            print("ERRO: Valor do servidor não era o esperado", response.value, value)

def runGrpcSync(par) -> None:
    key, value = par
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hashtable_pb2_grpc.HashtableStub(channel)
        stub.put(hashtable_pb2.putRequest(key=key, value=value))
        response = stub.get(hashtable_pb2.getRequest(key=key))
        if(response.value != value):
            print("ERRO: Valor do servidor não era o esperado", response.value, value)



def runGrpc_sync(par) -> None:
    key, value = par
    asyncio.run(runGrpc(key, value))
    return value

if __name__ == '__main__':

    tempo = []

    m = 10000
    processos = 1
    keys = []
    values = []

    # gera os valores
    for i in range(m):
        keys.append(str(i))
        values.append(i)

    p = Pool(processes=processos)
    for i in range(5):
        start = time()
        # result = p.map(runGrpc_sync, zip(keys, values))
        result = p.map(runGrpcSync, zip(keys, values))
        tempo.append(time() - start)
        print(f"Tempo({i}): ", tempo[i])
    p.close()
    p.join()

    print(f"\n{processos} processos:")
    print(f"Média: {mean(tempo)}")
    print(f"Mediana: {median(tempo)}")
    print(f"Desvio Padrão: {pstdev(tempo)}")


    # print("Acabou.")
