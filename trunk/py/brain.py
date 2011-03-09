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
from config import network



@coroutine
def input_processor(target):
    """ Checks 'high-level' correctness, filters out nonsense message!s """
    while True:           
        channel, msg = (yield)
        print msg
        if msg.name == "chat":
            print msg.args

@singleton
class NetworkCortex(object):
    """ Module for processing network signals. """
    def __init__(self):
        self.input = input_processor("dummy")
        self.network_neuron = NetworkNeuron(self.input)

    def process(self, amount = network.default_listen_time):
        self.network_neuron.feed(amount)
        
        
    
