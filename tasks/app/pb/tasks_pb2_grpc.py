# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from app.pb import tasks_pb2 as app_dot_pb_dot_tasks__pb2


class TasksStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ConfirmEmail = channel.unary_unary(
            "/pb.Tasks/ConfirmEmail",
            request_serializer=app_dot_pb_dot_tasks__pb2.ConfirmEmailRequest.SerializeToString,
            response_deserializer=app_dot_pb_dot_tasks__pb2.ConfirmEmailResponse.FromString,
        )
        self.CheckPermission = channel.unary_unary(
            "/pb.Tasks/CheckPermission",
            request_serializer=app_dot_pb_dot_tasks__pb2.PermissionRequest.SerializeToString,
            response_deserializer=app_dot_pb_dot_tasks__pb2.PermissionResponse.FromString,
        )
        self.GetUserFromToken = channel.unary_unary(
            "/pb.Tasks/GetUserFromToken",
            request_serializer=app_dot_pb_dot_tasks__pb2.GetUserFromTokenRequest.SerializeToString,
            response_deserializer=app_dot_pb_dot_tasks__pb2.GetUserFromTokenResponse.FromString,
        )
        self.GetTokenFromUsername = channel.unary_unary(
            "/pb.Tasks/GetTokenFromUsername",
            request_serializer=app_dot_pb_dot_tasks__pb2.GetTokenFromUsernameRequest.SerializeToString,
            response_deserializer=app_dot_pb_dot_tasks__pb2.GetTokenFromUsernameResponse.FromString,
        )


class TasksServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ConfirmEmail(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CheckPermission(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetUserFromToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetTokenFromUsername(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TasksServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ConfirmEmail": grpc.unary_unary_rpc_method_handler(
            servicer.ConfirmEmail,
            request_deserializer=app_dot_pb_dot_tasks__pb2.ConfirmEmailRequest.FromString,
            response_serializer=app_dot_pb_dot_tasks__pb2.ConfirmEmailResponse.SerializeToString,
        ),
        "CheckPermission": grpc.unary_unary_rpc_method_handler(
            servicer.CheckPermission,
            request_deserializer=app_dot_pb_dot_tasks__pb2.PermissionRequest.FromString,
            response_serializer=app_dot_pb_dot_tasks__pb2.PermissionResponse.SerializeToString,
        ),
        "GetUserFromToken": grpc.unary_unary_rpc_method_handler(
            servicer.GetUserFromToken,
            request_deserializer=app_dot_pb_dot_tasks__pb2.GetUserFromTokenRequest.FromString,
            response_serializer=app_dot_pb_dot_tasks__pb2.GetUserFromTokenResponse.SerializeToString,
        ),
        "GetTokenFromUsername": grpc.unary_unary_rpc_method_handler(
            servicer.GetTokenFromUsername,
            request_deserializer=app_dot_pb_dot_tasks__pb2.GetTokenFromUsernameRequest.FromString,
            response_serializer=app_dot_pb_dot_tasks__pb2.GetTokenFromUsernameResponse.SerializeToString,
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
    def ConfirmEmail(
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
            "/pb.Tasks/ConfirmEmail",
            app_dot_pb_dot_tasks__pb2.ConfirmEmailRequest.SerializeToString,
            app_dot_pb_dot_tasks__pb2.ConfirmEmailResponse.FromString,
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
    def CheckPermission(
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
            "/pb.Tasks/CheckPermission",
            app_dot_pb_dot_tasks__pb2.PermissionRequest.SerializeToString,
            app_dot_pb_dot_tasks__pb2.PermissionResponse.FromString,
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
    def GetUserFromToken(
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
            "/pb.Tasks/GetUserFromToken",
            app_dot_pb_dot_tasks__pb2.GetUserFromTokenRequest.SerializeToString,
            app_dot_pb_dot_tasks__pb2.GetUserFromTokenResponse.FromString,
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
    def GetTokenFromUsername(
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
            "/pb.Tasks/GetTokenFromUsername",
            app_dot_pb_dot_tasks__pb2.GetTokenFromUsernameRequest.SerializeToString,
            app_dot_pb_dot_tasks__pb2.GetTokenFromUsernameResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
