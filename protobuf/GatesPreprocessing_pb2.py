# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/GatesPreprocessing.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/GatesPreprocessing.proto',
  package='project_inf_mpc',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n!protobuf/GatesPreprocessing.proto\x12\x0fproject_inf_mpc\"Z\n\x04Gate\x12\n\n\x02id\x18\x01 \x02(\x05\x12\n\n\x02M0\x18\x02 \x01(\x0c\x12\n\n\x02M1\x18\x03 \x01(\x0c\x12\n\n\x02G0\x18\x04 \x01(\x0c\x12\n\n\x02G1\x18\x05 \x01(\x0c\x12\n\n\x02G2\x18\x06 \x01(\x0c\x12\n\n\x02G3\x18\x07 \x01(\x0c\":\n\x12GatesPreprocessing\x12$\n\x05gates\x18\x01 \x03(\x0b\x32\x15.project_inf_mpc.Gate')
)




_GATE = _descriptor.Descriptor(
  name='Gate',
  full_name='project_inf_mpc.Gate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='project_inf_mpc.Gate.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='M0', full_name='project_inf_mpc.Gate.M0', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='M1', full_name='project_inf_mpc.Gate.M1', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='G0', full_name='project_inf_mpc.Gate.G0', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='G1', full_name='project_inf_mpc.Gate.G1', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='G2', full_name='project_inf_mpc.Gate.G2', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='G3', full_name='project_inf_mpc.Gate.G3', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=54,
  serialized_end=144,
)


_GATESPREPROCESSING = _descriptor.Descriptor(
  name='GatesPreprocessing',
  full_name='project_inf_mpc.GatesPreprocessing',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gates', full_name='project_inf_mpc.GatesPreprocessing.gates', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=146,
  serialized_end=204,
)

_GATESPREPROCESSING.fields_by_name['gates'].message_type = _GATE
DESCRIPTOR.message_types_by_name['Gate'] = _GATE
DESCRIPTOR.message_types_by_name['GatesPreprocessing'] = _GATESPREPROCESSING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Gate = _reflection.GeneratedProtocolMessageType('Gate', (_message.Message,), dict(
  DESCRIPTOR = _GATE,
  __module__ = 'protobuf.GatesPreprocessing_pb2'
  # @@protoc_insertion_point(class_scope:project_inf_mpc.Gate)
  ))
_sym_db.RegisterMessage(Gate)

GatesPreprocessing = _reflection.GeneratedProtocolMessageType('GatesPreprocessing', (_message.Message,), dict(
  DESCRIPTOR = _GATESPREPROCESSING,
  __module__ = 'protobuf.GatesPreprocessing_pb2'
  # @@protoc_insertion_point(class_scope:project_inf_mpc.GatesPreprocessing)
  ))
_sym_db.RegisterMessage(GatesPreprocessing)


# @@protoc_insertion_point(module_scope)
