#! /usr/bin/env python
# -*- coding: utf-8 -*-
# gui_interface.py
#
# The interface connects the brain and GUI.

#from gui_main import myMainWindow

class QueryTime(object):
    """ Query time data storage struct """
    WEEKDAYS = ["mo", "tue", "wed", "thu", "fri", "sat", "sun"]
    class Weekday: mo, tue, wed, thu, fri, sat, sun = QueryTime.WEEKDAYS
    def __init__(self, from_hour, from_minute, until_hour,
                 until_minute, weekdays):
        self.from_hour = from_hour
        self.from_minute = from_minute
        self.until_hour = until_hour
        self.until_minute = until_minute
        self.weekdays = weekdays
        
class Query(object):
    """ Query data struct for gui communications"""
    def __init__(self, title, place, query_time, description, id_=None):        
        self.title = title
        self.place = place
        self.query_time = query_time
        self.description = description
        self.id = id_


''' ###### 1 ######'''
''' GUI --> brain '''
def createNewQueryEntry(newSearchEntry):
    pass

''' brain --> GUI '''
def reloadQueryEntries():
    pass

''' GUI --> brain '''
def getAllQueryEntries():
    pass

''' HINWEIS: reloadSearchEntries oder getAllSearchEntries eventuell überflüssig '''



''' ###### 2 ###### '''
''' GUI --> brain '''
def getQueryEntryById(id):
    pass

''' GUI --> brain '''
def setQueryEntryById(id, data):
    pass

''' ###### 2.1 ###### '''
''' GUI --> brain '''
def deleteQueryEntryById(id):
    pass



''' ###### 3 ###### '''
''' brain --> GUI '''
def reloadResultsForQueryId(id):
    pass



''' ###### 4 ###### '''
''' GUI --> brain '''
def getDetailResult(queryId, resultId):
    pass



''' ###### 5 ###### '''
''' GUI --> brain '''
def sendChatMsg(msg, receiver):
    pass



''' ###### 6 ###### '''
''' brain --> GUI '''
def pickupChatMsg():
    pass


''' ###### 7 ###### '''
''' brain --> GUI '''
def logMessage(msg):
    myMainWindow.log(msg)
