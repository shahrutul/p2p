#! /Usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for ayncronous communication (non-threaded, non-blocking) with network
and ui organs.
You must provide some energy in terms of 'time' or this module will not
work correctly!
"""


from decorators import coroutine, singleton
from network_nerve import NetworkNeuron
from signal_protocol import Signal, ProtocolError
from config import network, logs


@coroutine
def whoami_signal_processor(transmitter):
    try:
        while True:
            synapse = (yield)
            signal = Signal('addr', synapse.organ_id)
            transmitter.send((synapse, signal))
            synapse.disconnect()
    finally:
        logs.logger.debug("whoami_processor closed")
                
@coroutine
def network_cortex(brain):
    """ process network signals """
    try:
        signal_transmitter = brain.network_neuron.signal_transmitter
        whoami_process = whoami_signal_processor(signal_transmitter)
        while True:       
            synapse, signal = (yield)
            try:
                logs.logger.debug("recieves data from %s" % synapse)
                if signal.type == 'whoami':
                    whoami_process.send(synapse)
                                
            except ProtocolError, reason:
                logs.logger.debug("filter error: %s,%s" % (synapse, reason))
                #err_sender.send((synapse, Signal.ProtocolError, str(reason)))
            else:                
                #processor.send((synapse, msg))
                print synapse,signal
    finally:
        logs.logger.debug("network_cortex closed")

@singleton
class Brain(object):
    """ Process input, produce output """
    def __init__(self):
        self.neighbours = {}
        self.network_neuron = NetworkNeuron()
        net_cortex = network_cortex(self)
        self.network_neuron.associate(net_cortex)

    def process(self, amount = network.default_listen_time):
        self.network_neuron.feed(amount)


        
        
    
