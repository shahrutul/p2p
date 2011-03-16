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
import uuid

from gui_interface import UIMessages, Query
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
        logs.logger.debug("send a 'youare' to %s" % str(synapse))
        signal = Signal('youare', synapse.organ_id)
        synapse.transmit(signal)
        synapse.disconnect()


@coroutine
def ping_sender(brain):
    """ sends keep-alive/explore pings to neighbours  """
    while brain.active:
        ttl, neighbour = (yield)
        ping_id = str(uuid.uuid1())
        brain.ping_cache[ping_id] = time_stamp()
        synapse = brain.network_neuron.connect(neighbour)
        synapse.transmit(Signal('ping', (ping_id, ttl, 0)))


@coroutine
def ping_processor(brain):
    """ process 'ping' requests """
    while brain.active:
        try:
            synapse, ping = (yield)
            ping_id, ttl, hops = ping

            if ping_id in brain.ping_cache:
                logs.logger.debug("discard ping request %s" % str(ping))
                synapse.disconnect()
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
            if brain.organ_id:
                synapse.transmit(Signal('pong', brain.organ_id))
            # send broadcast to neighbours
            if ttl > 0:
                for neigh in brain.neighbours.keys():
                    #if neigh[0] == synapse.organ_id[0]:   # TODO: reenable it for "real world"
                    #    continue
                    neigh_synapse = brain.network_neuron.connect(neigh, synapse)
                    logs.logger.debug("broadcast %s to %s" %(ping, str(neigh)))
                    neigh_synapse.transmit(Signal('ping',
                                                  (ping_id, ttl, hops)))
            else:
                synapse.disconnect()

        except ValueError, reason:
            logs.logger.debug("ping processor protocol error %s" % str(reason))
            err_response = Signal('error', (Signal.ProtocolError, str(reason)))
            synapse.transmit((synapse, err_response))
            synapse.disconnect()


@coroutine
def network_explorer(brain):
    """ Explores the network with pings. Starts with ttl = 1. Ends with
    ttl = max_ttl. Waits for a while to avoid unnecessary traffic.
    Call it only if necessary (e.g if there are not enough neighbours) """
    pinger = ping_sender(brain)
    while brain.active:
        explore_level = 0
        while len(brain.neighbours) == 0:
            yield

        while explore_level < network.max_ttl:
            explore_level += 1
            logs.logger.debug("Explore the network with ping(%s)"
                              % explore_level)
            for neigh in brain.neighbours.keys():
                pinger.send((explore_level, neigh))
                wait = Wait(network.explore_step_timeout)
                while wait:
                    yield
        else:
            # max explore level reached, wait for longer time and retry:
            wait = Wait(network.explore_round_timeout)
            while wait:
                yield


@coroutine
def identity_resolver(brain):
    """ obtains own network address """
    net_neuron = brain.network_neuron
    try:
        while not brain.organ_id:
            # if there are no neighbours, do noting
            while len(brain.neighbours) == 0:
                yield
            rand_neighbour = random.choice(list(brain.neighbours))
            synapse = net_neuron.connect(rand_neighbour)
            synapse.transmit(Signal('whoami', (brain.network_neuron.port)))
            logs.logger.debug("send a 'whoami' to %s" % str(rand_neighbour))
            wait = Wait(network.wait_for_whoami)
            while wait and synapse.is_active():
                yield
            synapse.disconnect()
            # TODO: delete or not delete?, that is the question
            if not brain.organ_id:
                logs.logger.debug("remove neighbour %s" % str(rand_neighbour))
                brain.neighbours.pop(rand_neighbour, None)
            continue
    finally:
        logs.logger.debug("indentity resolver closed")


@coroutine
def candidates_processor(brain):
    """ process pongs/whoami's, extracts contact data and adds sender
    to 'neighbour candidates' """
    while brain.active:
        synapse, signal = (yield)
        if signal.type == 'pong':
            # case 1: a 'refresh' pong from a neighbour:
            neigh = tuple(signal.content)
            if neigh in brain.neighbours:
                # refresh
                logs.logger.debug("referesh %s" % str(neigh))
                brain.neighbours.add(neigh)
                brain.neigh_refresh.pop(neigh, None)
                continue
            # case 2: a whoami from unknown
        elif signal.type == 'whoami':
            neigh = tuple((synapse.organ_id[0], signal.content[0]))

        # it is a pong/whoami from unknown. Add it to neighbour candidates.
        if len(brain.neigh_candidates) < network.max_candidates:
            brain.neigh_candidates.add(neigh)
            logs.logger.debug("whoami to candidates %s" % str(neigh))


@coroutine
def network_interaction(brain):
    """ Active interaction with the network. Call its next()
    method periodically generate some active interaction!"""
    explorer = network_explorer(brain)
    id_resolver = identity_resolver(brain)
    wait_for_ping_cleanup = Wait(network.ping_cache_storage_time)
    wait_for_neighbours_cleanup = Wait(network.cleanup_period)
    pinger = ping_sender(brain)
    while brain.active:
        yield
        # obtain own adress if not done:
        if not brain.organ_id:
            id_resolver.next()

        # check, if enough neighbours or candidates available,
        # else explore the network:
        if len(brain.neighbours) < network.min_neighbours:
            if len(brain.neigh_candidates):
                while len(brain.neighbours) < network.min_neighbours and \
                      len(brain.neigh_candidates) > 0:
                    brain.neighbours.update([brain.neigh_candidates.popitem()])
            else:
                explorer.next()
        # it is time for a cleanup?
        # remove too old entries from neigh_candidates, neigh_refresh and
        # ping_cache
        if not wait_for_ping_cleanup:
            wait_for_ping_cleanup = Wait(network.ping_cache_cleanup)
            brain.ping_cache.cleanup(network.ping_cache_cleanup)

        if not wait_for_neighbours_cleanup:
            wait_for_neighbours_cleanup = Wait(network.cleanup_period)
            brain.neigh_candidates.cleanup(network.neighbour_timeout)
            brain.neighbours.cleanup(network.neighbour_timeout)
            brain.neigh_refresh.cleanup(network.neighbour_timeout)
            # look for old neighbour entries and sends a ping
            act_time = time_stamp()
            min_time = network.neighbour_timeout - (network.cleanup_period * 2)
            for neighbour, timestamp in brain.neighbours.items():
                if (((act_time - timestamp) > min_time) and
                    neighbour not in brain.neigh_refresh):
                    brain.neigh_refresh[neighbour] = timestamp
                    pinger.send((1, neighbour))
                    logs.logger.debug("sends a refresh ping to %s" %
                                      str(neighbour))


@coroutine
def network_cortex(brain):
    """ process incoming network signals.
    'Passive' interactions/responses only."""
    whoami_target = whoami_processor()
    ping_target = ping_processor(brain)
    candidate_target = candidates_processor(brain)
    while brain.active:
        synapse, signal = (yield)
        try:
            logs.logger.debug("recieves data from %s" % synapse)
            if signal.type == 'whoami':
                whoami_target.send(synapse)
                candidate_target.send((synapse, signal))

            elif signal.type == 'youare':
                if not brain.organ_id:
                    brain.organ_id = (signal.content[0],
                                      brain.network_neuron.port)
            elif signal.type == 'ping':
                ping_target.send((synapse, signal.content))

            elif signal.type == 'pong':
                # process pong
                candidate_target.send((synapse, signal))
                # and forward, if necessary
                if synapse.signal_target is not None:
                    logs.logger.debug("pipes pong to %s" %
                                      str(synapse.signal_target))
                    synapse.signal_target.transmit(signal)

        except ProtocolError, reason:
            logs.logger.debug("network cortex error: %s,%s" %
                              (synapse, reason))
            err_response = Signal('error',
                                  (Signal.ProtocolError, str(reason)))
            synapse.transmit(err_response)
            synapse.disconnect()


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


class TimeStampDict(dict):
    """ Manages time-depended items
    (a simple dict with item:time_stamp values)"""
    def __init__(self, items=(), timestamp=None):
        dict.__init__(self)
        for item in items:
            self.add(item, timestamp)

    def add(self, item, timestamp=None):
        """ adds an item and a default time value """
        if not timestamp:
            timestamp = time_stamp()
        self[item] = timestamp

    def cleanup(self, max_time):
        """ removes old entries """
        act_time = time_stamp()
        new_items = ((item, val) for item, val in self.items()
                       if act_time - val < max_time)
        self.clear()
        self.update(new_items)


@singleton
class Brain(UIMessages):
    """ Process input, produce output """
    def __init__(self, ui = None):
        self.resume()

    def createNewQueryEntry(entry):
        if not isinstance(entry, Query):
            raise ValueError("not a query!")
        self.user_queries[uuid.uuid1()] = entry

    def getAllQueryEntries():
        return self.user_queries.copy()

    def getQueryEntryById(id):
        return self.user_queries.get(id)

    def setQueryEntryById(id, data):
        raise NotImplementedError
    
    def getDetailResult(queryId, resultId):
        raise NotImplementedError
    
    def sendChatMsg(msg, receiver):
        raise NotImplementedError
    
    def deleteQueryEntryById(id):
        self.user_queries.pop(id, None)

    def resume(self):
        """ Resumes from suspend. Initializes all interfaces """
        self.ping_cache = {}
        self.user_queries = {}
        self.interaction_pause = Wait(2)
        self.neigh_candidates = TimeStampDict()
        self.neigh_refresh = TimeStampDict()

        self.organ_id = None
        self.active = True
        self.fallback = False
        self.neighbours = TimeStampDict(last_known_neighbours.values())
        self.network_cortex = network_cortex(self)
        self.network_neuron = NetworkNeuron(self.network_cortex)
        self.network_interaction = network_interaction(self)
        self.errors_to_ui = errors_to_ui()

    def suspend(self):
        """ Closes all connections, cleans up and 'suspends'. """
        self.active = False
        self.network_neuron.suspend()
        self.network_cortex.close()
        self.network_interaction.close()
        settings.last_known_neighbours = self.neighbours.keys()
        settings.store()

    def process(self, amount=network.default_listen_time):
        """ process incoming signals and generates some active output
        (pings neighbours, explores the network) """
        self.network_neuron.feed(amount)
        # it is not necessary to call it more than few times in a second.
        # No active interactions without neighbours:
        if (len(self.neighbours) > 0) or (len(self.neigh_candidates) > 0):
            if not self.interaction_pause:
                self.interaction_pause = Wait(2)
                self.network_interaction.next()
        elif not self.fallback:
            # fallback to well known servers
            self.fallback = True
            self.neighbours = TimeStampDict(settings.fallback_servers.values())
            logs.logger.debug("Fallback to well known servers %s" %
                              str(self.neighbours.keys()))
        else:
            # hm, we have a problem!
            self.errors_to_ui.send("No known neighbours!")
