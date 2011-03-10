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
# returns: pong

# whoami: discover own IP address
whoami()
# returns: addr

# query: search for data
query(mydata, ttl, hops)
# args: object, number, number
# returns: query hit

Datastructs:
# pong: reply to ping with contact data
pong(addr)

# addr: IP address
addr(IP, port)
# args: string, number

# query hit: reply to a query
query_hit(addr, data)
# args: addr, object
# returns: nothing
"""
import json
from collections import namedtuple
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

class Signal():
    """ Provides common signals for communication and
    a message to/from JSON converter. Accepts 'registered'
    signals only. """
    __slots__ = ("type", "content")
    TERMINATOR = '\0'
    # errors:
    ProtocolError = "ProtocolError"
    # implemented signals with name and argument types
    _types = {'error' : (basestring, basestring),
              'whoami' :(),
              'addr': (basestring, int)
             }
    
    def __init__(self, type_, content = ()):        
        try:
            arg_types = Signal._types[type_]
            if not arg_type_check(arg_types, *content):
                raise ProtocolError("Expected: %s(%s), not %s(%s)" %
                                    (type_, arg_types, type_, content))
        except (ValueError, TypeError, KeyError):
            raise ProtocolError(type_)
        
        self.type = type_
        self.content = content

    def __str__(self):
        return "Signal(%s,%s)" %(self.type, self.content)

    @staticmethod
    def deserialize(data):
        """ Deserializes JSON objects to Signals """
        logs.logger.debug("convert: %s" % data)
        try:
            return Signal(*json.loads(data))
        except (TypeError, ValueError), reason:
            raise ProtocolError(data, reason)

    def serialize(self):
        """ Converts input to JSON objects
        Returns: JSON representation, e.g 
        """
        logs.logger.debug("serialize: %s", self)
        try:
            return json.dumps({'type' :self.type,
                               'content':self.content}) + Signal.TERMINATOR
        except (TypeError), reason:
            logs.logger.critical("serializer exception, reason %s" % reason)
            raise ProtocolError(reason)
        
    
        
class Signal2(object):

    TERMINATOR = '\0'
    msg = namedtuple('msg', 'name args')
    # Errors:
    ProtocolError = "ProtocolError"
    # Message names and argument types:
    _error = msg('error', (basestring, basestring))
    _ping = msg('ping',(basestring, basestring, basestring))
    _whoami = msg('whoami',())
    _addr = msg('addr', (basestring, int))
    msg_pool = {'error' : _error,
                'whoami' : _whoami}
    
    @staticmethod
    def serialize(arg_msg):
        """ Converts input to JSON objects, checks args types.
        Accepts: Message.msg objects
        Returns: JSON representation, e.g 
        """
        logs.logger.debug("serialize: msg(%s)", arg_msg)
        try:
            types = Signal.msg_pool[arg_msg.name].args
            if arg_type_check(types, *arg_msg.args):
                return json.dumps(arg_msg) + Signal.TERMINATOR
            else:
                raise ProtocolError("Expected: %s(%s), not %s(%s)" %
                                    (arg_msg.name, types,
                                     arg_msg.name, arg_msg.args))
        except (KeyError, ValueError, TypeError), reason:
            logs.logger.critical("serializer exception, reason %s" % reason)
            raise ProtocolError(reason)
        
    @staticmethod
    def deserialize(data):
        """ Converts from JSON objects to message object, provides some
        type checking."""
        logs.logger.debug("deserialize: %s" % data)
        try:
            data_msg = Signal.msg(*json.loads(data))
            types = Signal.msg_pool[data_msg.name].args
            if not arg_type_check(types, *data_msg.args):
                raise ProtocolError("Expected: %s(%s), not %s(%s)" %
                                    (data_msg.name, types, data_msg.name,
                                     tuple(map(type, data_msg.args))))
            else:
                return data_msg
        except (ValueError, TypeError, KeyError), reason:
            raise ProtocolError(data)
