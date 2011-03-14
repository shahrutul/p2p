# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(568, 539)
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
        self.buttonFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QtGui.QFrame.Raised)
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
        self.lbDetails = QtGui.QLabel(self.centralwidget)
        self.lbDetails.setObjectName("lbDetails")
        self.verticalLayout.addWidget(self.lbDetails)
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
        self.twSuche.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Ort", None, QtGui.QApplication.UnicodeUTF8))
        self.twSuche.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Beschreibung", None, QtGui.QApplication.UnicodeUTF8))
        self.pbNeu.setText(QtGui.QApplication.translate("MainWindow", "Neu", None, QtGui.QApplication.UnicodeUTF8))
        self.pbBearbeiten.setText(QtGui.QApplication.translate("MainWindow", "Bearbeiten", None, QtGui.QApplication.UnicodeUTF8))
        self.pbEntfernen.setText(QtGui.QApplication.translate("MainWindow", "Entfernen", None, QtGui.QApplication.UnicodeUTF8))
        self.lbDetails.setText(QtGui.QApplication.translate("MainWindow", "Details:", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Titel", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Ort", None, QtGui.QApplication.UnicodeUTF8))
        self.twDetails.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Beschreibung", None, QtGui.QApplication.UnicodeUTF8))
        self.twLog.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))
        
        
        
class MyMainWindow(QtGui.QMainWindow):
    def pbNeuClick(self):
        self.log("Neu wurde angeklickt!")
        self.addDummySearch()
    
    def pbBearbeitenClick(self):
        self.log("Bearbeiten wurde angeklickt!")
        item = self.ui.twSuche.currentItem()
        if not item:
            self.log("Kein Item ausgewaehlt!")
            return
        index = self.ui.twSuche.indexOfTopLevelItem(item)
        print index
        
    def pbEntfernen(self):
        self.log("Entfernen wurde angeklickt!")
    
    def twSucheItemClicked(self, item = None, columnIndex = None): 
        self.log("Suchefeld angeklickt.")
        if columnIndex != None:
            print item
            print columnIndex
    
    ''' ... '''
    
    def addDummySearch(self):
        newItem = QtGui.QTreeWidgetItem(self.ui.twSuche)
        newItem.setText(0, "a")
        newItem.setText(1, "b")
        newItem.setText(2, "c")
        self.ui.twLog.addTopLevelItem(newItem)


        
    def clearLog(self):
        self.ui.twLog.clear()
        print "Hello World"
        
        
    def log(self, inString):
        newItem = QtGui.QTreeWidgetItem(self.ui.twLog)
        newItem.setText(0, inString)
        self.ui.twLog.addTopLevelItem(newItem)
        
    
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        ' Signals '
        QtCore.QObject.connect(self.ui.pbNeu, QtCore.SIGNAL('clicked()'), self.pbNeuClick)
        QtCore.QObject.connect(self.ui.pbBearbeiten, QtCore.SIGNAL('clicked()'), self.pbBearbeitenClick)
        QtCore.QObject.connect(self.ui.pbEntfernen, QtCore.SIGNAL('clicked()'), self.pbEntfernen)
        QtCore.QObject.connect(self.ui.twSuche, QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'), self.twSucheItemClicked)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyMainWindow()
    myapp.show()
    sys.exit(app.exec_())
    
'''
        msgBox = QtGui.QMessageBox.question(self, 'Ueberschrift', "Die Nachricht ....", QtGui.QMessageBox.Ok)

'''