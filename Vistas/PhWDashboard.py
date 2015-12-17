# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWDashboard.ui'
#
# Created: Wed Dec 16 18:52:19 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PhWDashboard(QtGui.QWidget):
    windowFinished = QtCore.Signal()
    
    def __init__(self):
        super(PhWDashboard, self).__init__()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(262, 177)
        self.Iniciar = QtGui.QPushButton(self)
        self.Iniciar.setGeometry(QtCore.QRect(10, 30, 111, 51))
        self.Iniciar.setObjectName("Iniciar")
        self.Pausar = QtGui.QPushButton(self)
        self.Pausar.setGeometry(QtCore.QRect(140, 30, 111, 51))
        self.Pausar.setObjectName("Parar")
        self.Salir = QtGui.QPushButton(self)
        self.Salir.setGeometry(QtCore.QRect(138, 110, 111, 51))
        self.Salir.setObjectName("Salir")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(self)
        QtCore.QObject.connect(self.Salir, QtCore.SIGNAL("pressed()"), self.cancelar)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("Form", "DASHBOARD", None, QtGui.QApplication.UnicodeUTF8))
        self.Iniciar.setText(QtGui.QApplication.translate("Form", "INICIAR", None, QtGui.QApplication.UnicodeUTF8))
        self.Pausar.setText(QtGui.QApplication.translate("Form", "PAUSAR", None, QtGui.QApplication.UnicodeUTF8))
        self.Salir.setText(QtGui.QApplication.translate("Form", "SALIR", None, QtGui.QApplication.UnicodeUTF8))
        
    def cancelar(self):
        self.close()
        self.windowFinished.emit()
    
    def aceptar(self):
        self.close()
        self.windowFinished.emit()

