#! /usr/bin/env python
# -*- coding: utf-8 -*-
# gui_interface.py
#
# The interface connects the brain and GUI.

#from gui_main import myMainWindow
import datetime
class QueryTime(object):
    """ Query time data storage struct """
    WEEKDAYS = ["mo", "tue", "wed", "thu", "fri", "sat", "sun"]

    def __init__(self, from_hour, from_minute, until_hour,
                 until_minute, weekdays):
        # validate hour/minutes values
        datetime.time(from_hour, from_minute)
        datetime.time(until_hour, until_minute)
        # check weekdays
        if len(weekdays) == 0:
            raise ValueError("weekday must be in 0..6 or %r, not empty!" %
                             (QueryTime.WEEKDAYS))
        self.weekdays = []
        for day in weekdays:
            if day in QueryTime.WEEKDAYS:
                self.weekdays.append(day)
            elif 0 <= day < len(QueryTime.WEEKDAYS):
                self.weekdays.append(QueryTime.WEEKDAYS[day])
            else:
                raise ValueError("weekday must be in 0..6 or %r" %
                                   (QueryTime.WEEKDAYS))
                
        self.from_hour = from_hour
        self.from_minute = from_minute
        self.until_hour = until_hour
        self.until_minute = until_minute
        self.weekdays = list(set(self.weekdays))
        
class Query(object):
    """ Query data struct for gui communications"""
    def __init__(self, title, place, query_time, description, id_=None):        
        self.title = str(title)
        self.place = str(place)
        self.query_time = query_time
        self.description = str(description)
        self.id = id_

class UIMessages(object):
    ''' ###### 1 ######'''
    ''' GUI --> brain '''
    def createNewQueryEntry(newSearchEntry):
        raise NotImplementedError
    
    ''' GUI --> brain '''
    def getAllQueryEntries():
        raise NotImplementedError

    ''' ###### 2 ###### '''
    ''' GUI --> brain '''
    def getQueryEntryById(id):
        raise NotImplementedError

    ''' GUI --> brain '''
    def setQueryEntryById(id, data):
        raise NotImplementedError
    
    ''' ###### 4 ###### '''
    ''' GUI --> brain '''
    def getDetailResult(queryId, resultId):
        raise NotImplementedError

    ''' ###### 5 ###### '''
    ''' GUI --> brain '''
    def sendChatMsg(msg, receiver):
        raise NotImplementedError
    
    ''' ###### 2.1 ###### '''
    ''' GUI --> brain '''
    def deleteQueryEntryById(id):
        raise NotImplementedError

    ''' HINWEIS: reloadSearchEntries oder getAllSearchEntries eventuell überflüssig '''

class BrainMessages(object):    
    ''' brain --> GUI '''
    def reloadQueryEntries():
        raise NotImplementedError

    ''' ###### 3 ###### '''
    ''' brain --> GUI '''
    def reloadResultsForQueryId(id):
        raise NotImplementedError

    ''' ###### 6 ###### '''
    ''' brain --> GUI '''
    def pickupChatMsg():
        raise NotImplementedError


# obsolete! import logging in GUI and register your log-outputter:
"""
 import logging
 
    class GUILogger(logging.Handler):
        def emit(self, record):
            msg = self.format(record)
            myMainWindow.logMessage(msg)
            
    logging.getLogger().addHandler(GUILogger())
"""
    
''' ###### 7 ###### '''
''' brain --> GUI '''
def logMessage(msg):   
    myMainWindow.log(msg)
