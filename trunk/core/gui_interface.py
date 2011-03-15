#! /usr/bin/env python
# -*- coding: utf-8 -*-
# gui_interface.py
#
# The interface connects the brain and GUI.

from gui_main import myMainWindow


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
