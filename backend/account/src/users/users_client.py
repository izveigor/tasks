import grpc
from account.pb.users_pb2_grpc import UsersStub
from account.constants import USERS_HOST

users_channel = grpc.insecure_channel(USERS_HOST)

users_client = UsersStub(users_channel)
