#! /usr/bin/env python
# -*- coding: utf-8 -*-
# gui_interface.py
#
# The interface connects the brain and GUI.



''' ###### 1 ######'''
''' GUI --> brain '''
def createNewSearchEntry(newSearchEntry):
    pass

''' brain --> GUI '''
def reloadSearchEntries():
    pass

''' GUI --> brain '''
def getAllSearchEntries():
    pass

''' HINWEIS: reloadSearchEntries oder getAllSearchEntries eventuell überflüssig '''



''' ###### 2 ###### '''
''' GUI --> brain '''
def getSearchEntryById(id):
    pass

''' GUI --> brain '''
def setSearchEntryById(id, data):
    pass

''' ###### 2.1 ###### '''
''' GUI --> brain '''
def deleteSearchEntryById(id):
    pass



''' ###### 3 ###### '''
''' brain --> GUI '''
def reloadResultsForSearchId(id):
    pass



''' ###### 4 ###### '''
''' GUI --> brain '''
def getDetailResult(searchId, resultId):
    pass



''' ###### 5 ###### '''
''' GUI --> brain '''
def sendChatMsg(msg, receiver):
    pass



''' ###### 6 ###### '''
''' brain --> GUI '''
def pickupChatMsg():
    pass
