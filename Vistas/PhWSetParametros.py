# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWSetParametros.ui'
#
# Created: Thu Nov 12 01:06:40 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PhWSetParametros(QtGui.QWidget):
    def __init__(self):
        super(PhWSetParametros, self).__init__()
        self.setupUi()
        self.show()
    
    def setupUi(self):
        self.setObjectName("Form")
        #Form.setObjectName("Form")
        self.resize(253, 320)
        #Form.resize(253, 320)
        self.SetMagnetometro = QtGui.QPushButton(self)
        self.SetMagnetometro.setGeometry(QtCore.QRect(30, 80, 191, 27))
        self.SetMagnetometro.setObjectName("SetMagnetometro")
        self.SetAcelerometro = QtGui.QPushButton(self)
        self.SetAcelerometro.setGeometry(QtCore.QRect(28, 140, 191, 27))
        self.SetAcelerometro.setObjectName("SetAcelerometro")
        self.SetGiroscopo = QtGui.QPushButton(self)
        self.SetGiroscopo.setGeometry(QtCore.QRect(30, 200, 191, 27))
        self.SetGiroscopo.setObjectName("SetGiroscopo")
        self.Salir = QtGui.QPushButton(self)
        self.Salir.setGeometry(QtCore.QRect(160, 290, 89, 27))
        self.Salir.setObjectName("Salir")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self):
        #Form.setWindowTitle(QtGui.QApplication.translate("Form", "CALIBRAR SENSORES", None, QtGui.QApplication.UnicodeUTF8))
        self.setWindowTitle(QtGui.QApplication.translate("Form", "CALIBRAR SENSORES", None, QtGui.QApplication.UnicodeUTF8))
        self.SetMagnetometro.setText(QtGui.QApplication.translate("Form", "CALIBRAR MAGNETÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.SetAcelerometro.setText(QtGui.QApplication.translate("Form", "CALIBRAR ACELERÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.SetGiroscopo.setText(QtGui.QApplication.translate("Form", "CALIBRAR GIRÓSCOPO", None, QtGui.QApplication.UnicodeUTF8))
        self.Salir.setText(QtGui.QApplication.translate("Form", "SALIR", None, QtGui.QApplication.UnicodeUTF8))

    def cancelar(self):
        self.close()
    
    def aceptar(self):
        self.close()
        self.windowFinished.emit()
