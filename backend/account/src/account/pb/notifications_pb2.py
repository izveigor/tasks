# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: account/pb/notifications.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor  # type: ignore
from google.protobuf import descriptor_pool as _descriptor_pool  # type: ignore
from google.protobuf import symbol_database as _symbol_database  # type: ignore
from google.protobuf.internal import builder as _builder  # type: ignore

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1e\x61\x63\x63ount/pb/notifications.proto\x12\x02pb\x1a\x1fgoogle/protobuf/timestamp.proto"l\n\x13NotificationRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\r\n\x05image\x18\x03 \x01(\t\x12(\n\x04time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06tokens\x18\x02 \x03(\t"\x16\n\x14NotificationResponse2L\n\rNotifications\x12;\n\x06Notify\x12\x17.pb.NotificationRequest\x1a\x18.pb.NotificationResponseb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "account.pb.notifications_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _NOTIFICATIONREQUEST._serialized_start = 71  # type: ignore
    _NOTIFICATIONREQUEST._serialized_end = 179  # type: ignore
    _NOTIFICATIONRESPONSE._serialized_start = 181  # type: ignore
    _NOTIFICATIONRESPONSE._serialized_end = 203  # type: ignore
    _NOTIFICATIONS._serialized_start = 205  # type: ignore
    _NOTIFICATIONS._serialized_end = 281  # type: ignore
# @@protoc_insertion_point(module_scope)
