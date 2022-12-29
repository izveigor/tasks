import grpc

from account.constants import NOTIFICATIONS_HOST
from account.pb.notifications_pb2_grpc import NotificationsStub

notifications_channel = grpc.insecure_channel(NOTIFICATIONS_HOST)

notifications_client = NotificationsStub(notifications_channel)
