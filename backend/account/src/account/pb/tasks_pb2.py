# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: account/pb/tasks.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x61\x63\x63ount/pb/tasks.proto\x12\x02pb\":\n\x0bUserRequest\x12\n\n\x02id\x18\x03 \x01(\x03\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05image\x18\x01 \x01(\t\"\x0e\n\x0cUserResponse\"\x17\n\tIDRequest\x12\n\n\x02id\x18\x01 \x01(\x03\x32\x95\x01\n\x05Users\x12,\n\x07\x41\x64\x64User\x12\x0f.pb.UserRequest\x1a\x10.pb.UserResponse\x12/\n\nChangeUser\x12\x0f.pb.UserRequest\x1a\x10.pb.UserResponse\x12-\n\nDeleteUser\x12\r.pb.IDRequest\x1a\x10.pb.UserResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'account.pb.tasks_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERREQUEST._serialized_start=30
  _USERREQUEST._serialized_end=88
  _USERRESPONSE._serialized_start=90
  _USERRESPONSE._serialized_end=104
  _IDREQUEST._serialized_start=106
  _IDREQUEST._serialized_end=129
  _USERS._serialized_start=132
  _USERS._serialized_end=281
# @@protoc_insertion_point(module_scope)
