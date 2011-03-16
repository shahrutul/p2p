#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from gui_interface import *

class Ui_NewQueryWindow(object):
    def setupUi(self, NewQueryWindow):
        NewQueryWindow.setObjectName("NewQueryWindow")
        NewQueryWindow.resize(389, 407)
        self.pteBeschreibung = QtGui.QPlainTextEdit(NewQueryWindow)
        self.pteBeschreibung.setGeometry(QtCore.QRect(20, 253, 351, 91))
        self.pteBeschreibung.setObjectName("pteBeschreibung")
        self.lbBeschreibung = QtGui.QLabel(NewQueryWindow)
        self.lbBeschreibung.setGeometry(QtCore.QRect(20, 230, 351, 17))
        self.lbBeschreibung.setObjectName("lbBeschreibung")
        self.pbAbbrechen = QtGui.QPushButton(NewQueryWindow)
        self.pbAbbrechen.setGeometry(QtCore.QRect(20, 360, 88, 27))
        self.pbAbbrechen.setObjectName("pbAbbrechen")
        self.pbSpeichern = QtGui.QPushButton(NewQueryWindow)
        self.pbSpeichern.setGeometry(QtCore.QRect(290, 360, 85, 27))
        self.pbSpeichern.setDefault(True)
        self.pbSpeichern.setObjectName("pbSpeichern")
        self.cbSo = QtGui.QCheckBox(NewQueryWindow)
        self.cbSo.setGeometry(QtCore.QRect(328, 180, 45, 22))
        self.cbSo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbSo.setObjectName("cbSo")
        self.cbSa = QtGui.QCheckBox(NewQueryWindow)
        self.cbSa.setGeometry(QtCore.QRect(278, 180, 44, 22))
        self.cbSa.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbSa.setObjectName("cbSa")
        self.cbMi = QtGui.QCheckBox(NewQueryWindow)
        self.cbMi.setGeometry(QtCore.QRect(127, 180, 44, 22))
        self.cbMi.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbMi.setObjectName("cbMi")
        self.cbDi = QtGui.QCheckBox(NewQueryWindow)
        self.cbDi.setGeometry(QtCore.QRect(79, 180, 42, 22))
        self.cbDi.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbDi.setObjectName("cbDi")
        self.cbMo = QtGui.QCheckBox(NewQueryWindow)
        self.cbMo.setGeometry(QtCore.QRect(24, 180, 49, 22))
        self.cbMo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbMo.setObjectName("cbMo")
        self.cbDo = QtGui.QCheckBox(NewQueryWindow)
        self.cbDo.setGeometry(QtCore.QRect(177, 180, 47, 22))
        self.cbDo.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbDo.setObjectName("cbDo")
        self.cbFr = QtGui.QCheckBox(NewQueryWindow)
        self.cbFr.setGeometry(QtCore.QRect(230, 180, 42, 22))
        self.cbFr.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cbFr.setObjectName("cbFr")
        self.lbEnde = QtGui.QLabel(NewQueryWindow)
        self.lbEnde.setGeometry(QtCore.QRect(25, 116, 49, 27))
        self.lbEnde.setObjectName("lbEnde")
        self.teEnde = QtGui.QTimeEdit(NewQueryWindow)
        self.teEnde.setGeometry(QtCore.QRect(80, 116, 294, 27))
        self.teEnde.setTime(QtCore.QTime(12, 0, 0))
        self.teEnde.setObjectName("teEnde")
        self.leTitel = QtGui.QLineEdit(NewQueryWindow)
        self.leTitel.setGeometry(QtCore.QRect(80, 17, 294, 27))
        self.leTitel.setObjectName("leTitel")
        self.lbBeginn = QtGui.QLabel(NewQueryWindow)
        self.lbBeginn.setGeometry(QtCore.QRect(25, 83, 49, 27))
        self.lbBeginn.setObjectName("lbBeginn")
        self.lbTitel = QtGui.QLabel(NewQueryWindow)
        self.lbTitel.setGeometry(QtCore.QRect(25, 17, 49, 27))
        self.lbTitel.setObjectName("lbTitel")
        self.lbOrt = QtGui.QLabel(NewQueryWindow)
        self.lbOrt.setGeometry(QtCore.QRect(25, 50, 49, 27))
        self.lbOrt.setObjectName("lbOrt")
        self.leOrt = QtGui.QLineEdit(NewQueryWindow)
        self.leOrt.setGeometry(QtCore.QRect(80, 50, 294, 27))
        self.leOrt.setObjectName("leOrt")
        self.teBeginn = QtGui.QTimeEdit(NewQueryWindow)
        self.teBeginn.setGeometry(QtCore.QRect(80, 83, 294, 27))
        self.teBeginn.setTime(QtCore.QTime(11, 0, 0))
        self.teBeginn.setObjectName("teBeginn")
        self.lbKalendertage = QtGui.QLabel(NewQueryWindow)
        self.lbKalendertage.setGeometry(QtCore.QRect(20, 160, 351, 17))
        self.lbKalendertage.setObjectName("lbKalendertage")

        self.retranslateUi(NewQueryWindow)
        QtCore.QMetaObject.connectSlotsByName(NewQueryWindow)
        NewQueryWindow.setTabOrder(self.leTitel, self.leOrt)
        NewQueryWindow.setTabOrder(self.leOrt, self.teBeginn)
        NewQueryWindow.setTabOrder(self.teBeginn, self.teEnde)
        NewQueryWindow.setTabOrder(self.teEnde, self.cbMo)
        NewQueryWindow.setTabOrder(self.cbMo, self.cbDi)
        NewQueryWindow.setTabOrder(self.cbDi, self.cbMi)
        NewQueryWindow.setTabOrder(self.cbMi, self.cbDo)
        NewQueryWindow.setTabOrder(self.cbDo, self.cbFr)
        NewQueryWindow.setTabOrder(self.cbFr, self.cbSa)
        NewQueryWindow.setTabOrder(self.cbSa, self.cbSo)
        NewQueryWindow.setTabOrder(self.cbSo, self.pteBeschreibung)
        NewQueryWindow.setTabOrder(self.pteBeschreibung, self.pbAbbrechen)
        NewQueryWindow.setTabOrder(self.pbAbbrechen, self.pbSpeichern)

    def retranslateUi(self, NewQueryWindow):
        NewQueryWindow.setWindowTitle(QtGui.QApplication.translate("NewQueryWindow", "Neue Suche", None, QtGui.QApplication.UnicodeUTF8))
        self.lbBeschreibung.setText(QtGui.QApplication.translate("NewQueryWindow", "Beschreibung:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbAbbrechen.setText(QtGui.QApplication.translate("NewQueryWindow", "&Abbrechen", None, QtGui.QApplication.UnicodeUTF8))
        self.pbSpeichern.setText(QtGui.QApplication.translate("NewQueryWindow", "&Speichern", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSo.setText(QtGui.QApplication.translate("NewQueryWindow", "So", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSa.setText(QtGui.QApplication.translate("NewQueryWindow", "Sa", None, QtGui.QApplication.UnicodeUTF8))
        self.cbMi.setText(QtGui.QApplication.translate("NewQueryWindow", "Mi", None, QtGui.QApplication.UnicodeUTF8))
        self.cbDi.setText(QtGui.QApplication.translate("NewQueryWindow", "Di", None, QtGui.QApplication.UnicodeUTF8))
        self.cbMo.setText(QtGui.QApplication.translate("NewQueryWindow", "Mo", None, QtGui.QApplication.UnicodeUTF8))
        self.cbDo.setText(QtGui.QApplication.translate("NewQueryWindow", "Do", None, QtGui.QApplication.UnicodeUTF8))
        self.cbFr.setText(QtGui.QApplication.translate("NewQueryWindow", "Fr", None, QtGui.QApplication.UnicodeUTF8))
        self.lbEnde.setText(QtGui.QApplication.translate("NewQueryWindow", "Ende:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbBeginn.setText(QtGui.QApplication.translate("NewQueryWindow", "Beginn:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbTitel.setText(QtGui.QApplication.translate("NewQueryWindow", "Titel:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbOrt.setText(QtGui.QApplication.translate("NewQueryWindow", "Ort:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbKalendertage.setText(QtGui.QApplication.translate("NewQueryWindow", "Kalendertage:", None, QtGui.QApplication.UnicodeUTF8))

        
class MyNewQueryWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyNewQueryWindow, self).__init__(parent)
        self.ui = Ui_NewQueryWindow()
        self.ui.setupUi(self)
        
        QtCore.QObject.connect(self.ui.pbAbbrechen, QtCore.SIGNAL('clicked()'), self.pbAbbrechenClicked)
        QtCore.QObject.connect(self.ui.pbSpeichern, QtCore.SIGNAL('clicked()'), self.pbSpeichernClicked)
        
    def pbAbbrechenClicked(self):
        self.close()
        
        
    def pbSpeichernClicked(self):
        if len(self.ui.leTitel.text()) <= 0:
            QtGui.QMessageBox.question(self, 'Fehlende Angaben', "Bitte einen Titel angeben!", QtGui.QMessageBox.Ok)
            self.ui.leTitel.setFocus()
            return
        
        if len(self.ui.leOrt.text()) <= 0:
            QtGui.QMessageBox.question(self, 'Fehlende Angaben', "Bitte einen Ort angeben!", QtGui.QMessageBox.Ok)
            self.ui.leOrt.setFocus()
            return
        
        if len(self.ui.pteBeschreibung.toPlainText()) <= 0:
            QtGui.QMessageBox.question(self, 'Fehlende Angaben', "Bitte eine Beschreibung angeben!", QtGui.QMessageBox.Ok)
            self.ui.pteBeschreibung.setFocus()
            return
        
        self.newFromHour = self.ui.teBeginn.time().hour()
        self.newFromMinute = self.ui.teBeginn.time().minute()
        self.newUntilHour = self.ui.teEnde.time().hour()
        self.newUntilMinute = self.ui.teEnde.time().minute()
        
        self.newWeekdays = []
        
        if self.ui.cbMo.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[0])
        if self.ui.cbDi.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[1])
        if self.ui.cbMi.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[2])
        if self.ui.cbDo.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[3])
        if self.ui.cbFr.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[4])
        if self.ui.cbSa.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[5])
        if self.ui.cbSo.isChecked():
            self.newWeekdays.append(QueryTime.WEEKDAYS[6])
        
        ''' def __init__(self, from_hour, from_minute, until_hour, until_minute, weekdays): '''
        try:
            self.newQueryTime = QueryTime(self.newFromHour, self.newFromMinute, self.newUntilHour, self.newUntilMinute, self.newWeekdays)
        except ValueError:
            QtGui.QMessageBox.question(self, 'Fehlende Angaben', "Bitte mindestens einen Kalendertag angeben!", QtGui.QMessageBox.Ok)
            return
        
        self.newTitle = self.ui.leTitel.text()
        self.newPlace = self.ui.leOrt.text()
        self.newDescription = self.ui.pteBeschreibung.toPlainText()
        ''' def __init__(self, title, place, query_time, description, id_=None): '''
        self.newQuery = Query(self.newTitle, self.newPlace, self.newQueryTime, self.newDescription)
        
        
        
        ''' Todo: Query an Brain schicken '''
        self.parent().brain.createNewQueryEntry(self.newQuery)
        
        self.close()
