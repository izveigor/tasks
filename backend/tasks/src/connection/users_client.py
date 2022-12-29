import grpc

from constants import USERS_HOST

from .pb.users_pb2_grpc import UsersStub

users_channel = grpc.insecure_channel(USERS_HOST)

users_client = UsersStub(users_channel)
