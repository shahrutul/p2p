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
from config import (network, logs, settings,  # pylint: disable=E0611
                    last_known_neighbours)


def time_stamp():
    """ A uniform timestamp """
    return time.time()


@coroutine
def whoami_processor():
    """ process 'whoami' requests """
    while True:
        synapse = (yield)
        signal = Signal('youare', synapse.organ_id)
        synapse.transmit(signal)
        synapse.disconnect()


@coroutine
def pipeline(sender):
    """ forwards signals from ping/query/etc broadcasts to the sender """
    logs.logger.debug("anonyme pipeline started")
    try:
        while sender.is_active():
            synapse, signal = (yield)
            logs.logger.debug("forwards a %s from %s" % (signal, synapse))
            sender.transmit(signal)
    finally:
        logs.logger.debug("anonyme pipeline closed")
        sender.disconnect()


@coroutine
def ping_processor(brain):
    """ process 'ping' requests """
    while brain.active:
        try:
            synapse, ping = (yield)
            ping_id, ttl, hops = ping

            if ping_id in brain.ping_cache:
                continue
            else:
                brain.ping_cache[ping_id] = time_stamp()

            # check ttl/hops
            if (0 < ttl < network.max_ttl) and (0 <= hops < network.max_hops):
                ttl -= 1
                hops += 1
            else:
                continue
            # send a pong:
            synapse.transmit(Signal('pong', brain.organ_id))
            if ttl > 0:
                # send broadcast (target <--pipe <-- neigh_responses)
                pipe = pipeline(synapse)
                for neigh in brain.neighbours.without(synapse.organ_id):
                    neigh_synapse = brain.network_neuron.connect(neigh, pipe)
                    neigh_synapse.transmit(Signal('ping', (ttl, hops)))

        except ValueError, reason:
            err_response = Signal('error', (Signal.ProtocolError, str(reason)))
            synapse.transmit((synapse, err_response))
            synapse.disconnect()


@coroutine
def network_explorer(brain):
    """ Explores the network with pings. Starts with ttl = 1. Ends with
    ttl = max_ttl. Waits for longer times to avoid unnecessary traffic.
    Call it only if not enough neighbours available! """
    while True:
        explore_level = 0
        while explore_level < network.max_ttl:
            explore_level += 1
            logs.logger.debug("Explore the network with ping(%s)"
                              % explore_level)
            for neigh in brain.neighbours.without(None):
                synapse = brain.network_neuron.connect(neigh)
                synapse.transmit(Signal('ping', (explore_level, 0)))
                wait = Wait(network.explore_step_timeout)
                while wait:
                    yield
        else:
            # explore level exceeded, wait for longer time:
            wait = Wait(network.explore_round_timeout)
            while wait:
                yield


@coroutine
def network_interaction(brain):
    """ Active interaction with the network. Call its next()
    method periodically generate some active interaction!"""
    net_neuron = brain.network_neuron
    explorer = network_explorer(brain)
    while brain.active:
        yield
        # check if we have some neighours (at least one):
        if len(brain.neighbours) == 0:
            continue

        # obtain own adress if not done:
        if not brain.organ_id:
            rand_neighbour = random.choice(list(brain.neighbours))
            synapse = net_neuron.connect(rand_neighbour)
            synapse.transmit(Signal('whoami'))
            logs.logger.debug("send a 'whoami' to %s" % str(rand_neighbour))
            wait = Wait(network.wait_for_whoami)
            while wait and synapse.is_active():
                yield
            # there is no response:
            if not brain.organ_id:
                logs.logger.debug("remove neighbour %s" % str(rand_neighbour))
                del(brain.neighbours[rand_neighbour])
                continue
        # ok, now check if enough neighbours or candidates available,
        # else explore the network:
        if len(brain.neighbours) < network.min_neighbours:
            explorer.next()


@coroutine
def network_cortex(brain):
    """ process incoming network signals.
    'Passive' interactions/responses only."""
    whoami_target = whoami_processor()
    ping_target = ping_processor(brain)
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
            elif signal.type == 'ping':
                ping_target.send((synapse, signal))

            elif signal.type == 'pong':
                if synapse.signal_target is not None:
                    synapse.signal_target.send((synapse, signal))

        except ProtocolError, reason:
            logs.logger.debug("network cortex error: %s,%s" %
                              (synapse, reason))
            synapse.transmit(Signal.ProtocolError, str(reason))
        else:
                #processor.send((synapse, msg))
            print synapse, signal


@coroutine
def errors_to_ui():
    """ sends errors to ui """
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
        self.start = time_stamp()
        self.seconds = seconds

    def __nonzero__(self):
        """ Implements bool() respresentation """
        return time_stamp() - self.start < self.seconds


class Neighbours(dict):
    """ Manages neighbours (a simple dict with neighbour:time_stamp values)"""
    def __init__(self, neighbours=(), timestamp=None):
        dict.__init__(self)
        for neigh in neighbours:
            self.add(neigh, timestamp)

    def add(self, neighbour, timestamp=time_stamp()):
        """ adds a neighbour and a default time value """
        self[neighbour] = timestamp

    def without(self, neighbour):
        """ returns a key list without 'neighbour' """
        return [key for key in self.keys() if key != neighbour]


@singleton
class Brain(object):
    """ Process input, produce output """
    def __init__(self):
        self.resume()

    def resume(self):
        """ Resumes from suspend. Initializes all interfaces """
        self.organ_id = None
        self.active = True
        self.fallback = False
        self.network_cortex = network_cortex(self)
        self.network_neuron = NetworkNeuron(self.network_cortex)
        self.network_interaction = network_interaction(self)

        self.errors_to_ui = errors_to_ui()
        self.ping_cache = {}
        self.neigh_candidates = Neighbours()
        self.neighbours = Neighbours(last_known_neighbours.values())

    def suspend(self):
        """ Closes all connections, cleans up and 'suspends'. """
        self.active = False
        self.fallback = False
        self.network_neuron.suspend()
        self.network_cortex.close()
        self.network_interaction.close()
        settings.last_known_neighbours = self.neighbours.without(None)
        settings.store()

    def process(self, amount=network.default_listen_time):
        self.network_neuron.feed(amount)  # TODO: reset default listen
        # it is not necessary to call it more than few times in a second.
        # No active interactions without neighbours:
        if len(self.neighbours) > 0:
            self.network_interaction.next()
        elif not self.fallback:
            # fallback to well known servers
            self.fallback = True
            self.neighbours = Neighbours(settings.fallback_servers.values())
        else:
            # hm, we have a problem!
            self.errors_to_ui.send("No known neighbours for bootstrapping!")
