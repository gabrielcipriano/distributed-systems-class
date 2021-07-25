import logging
import asyncio
import grpc

import hashtable_pb2
import hashtable_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = hashtable_pb2_grpc.HashtableStub(channel)
        response = await stub.put(hashtable_pb2.putRequest(key='2', value=2))
    print(f"Put client received: {response.ok}")

    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = hashtable_pb2_grpc.HashtableStub(channel)
        response = await stub.get(hashtable_pb2.getRequest(key='2'))
    print(f"Get client received: {response.value}")


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())