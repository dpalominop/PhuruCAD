# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWControlOrientacion.ui'
#
# Created: Sun Nov 29 18:16:40 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PhWControlOrientacion(QtGui.QWidget):
    windowFinished = QtCore.Signal()
    
    def __init__(self):
        super(PhWControlOrientacion, self).__init__()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        self.setObjectName("widget")
        self.resize(332, 139)
        self.Iniciar = QtGui.QPushButton(self)
        self.Iniciar.setGeometry(QtCore.QRect(10, 30, 151, 41))
        self.Iniciar.setObjectName("Iniciar")
        self.Pausar = QtGui.QPushButton(self)
        self.Pausar.setGeometry(QtCore.QRect(170, 30, 151, 41))
        self.Pausar.setObjectName("Pausar")
        self.Salir = QtGui.QPushButton(self)
        self.Salir.setGeometry(QtCore.QRect(200, 90, 101, 31))
        self.Salir.setObjectName("Salir")
        self.Translacion = QtGui.QCheckBox(self)
        self.Translacion.setGeometry(QtCore.QRect(10, 100, 151, 22))
        self.Translacion.setObjectName("Translacion")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(self)
        QtCore.QObject.connect(self.Salir, QtCore.SIGNAL("pressed()"), self.cancelar)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("widget", "Control de Orientación", None, QtGui.QApplication.UnicodeUTF8))
        self.Iniciar.setText(QtGui.QApplication.translate("widget", "INICIAR", None, QtGui.QApplication.UnicodeUTF8))
        self.Pausar.setText(QtGui.QApplication.translate("widget", "PAUSAR", None, QtGui.QApplication.UnicodeUTF8))
        self.Salir.setText(QtGui.QApplication.translate("widget", "SALIR", None, QtGui.QApplication.UnicodeUTF8))
        self.Translacion.setText(QtGui.QApplication.translate("widget", "Habilitar Translación", None, QtGui.QApplication.UnicodeUTF8))

    def cancelar(self):
        self.close()
        self.windowFinished.emit()
    
    def aceptar(self):
        self.close()
        self.windowFinished.emit()