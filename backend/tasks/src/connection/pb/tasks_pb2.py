# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connection/pb/tasks.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor  # type: ignore
from google.protobuf import descriptor_pool as _descriptor_pool  # type: ignore
from google.protobuf import symbol_database as _symbol_database  # type: ignore
from google.protobuf.internal import builder as _builder  # type: ignore

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x19\x63onnection/pb/tasks.proto\x12\x02pb":\n\x0bUserRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05image\x18\x03 \x01(\t"\x0e\n\x0cUserResponse"\x17\n\tIDRequest\x12\n\n\x02id\x18\x01 \x01(\t2\x95\x01\n\x05Tasks\x12,\n\x07\x41\x64\x64User\x12\x0f.pb.UserRequest\x1a\x10.pb.UserResponse\x12/\n\nChangeUser\x12\x0f.pb.UserRequest\x1a\x10.pb.UserResponse\x12-\n\nDeleteUser\x12\r.pb.IDRequest\x1a\x10.pb.UserResponseb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "connection.pb.tasks_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _USERREQUEST._serialized_start = 33  # type: ignore
    _USERREQUEST._serialized_end = 91  # type: ignore
    _USERRESPONSE._serialized_start = 93  # type: ignore
    _USERRESPONSE._serialized_end = 107  # type: ignore
    _IDREQUEST._serialized_start = 109  # type: ignore
    _IDREQUEST._serialized_end = 132  # type: ignore
    _TASKS._serialized_start = 135  # type: ignore
    _TASKS._serialized_end = 284  # type: ignore
# @@protoc_insertion_point(module_scope)
