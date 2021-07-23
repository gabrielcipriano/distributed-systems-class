# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import hashtable_pb2 as hashtable__pb2


class HashtableStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.put = channel.unary_unary(
                '/tutorial.Hashtable/put',
                request_serializer=hashtable__pb2.putRequest.SerializeToString,
                response_deserializer=hashtable__pb2.putResponse.FromString,
                )
        self.get = channel.unary_unary(
                '/tutorial.Hashtable/get',
                request_serializer=hashtable__pb2.getRequest.SerializeToString,
                response_deserializer=hashtable__pb2.getResponse.FromString,
                )


class HashtableServicer(object):
    """Missing associated documentation comment in .proto file."""

    def put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HashtableServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'put': grpc.unary_unary_rpc_method_handler(
                    servicer.put,
                    request_deserializer=hashtable__pb2.putRequest.FromString,
                    response_serializer=hashtable__pb2.putResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=hashtable__pb2.getRequest.FromString,
                    response_serializer=hashtable__pb2.getResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tutorial.Hashtable', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Hashtable(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tutorial.Hashtable/put',
            hashtable__pb2.putRequest.SerializeToString,
            hashtable__pb2.putResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tutorial.Hashtable/get',
            hashtable__pb2.getRequest.SerializeToString,
            hashtable__pb2.getResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
