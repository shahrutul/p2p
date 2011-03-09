#! /Usr/bin/env python
# -*- coding: utf-8 -*-

""" Asyncore/asychat "mutated" to a network-nerve.
The central idea: represent the network as an 'organ' pool.
Organs may send/receive signals.
Simply connect the nervous system to this pool and communicate.

How it works:
1.wraps asyncore Server/Channels to coroutines (neuron, synapses) 
2.creates one filter-neuron-coroutine for simple signal filtering
3.transmits distinct signals over distinct synapses to a filter neuron.
Filters singals and transmist them to the output.
Provides some organ_id/synapse_id for further communication.
                  +-------+
          ------->|synapse|-------
         /        +-------+       \
+----- +/         +-------+        \  +------+      +------+
|neuron|--------->|synapse|---------->|filter|----->|output|
+----- +\         +-------+        /  +------+      +------+
         \        +-------+       /
          ------->|synapse|-------
                  +-------+
                  
Creating: NetworkNeuron(output_synapse)
The output_synapse is a coroutine or an object implementing 'send' method
and consumes incoming signals.

Output format: (organ_id/synapse, python object)

Attention:
Neurons need energy to transport their neurotransmitters!
Provide some energy(=time) or the neuron will not work correctly!

NetworkNeuron.feed(amount=(0,R+])
or
NetworkNeuron.feed()
"""

import asynchat
import asyncore
import socket

from decorators import coroutine
from config import network, logs
from signal_protocol import Messages, ProtocolError

class NeuronError(Exception):
    """ Serious/fatal error while creating a neuronal connection """
    pass

@coroutine
def error_transmitter():
    try:
        while True:
            synapse, error, reason = (yield)
            if synapse.is_active():
                synapse.err_response(Messages.error(error, reason))
                logs.logger.debug("error_transmitter: %s, %s, %s" %
                                  (synapse, error.__name__, reason))
    finally:
        logs.logger.debug("error_transmitter closed")
        
@coroutine
def signal_filter(processor, err_sender):
    """ Collects and validates input messages from synapses """
    try:
        while True:       
            synapse, data = (yield)
            try:
                logs.logger.debug("filters data from %s" % synapse)
                msg = Messages.deserialize(data)                
            except ProtocolError, reason:
                # low-level protocol error (e.g transmission of '[1,2' )
                logs.logger.debug("filter error: %s,%s" % (synapse, reason))
                err_sender.send((synapse, ProtocolError, str(reason)))
            else:                
                processor.send((synapse, msg))
    finally:
        logs.logger.debug("data filter closed")
            

class _Synapse(asynchat.async_chat):
    """ Asynchronous network channel mutated to a synapse."""

    def __init__(self, sock, addr, target):
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator(Messages.TERMINATOR)
        self.buffer = []
        self.target = target
        self.collect_incoming_data = self.buffer.append
        self.host_addr = addr[0]

    def found_terminator(self):
        """ Sends received message to target """
        logs.logger.debug("%s sends data to %s" % (self, self.target.__name__))
        self.target.send((self, "".join(self.buffer)))
        del(self.buffer[:])        
        
    def is_active(self):
        """ provides information about synapse activity """
        return (self.accepting  == True) or (self.connected == True)

    def err_response(self, data):
        """ send back and close """
        logs.logger.debug("err_response on %s" % self)
        self.push(data)
        self.close_when_done()

    def get_organ_id(self):
        """ provides informations about signal sender """
        return self.host_addr

    def __str__(self):
        return "Synapse(%s <-> %s)" % (self.host_addr, self.target.__name__)
    
    def log(self, message):
        """ provides logs from asyncore module """
        logs.logger.debug("asyncore log: %s" % message)

    def log_info(self, message, msg_type='info'):
        """ provides logs from asyncore module """
        logs.logger.debug("asyncore log: %s, %s" % (msg_type, message))  

class NetworkNeuron(asyncore.dispatcher):
    """ Provides asynchronous network communication, represented by a
    neuronal connection.
    Expects: some output consumer (coroutine or an object implementing 'send' )
    Message format: (organ_id/synapse, message)"""
    def __init__(self, output_synapse, port=network.server_port):       
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        port_range = network.server_port_range + port
        # try to crate a listener in predefined portrange:
        while port < port_range:        
            try:
                self.bind(('', port))
                self.listen(5)
            except socket.error, reason:
                port += 1
                logs.logger.warning("Error: could not bind socket." +
                                    "Port: %s already in use" % port)
            else:
                self.port = port
                break
        else:
            logs.logger.critical("Error: could not bind socket")
            raise NeuronError(reason)
        logs.logger.debug("listen to: %s" % port)
        self.signal_filter = signal_filter(output_synapse, error_transmitter())

    def log(self, message):
        """ provides logs from asyncore module """
        logs.logger.debug("asyncore log: %s" % message)

    def log_info(self, message, msg_type='info'):
        """ provides logs from asyncore module """
        logs.logger.debug("asyncore log: %s, %s" % (msg_type, message))
        
    def handle_accept(self):
        sock, addr = self.accept()
        logs.logger.debug("accepts: %s" % [addr])
        logs.logger.debug("connections: %s" % len(self._map))
        _Synapse(sock, addr, self.signal_filter)

    def feed(self, amount = network.default_listen_time):
        """ Feeds the neuron with some time. Neuron spends this time for
        network transmissions."""
        asyncore.loop(timeout = amount, count = 1)
        
