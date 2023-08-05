# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CanStackNode.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import Common_pb2 as Common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x43\x61nStackNode.proto\x12\x0c\x43\x61nStackNode\x1a\x0c\x43ommon.proto\"}\n\x12\x63\x61n_channel_config\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x12\x0f\n\x07\x62itrate\x18\x02 \x01(\x05\x12\r\n\x05is_fd\x18\x03 \x01(\x08\x12\x12\n\nfd_bitrate\x18\x04 \x01(\x05\x12\x10\n\x08\x62us_type\x18\x05 \x01(\t\x12\x10\n\x08\x61pp_name\x18\x06 \x01(\t\"H\n\x13\x63\x61n_channel_configs\x12\x31\n\x07\x63onfigs\x18\x01 \x03(\x0b\x32 .CanStackNode.can_channel_config\"-\n\x0esubscribe_info\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x12\n\n\x02id\x18\x02 \x01(\x05\"c\n\x11log_start_request\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tfile_path\x18\x02 \x01(\t\x12\x1b\n\x13max_log_time_minute\x18\x03 \x01(\r\x12\x10\n\x08\x63hannels\x18\x04 \x03(\x05\" \n\x10log_stop_request\x12\x0c\n\x04name\x18\x01 \x01(\t\"z\n\rcrc_rc_config\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x12\x16\n\x0e\x61rbitration_id\x18\x02 \x01(\x05\x12\x16\n\x0e\x63rc_bit_starts\x18\x03 \x03(\x05\x12\x15\n\rrc_bit_starts\x18\x05 \x03(\x05\x12\x11\n\tcrc_table\x18\x07 \x03(\x05\"!\n\x05timer\x12\x18\n\x10timer_cycle_time\x18\x01 \x01(\x04\"\x1a\n\x07\x63hannel\x12\x0f\n\x07\x63hannel\x18\x01 \x01(\x05\x32\xde\x05\n\x0c\x43\x61nStackNode\x12.\n\nGetVersion\x12\r.Common.empty\x1a\x0f.Common.version\"\x00\x12\x41\n\nSetConfigs\x12!.CanStackNode.can_channel_configs\x1a\x0e.Common.result\"\x00\x12\x30\n\rStartCanStack\x12\r.Common.empty\x1a\x0e.Common.result\"\x00\x12/\n\x0cStopCanStack\x12\r.Common.empty\x1a\x0e.Common.result\"\x00\x12,\n\tClearSend\x12\r.Common.empty\x1a\x0e.Common.result\"\x00\x12\x31\n\x0e\x43learSubscribe\x12\r.Common.empty\x1a\x0e.Common.result\"\x00\x12=\n\x08StartLog\x12\x1f.CanStackNode.log_start_request\x1a\x0e.Common.result\"\x00\x12;\n\x07StopLog\x12\x1e.CanStackNode.log_stop_request\x1a\x0e.Common.result\"\x00\x12.\n\x0b\x43learLogger\x12\r.Common.empty\x1a\x0e.Common.result\"\x00\x12?\n\x0eSetCrcRcConfig\x12\x1b.CanStackNode.crc_rc_config\x1a\x0e.Common.result\"\x00\x12\x38\n\x0f\x43reatTimerEvent\x12\x13.CanStackNode.timer\x1a\x0e.Common.result\"\x00\x12\x31\n\x0eGetStackStatus\x12\r.Common.empty\x1a\x0e.Common.result\"\x00\x12=\n\x12StopChannelSendCyc\x12\x15.CanStackNode.channel\x1a\x0e.Common.result\"\x00\x62\x06proto3')



_CAN_CHANNEL_CONFIG = DESCRIPTOR.message_types_by_name['can_channel_config']
_CAN_CHANNEL_CONFIGS = DESCRIPTOR.message_types_by_name['can_channel_configs']
_SUBSCRIBE_INFO = DESCRIPTOR.message_types_by_name['subscribe_info']
_LOG_START_REQUEST = DESCRIPTOR.message_types_by_name['log_start_request']
_LOG_STOP_REQUEST = DESCRIPTOR.message_types_by_name['log_stop_request']
_CRC_RC_CONFIG = DESCRIPTOR.message_types_by_name['crc_rc_config']
_TIMER = DESCRIPTOR.message_types_by_name['timer']
_CHANNEL = DESCRIPTOR.message_types_by_name['channel']
can_channel_config = _reflection.GeneratedProtocolMessageType('can_channel_config', (_message.Message,), {
  'DESCRIPTOR' : _CAN_CHANNEL_CONFIG,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.can_channel_config)
  })
_sym_db.RegisterMessage(can_channel_config)

can_channel_configs = _reflection.GeneratedProtocolMessageType('can_channel_configs', (_message.Message,), {
  'DESCRIPTOR' : _CAN_CHANNEL_CONFIGS,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.can_channel_configs)
  })
_sym_db.RegisterMessage(can_channel_configs)

subscribe_info = _reflection.GeneratedProtocolMessageType('subscribe_info', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBE_INFO,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.subscribe_info)
  })
_sym_db.RegisterMessage(subscribe_info)

log_start_request = _reflection.GeneratedProtocolMessageType('log_start_request', (_message.Message,), {
  'DESCRIPTOR' : _LOG_START_REQUEST,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.log_start_request)
  })
_sym_db.RegisterMessage(log_start_request)

log_stop_request = _reflection.GeneratedProtocolMessageType('log_stop_request', (_message.Message,), {
  'DESCRIPTOR' : _LOG_STOP_REQUEST,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.log_stop_request)
  })
_sym_db.RegisterMessage(log_stop_request)

crc_rc_config = _reflection.GeneratedProtocolMessageType('crc_rc_config', (_message.Message,), {
  'DESCRIPTOR' : _CRC_RC_CONFIG,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.crc_rc_config)
  })
_sym_db.RegisterMessage(crc_rc_config)

timer = _reflection.GeneratedProtocolMessageType('timer', (_message.Message,), {
  'DESCRIPTOR' : _TIMER,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.timer)
  })
_sym_db.RegisterMessage(timer)

channel = _reflection.GeneratedProtocolMessageType('channel', (_message.Message,), {
  'DESCRIPTOR' : _CHANNEL,
  '__module__' : 'CanStackNode_pb2'
  # @@protoc_insertion_point(class_scope:CanStackNode.channel)
  })
_sym_db.RegisterMessage(channel)

_CANSTACKNODE = DESCRIPTOR.services_by_name['CanStackNode']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CAN_CHANNEL_CONFIG._serialized_start=50
  _CAN_CHANNEL_CONFIG._serialized_end=175
  _CAN_CHANNEL_CONFIGS._serialized_start=177
  _CAN_CHANNEL_CONFIGS._serialized_end=249
  _SUBSCRIBE_INFO._serialized_start=251
  _SUBSCRIBE_INFO._serialized_end=296
  _LOG_START_REQUEST._serialized_start=298
  _LOG_START_REQUEST._serialized_end=397
  _LOG_STOP_REQUEST._serialized_start=399
  _LOG_STOP_REQUEST._serialized_end=431
  _CRC_RC_CONFIG._serialized_start=433
  _CRC_RC_CONFIG._serialized_end=555
  _TIMER._serialized_start=557
  _TIMER._serialized_end=590
  _CHANNEL._serialized_start=592
  _CHANNEL._serialized_end=618
  _CANSTACKNODE._serialized_start=621
  _CANSTACKNODE._serialized_end=1355
# @@protoc_insertion_point(module_scope)
