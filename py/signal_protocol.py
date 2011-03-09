""" Network protocol module. Converts python messages from/to JSON objects"""
import json
from collections import namedtuple
from config import logs  # pylint: disable=E0611


class ProtocolError(Exception):  # pylint: disable=C0111
    pass


class Messages(object):
    """ Provides common messages for communication and
    a message to/from JSON converter."""
    TERMINATOR = '\0'
    errors = [ProtocolError.__name__]
    messages = ['chat', 'error']

    Message = namedtuple('Message', 'name args')

    @staticmethod
    def chat(message):
        """ converts chat message to an JSON object.
        JSON.name = "chat"
        json.args = message """
        return Messages.serialize("chat", message)
    

    @staticmethod
    def error(spec, reason=None):
        """ converts an error to an JSON object
        JSON.name = "error"
        JSON.args = "spec, reason(s)" list
        """
        logs.logger.debug("Message error: %s, reason: %s" % (spec, reason))
        try:
            if spec.__name__ in Messages.errors:
                return Messages.serialize("error", spec.__name__, reason)
            else:
                raise ProtocolError(spec)
        except AttributeError, error:
            logs.logger.critical(
                "Messages.error exception, reason: %s" % error)
            raise ProtocolError(error)

    @staticmethod
    def serialize(name, *args):
        """ converts input to JSON objects:
        JSON.name = name
        JSON.args = args
        """
        logs.logger.debug("serialize: %s, %s, %s", name, args)
        try:
            return json.dumps({'name': name, 'args': args})
        except (ValueError, TypeError), reason:
            logs.logger.critical("serializer exception, reason %s" % reason)
            raise ProtocolError(name)

    @staticmethod
    def deserialize(data):
        """ converts from JSON objects to python dictionary """
        logs.logger.debug("deserialize: %s" % data)
        try:
            result = json.loads(data)
            if result['name'] in Messages.messages:
                return Messages.Message(result['name'], result['args'])
            else:
                raise ProtocolError(result['name'])
        except (ValueError, TypeError, KeyError):
            raise ProtocolError(data)
