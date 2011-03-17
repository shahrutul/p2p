#! /usr/bin/env python
# -*- coding: utf-8 -*-
# gui_main.py
#
# The main class for the GUI.

import sys
import logging

from PySide import QtCore, QtGui
from time import localtime, strftime

import gui
from core.brain import Brain
from gui.gui_interface import BrainMessages, Query, QueryTime
from gui.gui_newquerywindow import MyNewQueryWindow
from gui.gui_detailswindow import MyDetailsWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(642, 539)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbSuche = QtGui.QLabel(self.centralwidget)
        self.lbSuche.setObjectName("lbSuche")
        self.verticalLayout.addWidget(self.lbSuche)
        self.twSuche = QtGui.QTreeWidget(self.centralwidget)
        self.twSuche.setObjectName("twSuche")
        self.verticalLayout.addWidget(self.twSuche)
        self.buttonFrame = QtGui.QFrame(self.centralwidget)
        self.buttonFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.buttonFrame.setObjectName("buttonFrame")
        self.gridLayout = QtGui.QGridLayout(self.buttonFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.pbNeu = QtGui.QPushButton(self.buttonFrame)
        self.pbNeu.setObjectName("pbNeu")
        self.gridLayout.addWidget(self.pbNeu, 0, 0, 1, 1)
        self.pbBearbeiten = QtGui.QPushButton(self.buttonFrame)
        self.pbBearbeiten.setObjectName("pbBearbeiten")
        self.gridLayout.addWidget(self.pbBearbeiten, 0, 1, 1, 1)
        self.pbEntfernen = QtGui.QPushButton(self.buttonFrame)
        self.pbEntfernen.setObjectName("pbEntfernen")
        self.gridLayout.addWidget(self.pbEntfernen, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.buttonFrame)
        self.lbErgebnisse = QtGui.QLabel(self.centralwidget)
        self.lbErgebnisse.setObjectName("lbErgebnisse")
        self.verticalLayout.addWidget(self.lbErgebnisse)
        self.twDetails = QtGui.QTreeWidget(self.centralwidget)
        self.twDetails.setObjectName("twDetails")
        self.verticalLayout.addWidget(self.twDetails)
        self.twLog = QtGui.QTreeWidget(self.centralwidget)
        self.twLog.setObjectName("twLog")
        self.verticalLayout.addWidget(self.twLog)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Peer2Peer 2011", None, QtGui.QApplication.UnicodeUTF8))
        self.lbSuche.setText(QtGui.QApplication.translate("MainWindow", "Suche:", None, QtGui.QApplication.UnicodeUTF8))
        self.twSuche.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Titel", None, QtGui.QApplication.UnicodeUTF8))
        self.twSuche.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Zeit", None, QtGui.QApplication.UnicodeUTF8))
        self.twSuche.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Kalendertage", None, QtGui.QApplication.UnicodeUTF8))
        self.twSuche.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Ort", None, QtGui.QApplication.UnicodeUTF8))
        self.twSuche.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Beschreibung", None, QtGui.QApplication.UnicodeUTF8))
        self.pbNeu.setText(QtGui.QApplication.translate("MainWindow", "&Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pbBearbeiten.setText(QtGui.QApplication.translate("MainWindow", "&Bearbeiten", None, QtGui.QApplication.UnicodeUTF8))
        self.pbEntfernen.setText(QtGui.QApplication.translate("MainWindow", "&Entfernen", None, QtGui.QApplication.UnicodeUTF8))
        self.lbErgebnisse.setText(QtGui.QApplication.translate("MainWindow", "Ergebnisse:", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Titel", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Zeit", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Kalendertage", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Ort", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Beschreibung", None, QtGui.QApplication.UnicodeUTF8))
        self.twLog.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))

        
class MyMainWindow(QtGui.QMainWindow, BrainMessages):    
    def pbNeuClicked(self):
        self.myNewQueryWindow = MyNewQueryWindow(self)
        self.myNewQueryWindow.setModal(True)
        self.myNewQueryWindow.myIsEdited = False
        self.myNewQueryWindow.show()    
    
    def pbBearbeitenClicked(self):
        item = self.ui.twSuche.currentItem()
        if not item:
            return

        self.myNewQueryWindow = MyNewQueryWindow(self)
        self.myNewQueryWindow.ui.leTitel.setText(item.myQuery.title)
        self.myNewQueryWindow.ui.leOrt.setText(item.myQuery.place)
        self.myNewQueryWindow.ui.teBeginn.setTime(QtCore.QTime(item.myQuery.query_time.from_hour, item.myQuery.query_time.from_minute,0,0))
        self.myNewQueryWindow.ui.teEnde.setTime(QtCore.QTime(item.myQuery.query_time.until_hour, item.myQuery.query_time.until_minute,0,0))
        if QueryTime.WEEKDAYS[0] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbMo.setChecked(True)
        if QueryTime.WEEKDAYS[1] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbDi.setChecked(True)
        if QueryTime.WEEKDAYS[2] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbMi.setChecked(True)
        if QueryTime.WEEKDAYS[3] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbDo.setChecked(True)
        if QueryTime.WEEKDAYS[4] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbFr.setChecked(True)
        if QueryTime.WEEKDAYS[5] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbSa.setChecked(True)
        if QueryTime.WEEKDAYS[6] in item.myQuery.query_time.weekdays:
            self.myNewQueryWindow.ui.cbSo.setChecked(True)
        self.myNewQueryWindow.ui.pteBeschreibung.clear()
        self.myNewQueryWindow.ui.pteBeschreibung.insertPlainText(item.myQuery.description)
        self.myNewQueryWindow.myIsEdited = True
        self.myNewQueryWindow.myUuidToDelete = item.myUuid
        self.myNewQueryWindow.setModal(True)
        self.myNewQueryWindow.show()
        
    def pbEntfernenClicked(self):
        item = self.ui.twSuche.currentItem()
        if not item:
            return
        self.brain.deleteQueryEntryById(item.myUuid)
    
    def twDetailsItemDoubleClicked(self, item = None, columnIndex = None):
        item = self.ui.twDetails.currentItem()
        if not item:
            return
        
        if item.myUuid in self.dictMyDetailsWindow:
            self.dictMyDetailsWindow.get(item.myUuid).show()
        else:
            #...        
            self.myDetailsWindow = MyDetailsWindow(self)
            self.dictMyDetailsWindow[item.myUuid] = self.myDetailsWindow
            
            # load query-data into new detail-window
            self.internalLoadDetailWindowData(self.dictMyDetailsWindow[item.myUuid], item.myQuery)
            
            # activate "Detail" tab and save UUID in window instance
            self.myDetailsWindow.ui.tabs.setCurrentIndex(0)
            self.myDetailsWindow.myUuid = item.myUuid
            self.myDetailsWindow.show()

    
    ''' ##################################################################### '''

    def reloadQueryEntries(self, userQueries):        
        self.internalReloadEntries(userQueries, self.ui.twSuche)
            
            
    def reloadResultEntries(self, userResults):
        # remove all detail-windows which are not present in userResults
        self.newDict = dict()
        for key, value in self.dictMyDetailsWindow.items():
            if key not in userResults:
                self.dictMyDetailsWindow[key].close()
            else:
                self.newDict[key] = value
        
        self.dictMyDetailsWindow = self.newDict
        self.internalReloadEntries(userResults, self.ui.twDetails)
        
    def pickupChatMsg(self, inQuery, inOppositeNick, inChatMessage, inUuid):
        if inUuid in self.dictMyDetailsWindow:
            self.dictMyDetailsWindow[inUuid].insertChatMessage(inChatMessage, inOppositeNick)
            self.dictMyDetailsWindow[inUuid].ui.tabs.setCurrentIndex(1)
            self.dictMyDetailsWindow[inUuid].show()
        else:
            # create new entry and save in dictionary
            self.myDetailsWindow = MyDetailsWindow(self)
            self.dictMyDetailsWindow[inUuid] = self.myDetailsWindow
            
            # load query-data into new detail-window
            self.internalLoadDetailWindowData(self.dictMyDetailsWindow[inUuid], inQuery)
            
            # activate "chat"-tab and save UUID in window instance
            self.dictMyDetailsWindow[inUuid].ui.tabs.setCurrentIndex(1)
            self.dictMyDetailsWindow[inUuid].myUuid = inUuid
            self.dictMyDetailsWindow[inUuid].insertChatMessage(inChatMessage, inOppositeNick)
            self.dictMyDetailsWindow[inUuid].show()
            

            
    ''' ##################################################################### '''
    
    def internalLoadDetailWindowData(self, inDetailsWindow, inQuery):
        # set detail data
        inDetailsWindow.ui.leTitel.setText(inQuery.title)
        inDetailsWindow.ui.leOrt.setText(inQuery.place)
        inDetailsWindow.ui.teBeginn.setTime(QtCore.QTime(inQuery.query_time.from_hour, inQuery.query_time.from_minute,0,0))
        inDetailsWindow.ui.teEnde.setTime(QtCore.QTime(inQuery.query_time.until_hour, inQuery.query_time.until_minute,0,0))
        if QueryTime.WEEKDAYS[0] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbMo.setChecked(True)
        if QueryTime.WEEKDAYS[1] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbDi.setChecked(True)
        if QueryTime.WEEKDAYS[2] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbMi.setChecked(True)
        if QueryTime.WEEKDAYS[3] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbDo.setChecked(True)
        if QueryTime.WEEKDAYS[4] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbFr.setChecked(True)
        if QueryTime.WEEKDAYS[5] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbSa.setChecked(True)
        if QueryTime.WEEKDAYS[6] in inQuery.query_time.weekdays:
            inDetailsWindow.ui.cbSo.setChecked(True)
        # load description
        inDetailsWindow.ui.pteBeschreibung.clear()
        inDetailsWindow.ui.pteBeschreibung.insertPlainText(inQuery.description)


    def internalReloadEntries(self, queries, treeWidget):
        treeWidget.clear()
        
        ''' Todo: Sortiert ausgeben? '''
        entries = list(queries.items())
        sorted_entries = sorted(entries, cmp=lambda x,y:
                                cmp(x[1].title.lower(), y[1].title.lower()))
        for key, query in sorted_entries:
            newItem = QtGui.QTreeWidgetItem(treeWidget)
            
            newItem.setText(0, query.title)
            
            self.fromHour = str(query.query_time.from_hour)
            if len(self.fromHour) <= 1:
                self.fromHour = "0" + self.fromHour 
            self.fromMinute = str(query.query_time.from_minute)
            if len(self.fromMinute) <= 1:
                self.fromMinute = "0" + self.fromMinute
            self.untilHour = str(query.query_time.until_hour)
            if len(self.untilHour) <= 1:
                self.untilHour = "0" + self.untilHour
            self.untilMinute = str(query.query_time.until_minute)
            if len(self.untilMinute) <= 1:
                self.untilMinute = "0" + self.untilMinute
            newItem.setText(1, self.fromHour + ":" + self.fromMinute +
                             "-" + self.untilHour + ":" + self.untilMinute)
            self.newWeekdays = ""
            if query.query_time.WEEKDAYS[0] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "Mo "
            if query.query_time.WEEKDAYS[1] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "Di "
            if query.query_time.WEEKDAYS[2] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "Mi "
            if query.query_time.WEEKDAYS[3] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "Do "
            if query.query_time.WEEKDAYS[4] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "Fr "
            if query.query_time.WEEKDAYS[5] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "Sa "
            if query.query_time.WEEKDAYS[6] in query.query_time.weekdays:
                self.newWeekdays = self.newWeekdays + "So "
            newItem.setText(2, self.newWeekdays)
            newItem.setText(3, query.place)
            
            self.newDescriptionWithoutReturns = unicode(query.description.replace("\n", " "))
            newItem.setText(4, self.newDescriptionWithoutReturns)
            newItem.myUuid = key
            newItem.myQuery = query
            treeWidget.addTopLevelItem(newItem)
            
            

    def log(self, inString):
        sItemText = strftime("%H:%M:%S", localtime()) + ": " + inString
        newItem = QtGui.QTreeWidgetItem(self.ui.twLog)
        newItem.setText(0, sItemText)
        self.ui.twLog.addTopLevelItem(newItem)
        ''' always scroll '''
        self.ui.twLog.setCurrentItem(newItem)
        
        
        
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.dictMyDetailsWindow = dict()
        
        ' Signals '
        QtCore.QObject.connect(self.ui.pbNeu, QtCore.SIGNAL('clicked()'), self.pbNeuClicked)
        QtCore.QObject.connect(self.ui.pbBearbeiten, QtCore.SIGNAL('clicked()'), self.pbBearbeitenClicked)
        QtCore.QObject.connect(self.ui.pbEntfernen, QtCore.SIGNAL('clicked()'), self.pbEntfernenClicked)
        QtCore.QObject.connect(self.ui.twSuche, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *, int)'), self.pbBearbeitenClicked)
        QtCore.QObject.connect(self.ui.twDetails, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *, int)'), self.twDetailsItemDoubleClicked)


    def closeEvent(self, event):
        self.brain.suspend()


class GUILogger(logging.Handler):
    def __init__(self, myMainWindow_):
        logging.Handler.__init__(self)
        self.myMainWindow = myMainWindow_
    
    def emit(self, record):
        msg = self.format(record)
        self.myMainWindow.log(msg)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myMainWindow = MyMainWindow()
    
    myGUILogger = GUILogger(myMainWindow)
    logging.getLogger().addHandler(myGUILogger)

    myMainWindow.brain = Brain()
    myMainWindow.brain.registerUI(myMainWindow)
    
    brainTimer = QtCore.QTimer()
    QtCore.QObject.connect(brainTimer, QtCore.SIGNAL("timeout()"), myMainWindow.brain.process)
    brainTimer.start(100)
    
    myMainWindow.show()    
    sys.exit(app.exec_())
    
