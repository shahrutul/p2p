#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for ayncronous communication (non-threaded, non-blocking) with network
and ui organs.
You must provide some energy in terms of 'time' (calling Brains.process()
function, or this module will not work correctly!

creating: Brain()
message processing: Brain().process() or Brain.process(time)
default time value = 0.001s
suspend all activities with Brain().suspend()
resume: Brain.resume()
"""
import time
import random

from decorators import coroutine, singleton
from network_nerve import NetworkNeuron
from signal_protocol import Signal, ProtocolError
from config import network, logs, settings, last_known_neighbours


@coroutine
def whoami_processor(transmitter):
    """ process 'whoami' requests """
    try:
        while True:
            synapse = (yield)
            signal = Signal('youare', synapse.organ_id)
            transmitter.send((synapse, signal))
            synapse.disconnect()
    finally:
        logs.logger.debug("whoami_processor closed")
    
        
@coroutine
def network_interaction(brain):
    """ Active interaction with the network. Call its next()
    method periodically generate some active interaction!"""
    net_neuron = brain.network_neuron
    transmitter = net_neuron.signal_transmitter
    
    while brain.active:
        yield
        # check if we have some neighours (at least one):
        if len(brain.neighbours) == 0:
            # TODO: send some generic error and let the UI translate it!
            brain.errors_to_ui.send("No known neighbours for bootstrapping!")
            continue
            
        # obtain own adress if not done:   
        if not brain.organ_id:
            # send a whoami to a random neighbour
            random_neighbour = random.choice(brain.neighbours)
            synapse = net_neuron.connect(random_neighbour)
            transmitter.send((synapse, Signal('whoami')))
            logs.logger.debug("send a 'whoami' to %s", random_neighbour)
            wait = Wait(5) # TODO: remove hardcoding
            while wait and synapse.is_active():
                yield
            continue
        # check if neighbours are reachable:
    

@coroutine
def network_cortex(brain):
    """ process incoming network signals """
    try:
        signal_transmitter = brain.network_neuron.signal_transmitter
        whoami_target = whoami_processor(signal_transmitter)
        while brain.active:       
            synapse, signal = (yield)
            try:
                logs.logger.debug("recieves data from %s" % synapse)
                if signal.type == 'whoami':
                    whoami_target.send(synapse)
                    
                elif signal.type == 'youare':
                    if not brain.organ_id:
                        brain.organ_id = (signal.content[0],
                                          brain.network_neuron.port)
                
                
                                
            except ProtocolError, reason:
                logs.logger.debug("network cortex error: %s,%s" %
                                  (synapse, reason))
                signal_transmitter.send((synapse,
                                         Signal.ProtocolError, str(reason)))
            else:                
                #processor.send((synapse, msg))
                print synapse,signal
    finally:
        logs.logger.debug("network_cortex closed")

@coroutine
def errors_to_ui():
    err = None
    while True:
        last, err = err, (yield)
        if last != err:
            print err
        # TODO: write some code

class Wait():
    """ Non-blocking wait for x seconds.
    Usage:
    w=Wait(3)
    while/if w: ... do someting ..."""
    def __init__(self, seconds):
        self.start = time.time()
        self.seconds = seconds
    def __nonzero__(self):
        """ Implements bool() respresentation """
        return time.time() - self.start < self.seconds

@singleton
class Brain(object):
    """ Process input, produce output """
    def __init__(self):
        self.resume()

    def get_neighbours(self):
        return self.neighbours

    def resume(self):
        """ Resumes from suspend. Initializes all interfaces """            
        self.organ_id = None
        self.active = True
        self.network_neuron = NetworkNeuron()
        # coroutines:
        self.network_cortex = network_cortex(self)
        self.network_neuron.associate(self.network_cortex)
        self.network_interaction = network_interaction(self)
        
        self.errors_to_ui = errors_to_ui()
        self.neighbours = last_known_neighbours.values()

    def suspend(self):
        """ Closes all connections, cleans up and 'suspends'. """
        self.active = False
        self.network_neuron.suspend()
        self.network_cortex.close()
        self.network_interaction.close()
        settings.last_known_neighbours = self.neighbours
        settings.store()
    
    def process(self, amount = network.default_listen_time):
        self.network_neuron.feed(0.01) # TODO: reset default listen
        # it is not necessary to call it more than few times in a second:
        self.network_interaction.next()
        



    
