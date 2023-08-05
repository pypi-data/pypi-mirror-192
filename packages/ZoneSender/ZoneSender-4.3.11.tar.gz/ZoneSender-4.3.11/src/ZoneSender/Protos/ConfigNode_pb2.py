# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ConfigNode.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import Common_pb2 as Common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x43onfigNode.proto\x12\nConfigNode\x1a\x0c\x43ommon.proto\"\x1d\n\rhardware_type\x12\x0c\n\x04type\x18\x01 \x03(\r\"*\n\x0c\x63hannel_info\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x03(\t\"Q\n\rhardware_info\x12\x15\n\rhardware_type\x18\x01 \x01(\t\x12)\n\x07\x63hannel\x18\x02 \x03(\x0b\x32\x18.ConfigNode.channel_info\"=\n\x0ehardware_infos\x12+\n\x08hardware\x18\x01 \x03(\x0b\x32\x19.ConfigNode.hardware_info\"\x1a\n\x07\x64\x62_path\x12\x0f\n\x07\x64\x62_path\x18\x01 \x01(\t\"\x1e\n\x0b\x63\x61n_cluster\x12\x0f\n\x07\x63luster\x18\x01 \x03(\t\"\x9d\x01\n\x10\x63\x61n_channel_info\x12\x18\n\x10software_channel\x18\x01 \x01(\t\x12\x18\n\x10hardware_channel\x18\x02 \x01(\t\x12\x18\n\x10\x64\x61tabase_channel\x18\x03 \x01(\t\x12\x10\n\x08\x63\x61n_type\x18\x04 \x01(\r\x12\x13\n\x0b\x61rb_bitrate\x18\x05 \x01(\r\x12\x14\n\x0c\x64\x61ta_bitrate\x18\x06 \x01(\r\"P\n\x0f\x63\x61n_config_info\x12=\n\x17\x63\x61n_config_channel_info\x18\x01 \x03(\x0b\x32\x1c.ConfigNode.can_channel_info\"\x84\x01\n\x10lin_channel_info\x12\x18\n\x10software_channel\x18\x01 \x01(\t\x12\x18\n\x10hardware_channel\x18\x02 \x01(\t\x12\x18\n\x10\x64\x61tabase_channel\x18\x03 \x01(\t\x12\x11\n\tis_master\x18\x04 \x01(\r\x12\x0f\n\x07\x62itrate\x18\x05 \x01(\r\"P\n\x0flin_config_info\x12=\n\x17lin_config_channel_info\x18\x01 \x03(\x0b\x32\x1c.ConfigNode.lin_channel_info\"=\n\x0f\x65th_config_info\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x64\x61tabase\x18\x03 \x03(\t2\xd8\x02\n\nConfigNode\x12J\n\x0fgetHardwareInfo\x12\x19.ConfigNode.hardware_type\x1a\x1a.ConfigNode.hardware_infos\"\x00\x12>\n\x0csendCanArxml\x12\x13.ConfigNode.db_path\x1a\x17.ConfigNode.can_cluster\"\x00\x12>\n\rsendCanConfig\x12\x1b.ConfigNode.can_config_info\x1a\x0e.Common.result\"\x00\x12>\n\rsendLinConfig\x12\x1b.ConfigNode.lin_config_info\x1a\x0e.Common.result\"\x00\x12>\n\rsendEthConfig\x12\x1b.ConfigNode.eth_config_info\x1a\x0e.Common.result\"\x00\x62\x06proto3')



_HARDWARE_TYPE = DESCRIPTOR.message_types_by_name['hardware_type']
_CHANNEL_INFO = DESCRIPTOR.message_types_by_name['channel_info']
_HARDWARE_INFO = DESCRIPTOR.message_types_by_name['hardware_info']
_HARDWARE_INFOS = DESCRIPTOR.message_types_by_name['hardware_infos']
_DB_PATH = DESCRIPTOR.message_types_by_name['db_path']
_CAN_CLUSTER = DESCRIPTOR.message_types_by_name['can_cluster']
_CAN_CHANNEL_INFO = DESCRIPTOR.message_types_by_name['can_channel_info']
_CAN_CONFIG_INFO = DESCRIPTOR.message_types_by_name['can_config_info']
_LIN_CHANNEL_INFO = DESCRIPTOR.message_types_by_name['lin_channel_info']
_LIN_CONFIG_INFO = DESCRIPTOR.message_types_by_name['lin_config_info']
_ETH_CONFIG_INFO = DESCRIPTOR.message_types_by_name['eth_config_info']
hardware_type = _reflection.GeneratedProtocolMessageType('hardware_type', (_message.Message,), {
  'DESCRIPTOR' : _HARDWARE_TYPE,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.hardware_type)
  })
_sym_db.RegisterMessage(hardware_type)

channel_info = _reflection.GeneratedProtocolMessageType('channel_info', (_message.Message,), {
  'DESCRIPTOR' : _CHANNEL_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.channel_info)
  })
_sym_db.RegisterMessage(channel_info)

hardware_info = _reflection.GeneratedProtocolMessageType('hardware_info', (_message.Message,), {
  'DESCRIPTOR' : _HARDWARE_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.hardware_info)
  })
_sym_db.RegisterMessage(hardware_info)

hardware_infos = _reflection.GeneratedProtocolMessageType('hardware_infos', (_message.Message,), {
  'DESCRIPTOR' : _HARDWARE_INFOS,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.hardware_infos)
  })
_sym_db.RegisterMessage(hardware_infos)

db_path = _reflection.GeneratedProtocolMessageType('db_path', (_message.Message,), {
  'DESCRIPTOR' : _DB_PATH,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.db_path)
  })
_sym_db.RegisterMessage(db_path)

can_cluster = _reflection.GeneratedProtocolMessageType('can_cluster', (_message.Message,), {
  'DESCRIPTOR' : _CAN_CLUSTER,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.can_cluster)
  })
_sym_db.RegisterMessage(can_cluster)

can_channel_info = _reflection.GeneratedProtocolMessageType('can_channel_info', (_message.Message,), {
  'DESCRIPTOR' : _CAN_CHANNEL_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.can_channel_info)
  })
_sym_db.RegisterMessage(can_channel_info)

can_config_info = _reflection.GeneratedProtocolMessageType('can_config_info', (_message.Message,), {
  'DESCRIPTOR' : _CAN_CONFIG_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.can_config_info)
  })
_sym_db.RegisterMessage(can_config_info)

lin_channel_info = _reflection.GeneratedProtocolMessageType('lin_channel_info', (_message.Message,), {
  'DESCRIPTOR' : _LIN_CHANNEL_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.lin_channel_info)
  })
_sym_db.RegisterMessage(lin_channel_info)

lin_config_info = _reflection.GeneratedProtocolMessageType('lin_config_info', (_message.Message,), {
  'DESCRIPTOR' : _LIN_CONFIG_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.lin_config_info)
  })
_sym_db.RegisterMessage(lin_config_info)

eth_config_info = _reflection.GeneratedProtocolMessageType('eth_config_info', (_message.Message,), {
  'DESCRIPTOR' : _ETH_CONFIG_INFO,
  '__module__' : 'ConfigNode_pb2'
  # @@protoc_insertion_point(class_scope:ConfigNode.eth_config_info)
  })
_sym_db.RegisterMessage(eth_config_info)

_CONFIGNODE = DESCRIPTOR.services_by_name['ConfigNode']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _HARDWARE_TYPE._serialized_start=46
  _HARDWARE_TYPE._serialized_end=75
  _CHANNEL_INFO._serialized_start=77
  _CHANNEL_INFO._serialized_end=119
  _HARDWARE_INFO._serialized_start=121
  _HARDWARE_INFO._serialized_end=202
  _HARDWARE_INFOS._serialized_start=204
  _HARDWARE_INFOS._serialized_end=265
  _DB_PATH._serialized_start=267
  _DB_PATH._serialized_end=293
  _CAN_CLUSTER._serialized_start=295
  _CAN_CLUSTER._serialized_end=325
  _CAN_CHANNEL_INFO._serialized_start=328
  _CAN_CHANNEL_INFO._serialized_end=485
  _CAN_CONFIG_INFO._serialized_start=487
  _CAN_CONFIG_INFO._serialized_end=567
  _LIN_CHANNEL_INFO._serialized_start=570
  _LIN_CHANNEL_INFO._serialized_end=702
  _LIN_CONFIG_INFO._serialized_start=704
  _LIN_CONFIG_INFO._serialized_end=784
  _ETH_CONFIG_INFO._serialized_start=786
  _ETH_CONFIG_INFO._serialized_end=847
  _CONFIGNODE._serialized_start=850
  _CONFIGNODE._serialized_end=1194
# @@protoc_insertion_point(module_scope)
