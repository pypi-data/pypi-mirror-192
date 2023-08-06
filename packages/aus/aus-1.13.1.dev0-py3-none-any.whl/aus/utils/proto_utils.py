"""Utilities for proto related manipulations."""
from typing import TypeVar
from google.protobuf import any_pb2
from google.protobuf import message
from google.protobuf import descriptor_pool
from google.protobuf import message_factory

# Type for a subclass of message.Message which will be used as a return type.
ProtoMessage = TypeVar('ProtoMessage', bound=message.Message)


def _create_proto_instance_from_name(
        message_name: str, pool: descriptor_pool.DescriptorPool) -> ProtoMessage:
    """Creates a protobuf message instance from a given message name."""
    message_descriptor = pool.FindMessageTypeByName(message_name)
    factory = message_factory.MessageFactory(pool)
    message_type = factory.GetPrototype(message_descriptor)
    return message_type()


from typing import Any, Dict, Iterator, TypeVar, Optional


def unpack_proto_any(any_proto: any_pb2.Any) -> ProtoMessage:
    """Unpacks a google.protobuf.Any message into its concrete type."""
    pool = descriptor_pool.Default()
    message_name = any_proto.type_url.split('/')[-1]
    proto_instance = _create_proto_instance_from_name(message_name, pool)
    any_proto.Unpack(proto_instance)
    return proto_instance
