import grpc
from .pb.notifications_pb2_grpc import NotificationsStub
from constants import NOTIFICATIONS_HOST

notifications_channel = grpc.insecure_channel(NOTIFICATIONS_HOST)

notifications_client = NotificationsStub(notifications_channel)
