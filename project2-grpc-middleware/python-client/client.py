import asyncio
import grpc

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

def runGrpc_sync(par) -> None:
    key, value = par
    asyncio.run(runGrpc(key, value))
    return value

if __name__ == '__main__':
    m = 10000
    processos = 8
    keys = []
    values = []

    # gera os valores
    for i in range(m):
        keys.append(str(i))
        values.append(i)

    # executa a operacao
    with Pool(processos) as p:
        p.map_async(runGrpc_sync, zip(keys, values))
        p.close()
        p.join()

    # print("Acabou.")
