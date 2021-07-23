#python3.9 -m grpc_tools.protoc -I . --python_out=./service-python --grpc_python_out=./service-python hashtable.proto

import grpc
import asyncio
import logging

import hashtable_pb2
import hashtable_pb2_grpc

class HashtableAIO(hashtable_pb2_grpc.HashtableServicer):
    hash_t = {}

    async def get(
        self, request: hashtable_pb2.getRequest,
        context: grpc.aio.ServicerContext) -> hashtable_pb2.getResponse:
        # LOGICA DE NEGOCIO
        if request.key in self.hash_t:
            return hashtable_pb2.getResponse(value=self.hash_t[request.key])
        return hashtable_pb2.getResponse(value=None)

    async def put(
            self, request: hashtable_pb2.putRequest,
            context: grpc.aio.ServicerContext) -> hashtable_pb2.putResponse:
        # LOGICA DE NEGOCIO
        if request.key in self.hash_t:
            return hashtable_pb2.putResponse(ok=False)
        self.hash_t[request.key] = request.value
        return hashtable_pb2.putResponse(ok=True)


async def serve() -> None:
    server = grpc.aio.server()
    hashtable_pb2_grpc.add_HashtableServicer_to_server(HashtableAIO(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())




class Greeter(helloworld_pb2_grpc.GreeterServicer):

    async def SayHello(
            self, request: helloworld_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

getrequest = hashtable_pb2.getRequest()
putrequest = hashtable_pb2.putRequest()

getrequest.key = "1"
getrequest.value = 1


