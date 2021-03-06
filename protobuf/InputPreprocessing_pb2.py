# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/InputPreprocessing.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/InputPreprocessing.proto',
  package='project_inf_mpc.input_preprocessing',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n!protobuf/InputPreprocessing.proto\x12#project_inf_mpc.input_preprocessing\"8\n\x05Input\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x14\n\x0cmasked_input\x18\x02 \x01(\x0c\x12\r\n\x05label\x18\x03 \x01(\x0c\"D\n\x06Inputs\x12:\n\x06inputs\x18\x01 \x03(\x0b\x32*.project_inf_mpc.input_preprocessing.Input')
)




_INPUT = _descriptor.Descriptor(
  name='Input',
  full_name='project_inf_mpc.input_preprocessing.Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='project_inf_mpc.input_preprocessing.Input.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='masked_input', full_name='project_inf_mpc.input_preprocessing.Input.masked_input', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='project_inf_mpc.input_preprocessing.Input.label', index=2,
      number=3, type=12, cpp_type=9, label=1,
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
  serialized_start=74,
  serialized_end=130,
)


_INPUTS = _descriptor.Descriptor(
  name='Inputs',
  full_name='project_inf_mpc.input_preprocessing.Inputs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='inputs', full_name='project_inf_mpc.input_preprocessing.Inputs.inputs', index=0,
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
  serialized_start=132,
  serialized_end=200,
)

_INPUTS.fields_by_name['inputs'].message_type = _INPUT
DESCRIPTOR.message_types_by_name['Input'] = _INPUT
DESCRIPTOR.message_types_by_name['Inputs'] = _INPUTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), dict(
  DESCRIPTOR = _INPUT,
  __module__ = 'protobuf.InputPreprocessing_pb2'
  # @@protoc_insertion_point(class_scope:project_inf_mpc.input_preprocessing.Input)
  ))
_sym_db.RegisterMessage(Input)

Inputs = _reflection.GeneratedProtocolMessageType('Inputs', (_message.Message,), dict(
  DESCRIPTOR = _INPUTS,
  __module__ = 'protobuf.InputPreprocessing_pb2'
  # @@protoc_insertion_point(class_scope:project_inf_mpc.input_preprocessing.Inputs)
  ))
_sym_db.RegisterMessage(Inputs)


# @@protoc_insertion_point(module_scope)
