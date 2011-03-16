#! /usr/bin/env python
# -*- coding: utf-8 -*-
# gui_main.py
#
# The main class for the GUI.

from brain import Brain

from gui_interface import BrainMessages, Query, QueryTime
from gui_newquerywindow import MyNewQueryWindow
from gui_detailswindow import MyDetailsWindow

from PySide import QtCore, QtGui
from time import localtime, strftime
import sys
import logging


from PySide import QtCore, QtGui

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
        self.myNewQueryWindow.myIsEdited = False
        self.myNewQueryWindow.show()
    
    
    def pbBearbeitenClicked(self):
        item = self.ui.twSuche.currentItem()
        if not item:
            #self.log("Kein Item selektiert!")
            return
        #index = self.ui.twSuche.indexOfTopLevelItem(item)
        #print index
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
        self.myNewQueryWindow.show()
    
        
    def pbEntfernenClicked(self):
        item = self.ui.twSuche.currentItem()
        if not item:
            #self.log("Kein Item selektiert!")
            return
        self.brain.deleteQueryEntryById(item.myUuid)
        
    
    def twDetailsItemDoubleClicked(self, item = None, columnIndex = None):
        self.log("Detailfeld doppelt angeklickt.")
        if columnIndex != None:
            pass
        self.myDetailsWindow = MyDetailsWindow()
        self.myDetailsWindow.ui.tabs.setCurrentIndex(0)
        ''' Todo: chat(1) wieder rausnehmen '''
        self.myDetailsWindow.ui.tabs.setTabText(1, "Chat (1)")
        self.myDetailsWindow.show()

    
    ''' ##################################################################### '''

    def reloadQueryEntries(self, userQueries):
        self.ui.twSuche.clear()
        
        ''' Todo: Sortiert ausgeben? '''
        for key, query in userQueries.items():
            newItem = QtGui.QTreeWidgetItem(self.ui.twSuche)
            
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
            #newItem.setText(2, query.query_time.weekdays)
            newItem.setText(3, query.place)
            
            self.newDescriptionWithoutReturns = unicode(str(query.description).replace("\n", " "))
            
            #exifUI.setWindowTitle(QtGui.QApplication.translate("exifUI", "Form", None, QtGui.QApplication.UnicodeUTF8))
            newItem.setText(4, self.newDescriptionWithoutReturns)
            newItem.myUuid = key
            newItem.myQuery = query
            self.ui.twLog.addTopLevelItem(newItem)

    ''' ##################################################################### '''

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
        
        ' Signals '
        QtCore.QObject.connect(self.ui.pbNeu, QtCore.SIGNAL('clicked()'), self.pbNeuClicked)
        QtCore.QObject.connect(self.ui.pbBearbeiten, QtCore.SIGNAL('clicked()'), self.pbBearbeitenClicked)
        QtCore.QObject.connect(self.ui.pbEntfernen, QtCore.SIGNAL('clicked()'), self.pbEntfernenClicked)
        QtCore.QObject.connect(self.ui.twSuche, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *, int)'), self.pbBearbeitenClicked)
        QtCore.QObject.connect(self.ui.twDetails, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *, int)'), self.twDetailsItemDoubleClicked)


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
    
    #brainTimer = QtCore.QTimer()
    #QtCore.QObject.connect(brainTimer, QtCore.SIGNAL("timeout()"), myMainWindow.brain.process)
    #brainTimer.start(1)
    
    myMainWindow.show()    
    sys.exit(app.exec_())
    
'''
        msgBox = QtGui.QMessageBox.question(self, 'Ueberschrift', "Die Nachricht ....", QtGui.QMessageBox.Ok)
self.ui.twLog.clear()
'''