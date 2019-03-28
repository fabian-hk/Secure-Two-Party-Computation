# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/Output.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/Output.proto',
  package='project_inf_mpc.output',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x15protobuf/Output.proto\x12\x16project_inf_mpc.output\"$\n\x06Output\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x0e\n\x06output\x18\x02 \x01(\x0c\":\n\x07Outputs\x12/\n\x07outputs\x18\x01 \x03(\x0b\x32\x1e.project_inf_mpc.output.Output')
)




_OUTPUT = _descriptor.Descriptor(
  name='Output',
  full_name='project_inf_mpc.output.Output',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='project_inf_mpc.output.Output.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output', full_name='project_inf_mpc.output.Output.output', index=1,
      number=2, type=12, cpp_type=9, label=1,
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
  serialized_start=49,
  serialized_end=85,
)


_OUTPUTS = _descriptor.Descriptor(
  name='Outputs',
  full_name='project_inf_mpc.output.Outputs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='outputs', full_name='project_inf_mpc.output.Outputs.outputs', index=0,
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
  serialized_start=87,
  serialized_end=145,
)

_OUTPUTS.fields_by_name['outputs'].message_type = _OUTPUT
DESCRIPTOR.message_types_by_name['Output'] = _OUTPUT
DESCRIPTOR.message_types_by_name['Outputs'] = _OUTPUTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Output = _reflection.GeneratedProtocolMessageType('Output', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUT,
  __module__ = 'protobuf.Output_pb2'
  # @@protoc_insertion_point(class_scope:project_inf_mpc.output.Output)
  ))
_sym_db.RegisterMessage(Output)

Outputs = _reflection.GeneratedProtocolMessageType('Outputs', (_message.Message,), dict(
  DESCRIPTOR = _OUTPUTS,
  __module__ = 'protobuf.Output_pb2'
  # @@protoc_insertion_point(class_scope:project_inf_mpc.output.Outputs)
  ))
_sym_db.RegisterMessage(Outputs)


# @@protoc_insertion_point(module_scope)