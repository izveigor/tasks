# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: account/pb/users.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder  # type: ignore
from google.protobuf import descriptor as _descriptor  # type: ignore
from google.protobuf import descriptor_pool as _descriptor_pool  # type: ignore
from google.protobuf import symbol_database as _symbol_database  # type: ignore
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x61\x63\x63ount/pb/users.proto\x12\x02pb\"%\n\x14\x41uthorizationRequest\x12\r\n\x05token\x18\x01 \x01(\t\"B\n\x11PermissionRequest\x12\x18\n\x10receiverUsername\x18\x02 \x01(\t\x12\x13\n\x0bsenderToken\x18\x01 \x01(\t\"F\n\x15\x41uthorizationResponse\x12\x1b\n\x13is_permission_exist\x18\x02 \x01(\x08\x12\x10\n\x08username\x18\x01 \x01(\t2\xec\x01\n\x05Users\x12L\n\x15\x41uthorizationLikeUser\x12\x18.pb.AuthorizationRequest\x1a\x19.pb.AuthorizationResponse\x12P\n\x19\x41uthorizationLikeTeammate\x12\x18.pb.AuthorizationRequest\x1a\x19.pb.AuthorizationResponse\x12\x43\n\x0f\x43heckPermission\x12\x15.pb.PermissionRequest\x1a\x19.pb.AuthorizationResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'account.pb.users_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AUTHORIZATIONREQUEST._serialized_start=30  # type: ignore
  _AUTHORIZATIONREQUEST._serialized_end=67  # type: ignore
  _PERMISSIONREQUEST._serialized_start=69  # type: ignore
  _PERMISSIONREQUEST._serialized_end=135  # type: ignore
  _AUTHORIZATIONRESPONSE._serialized_start=137  # type: ignore
  _AUTHORIZATIONRESPONSE._serialized_end=207  # type: ignore
  _USERS._serialized_start=210  # type: ignore
  _USERS._serialized_end=446  # type: ignore
# @@protoc_insertion_point(module_scope)
