# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from evals.utils.api.talk import talk_pb2 as talk__pb2


class TalkStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamingTalk = channel.stream_stream(
                '/svpb.Talk/StreamingTalk',
                request_serializer=talk__pb2.TalkRequest.SerializeToString,
                response_deserializer=talk__pb2.TalkResponse.FromString,
                )


class TalkServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StreamingTalk(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TalkServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StreamingTalk': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamingTalk,
                    request_deserializer=talk__pb2.TalkRequest.FromString,
                    response_serializer=talk__pb2.TalkResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'svpb.Talk', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Talk(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StreamingTalk(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/svpb.Talk/StreamingTalk',
            talk__pb2.TalkRequest.SerializeToString,
            talk__pb2.TalkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
