#! /Usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for XML-RPC based network communication """

import xmlrpclib
import threading
import SocketServer

from SimpleXMLRPCServer import SimpleXMLRPCServer, \
     SimpleXMLRPCRequestHandler as RequestHandler, SimpleXMLRPCDispatcher

from config import settings  # pylint: disable=E0611


class _NonBlockingRPC(SocketServer.ThreadingMixIn,  # pylint: disable=R0904
             SimpleXMLRPCServer):
    """ Non-blocking receiver for incoming messages """

class _ExtendedRequestHandler(RequestHandler):
    """ Subclassed RequestHandler to obtain clients IP) """
    def __init__(self, request, client_address, server):
        self.client_address = client_address[0]
        RequestHandler.__init__(self, request, client_address, server)

    def _dispatch(self, method, params):
        """ Overrides dispatch to pass obtained client informations """
        func = World().funcs.get(method)
        if func is not None:
            return func(*params, client_address = self.client_address)
        else:
            raise Exception('method "%s" is not supported' % method)


def singleton(cls):
    """ A simple singleton pattern decorator """
    instances = {}

    def getinstance():
        """ Creates a single object and use instances dict as cache """
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class World(object):
    """ Class for communication with the rest of the world """
        
    def __init__(self, port=settings.network.server_port):
        """ Creates an RPC Server, accepts a single method or a list """
        
        self.funcs = {}
        self._rpc_server = _NonBlockingRPC(
            ('', port), requestHandler=_ExtendedRequestHandler)

        thread = threading.Thread(target=self._rpc_server.serve_forever)
        thread.setDaemon(True)
        thread.start()

    def register_method(self, method, name=None):        
        if name is None:
            name = method.__name__
        # TODO: put some thread-safety in here
        self.funcs[name] = method


