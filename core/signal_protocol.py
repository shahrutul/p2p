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
query(query_data, IP, port, ttl, hops)
# args: object, string, number, number, number
# returns: query hit

# pong: reply to ping with contact data
pong(IP, port)
# args: string, number
# Pongs are only sent in response to an incoming ping

# youare: a reply to 'whoami'
youare(IP, port)
# args: string, number

# query hit: reply to a query
query_hit(reply_query_data)
# args: string, number, object
# returns: nothing

Data structs:
query_data: JSON object
  id = string
  title = string
  place = string
  description = string
  query_time = query_time_obj

query_time_obj <=> JSON object:
  from_hour: number in 0..23
  from_minute: number in 0..59
  until_hour: number in 0..23
  until_minute: number in 0..59
  weekdays: list with one or more weekday entries
            'mo', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'


"""
import json
from config import logs  # pylint: disable=E0611
from gui_interface import Query, QueryTime


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

class QueryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Query):
            return {'title': obj.title,
                    'place': obj.place,
                    'query_time': obj.query_time,
                    'description': obj.description,
                    'id': obj.id}
        elif isinstance(obj, QueryTime):
            return { 'from_hour': obj.from_hour,
                     'from_minute': obj.from_minute,
                     'until_hour': obj.until_hour,
                     'until_minute': obj.until_minute,
                     'weekdays': obj.weekdays}
        return json.JSONEncoder.default(self, obj)
    
def decode_query(dict_):
    if 'query_time' in dict_:
        vals = dict_['query_time']
        q_time = QueryTime(vals['from_hour'],
                           vals['from_minute'],
                           vals['until_hour'],
                           vals['until_minute'],
                           vals['weekdays'])
        return Query(dict_['title'],
                     dict_['place'],
                     q_time,
                     dict_['description'],
                     dict_['id'])
    
    else:
        return dict_
    
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
              'pong': (basestring, int),
              'query': (Query, int, int)
             }

    def __init__(self, type_, content=()):
        try:
            arg_types = Signal._types[type_]
            if not hasattr(content, '__iter__'):
                content = (content,)
            if not arg_type_check(arg_types, *content):
                raise ProtocolError("Expected: %s(%s), not %s(%s)" %
                      (type_, map(lambda obj:
                                  getattr(obj,"__name__"),
                                  arg_types),
                              type_, content))
        except (ValueError, TypeError, KeyError), reason:
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
            json_obj = json.loads(data, object_hook = decode_query)
            return Signal(json_obj['type'], json_obj['content'])
        except (TypeError, ValueError), reason:
            raise ProtocolError(data, reason)
        except KeyError, reason:
            err = """Expected: '{"%s":"x", "%s":["y","z"]}', not %s""" % \
                  ('type', 'content', data)
            raise ProtocolError(err)

    def serialize(self):
        """ Converts input to JSON objects
        Returns: JSON representation, e.g """
        logs.logger.debug("serialize: %s", self)
        try:
            return json.dumps({'type': self.type,
                               'content': self.content},
                              cls = QueryEncoder) + Signal.TERMINATOR
        except (TypeError), reason:
            logs.logger.critical("serializer exception, reason %s" % reason)
            raise ProtocolError(reason)
