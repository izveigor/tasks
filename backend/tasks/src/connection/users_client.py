import grpc
from .pb.users_pb2_grpc import UsersStub
from constants import USERS_HOST

users_channel = grpc.insecure_channel(USERS_HOST)

users_client = UsersStub(users_channel)
