# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from connection.pb import tasks_pb2 as connection_dot_pb_dot_tasks__pb2


class TasksStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddUser = channel.unary_unary(
            "/pb.Tasks/AddUser",
            request_serializer=connection_dot_pb_dot_tasks__pb2.UserRequest.SerializeToString,
            response_deserializer=connection_dot_pb_dot_tasks__pb2.UserResponse.FromString,
        )
        self.ChangeUser = channel.unary_unary(
            "/pb.Tasks/ChangeUser",
            request_serializer=connection_dot_pb_dot_tasks__pb2.UserRequest.SerializeToString,
            response_deserializer=connection_dot_pb_dot_tasks__pb2.UserResponse.FromString,
        )
        self.DeleteUser = channel.unary_unary(
            "/pb.Tasks/DeleteUser",
            request_serializer=connection_dot_pb_dot_tasks__pb2.IDRequest.SerializeToString,
            response_deserializer=connection_dot_pb_dot_tasks__pb2.UserResponse.FromString,
        )


class TasksServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ChangeUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TasksServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "AddUser": grpc.unary_unary_rpc_method_handler(
            servicer.AddUser,
            request_deserializer=connection_dot_pb_dot_tasks__pb2.UserRequest.FromString,
            response_serializer=connection_dot_pb_dot_tasks__pb2.UserResponse.SerializeToString,
        ),
        "ChangeUser": grpc.unary_unary_rpc_method_handler(
            servicer.ChangeUser,
            request_deserializer=connection_dot_pb_dot_tasks__pb2.UserRequest.FromString,
            response_serializer=connection_dot_pb_dot_tasks__pb2.UserResponse.SerializeToString,
        ),
        "DeleteUser": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteUser,
            request_deserializer=connection_dot_pb_dot_tasks__pb2.IDRequest.FromString,
            response_serializer=connection_dot_pb_dot_tasks__pb2.UserResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pb.Tasks", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Tasks(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddUser(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pb.Tasks/AddUser",
            connection_dot_pb_dot_tasks__pb2.UserRequest.SerializeToString,
            connection_dot_pb_dot_tasks__pb2.UserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ChangeUser(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pb.Tasks/ChangeUser",
            connection_dot_pb_dot_tasks__pb2.UserRequest.SerializeToString,
            connection_dot_pb_dot_tasks__pb2.UserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def DeleteUser(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pb.Tasks/DeleteUser",
            connection_dot_pb_dot_tasks__pb2.IDRequest.SerializeToString,
            connection_dot_pb_dot_tasks__pb2.UserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
