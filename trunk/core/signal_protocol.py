#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Network protocol module. Converts python messages from/to JSON objects.
Format: an JSON object with type and content attributes:

JSON.type = message type/name
JSON.content = list with arguments/data

Message terminator is '\x00'
e.g
error("ProtocolError", "x")
<=>
'{"type": "error", "content": ["ProtocolError", "x"]}\x00'

Messages:
# error: response for invalid requests
error(spec, reason)
# args: string, string
# returns: nothing

# ping: discover hosts on network
ping(ping_id, ttl, hops)
# args: string, number, number
# returns: at least one pong


# whoami: discover own IP address and invite for neighbourship
whoami(port)
# args: number
# returns: youare

# query: search for data
query(mydata, ttl, hops)
# args: object, number, number
# returns: query hit

# pong: reply to ping with contact data
pong(IP, port)
# args: string, number
# Pongs are only sent in response to an incoming ping

# youare: a reply to 'whoami'
youare(IP, port)
# args: string, number

# query hit: reply to a query
query_hit(IP, port, data)
# args: string, number, object
# returns: nothing
"""
import json
from config import logs  # pylint: disable=E0611


class ProtocolError(Exception):  # pylint: disable=C0111
    pass


def arg_type_check(types, *args):
    """ Provides argument type checking.
    Expects: typelist, arguments to check.
    e.g: [str, str], 'hello','world'
    """
    if len(types) != len(args):
        return False
    for arg, type_ in zip(args, types):
        if not isinstance(arg, type_):
            return False

    return True


class Signal(object):
    """ Provides common signals for communication and
    a message to/from JSON converter. Accepts 'registered'
    signals only. """
    __slots__ = ("type", "content")
    TERMINATOR = '\0'
    # errors:
    ProtocolError = "ProtocolError"
    # implemented signals with name and argument types
    _types = {'error': (basestring, basestring),
              'whoami': (int,),
              'youare': (basestring, int),
              'ping': (basestring, int, int),
              'pong': (basestring, int)
             }

    def __init__(self, type_, content=()):
        try:
            arg_types = Signal._types[type_]
            if not hasattr(content, '__iter__'):
                content = (content,)
            if not arg_type_check(arg_types, *content):
                raise ProtocolError("Expected: %s(%s), not %s(%s)" %
                                    (type_, arg_types, type_, content))
        except (ValueError, TypeError, KeyError), reason:
            print reason
            raise ProtocolError("type = %s, content = %s" % (type_, content))

        self.type = type_
        self.content = content

    def __str__(self):
        return "Signal(%s,%s)" % (self.type, self.content)

    @staticmethod
    def deserialize(data):
        """ Deserializes JSON objects to Signals """
        logs.logger.debug("convert: %s" % data)
        try:
            json_obj = json.loads(data)
            return Signal(json_obj['type'], json_obj['content'])
        except (TypeError, ValueError), reason:
            raise ProtocolError(data, reason)
        except KeyError:
            err = """Expected: '{"%s":"x", "%s":["y","z"]}', not %s""" % \
                  ('type', 'content', data)
            raise ProtocolError(err)

    def serialize(self):
        """ Converts input to JSON objects
        Returns: JSON representation, e.g """
        logs.logger.debug("serialize: %s", self)
        try:
            return json.dumps({'type': self.type,
                               'content': self.content}) + Signal.TERMINATOR
        except (TypeError), reason:
            logs.logger.critical("serializer exception, reason %s" % reason)
            raise ProtocolError(reason)
