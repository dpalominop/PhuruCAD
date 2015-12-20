# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWCalibracionAcelerometro.ui'
#
# Created: Sat Dec 19 22:27:50 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PhWCalibracionAcelerometro(QtGui.QWidget):
    windowFinished = QtCore.Signal()
    
    def __init__(self):
        super(PhWCalibracionAcelerometro, self).__init__()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(271, 477)
        self.X_MENOS = QtGui.QPushButton(self)
        self.X_MENOS.setGeometry(QtCore.QRect(10, 20, 111, 51))
        self.X_MENOS.setObjectName("X_MENOS")
        self.X_MAS = QtGui.QPushButton(self)
        self.X_MAS.setGeometry(QtCore.QRect(148, 20, 111, 51))
        self.X_MAS.setObjectName("X_MAS")
        self.Y_MENOS = QtGui.QPushButton(self)
        self.Y_MENOS.setGeometry(QtCore.QRect(10, 120, 111, 51))
        self.Y_MENOS.setObjectName("Y_MENOS")
        self.Y_MAS = QtGui.QPushButton(self)
        self.Y_MAS.setGeometry(QtCore.QRect(148, 120, 111, 51))
        self.Y_MAS.setObjectName("Y_MAS")
        self.Z_MENOS = QtGui.QPushButton(self)
        self.Z_MENOS.setGeometry(QtCore.QRect(10, 220, 111, 51))
        self.Z_MENOS.setObjectName("Z_MENOS")
        self.Z_MAS = QtGui.QPushButton(self)
        self.Z_MAS.setGeometry(QtCore.QRect(150, 220, 111, 51))
        self.Z_MAS.setObjectName("Z_MAS")
        self.PROM_X_MENOS = QtGui.QLineEdit(self)
        self.PROM_X_MENOS.setGeometry(QtCore.QRect(10, 80, 111, 29))
        self.PROM_X_MENOS.setObjectName("PROM_X_MENOS")
        self.PROM_X_MAS = QtGui.QLineEdit(self)
        self.PROM_X_MAS.setGeometry(QtCore.QRect(150, 80, 111, 29))
        self.PROM_X_MAS.setObjectName("PROM_X_MAS")
        self.PROM_Y_MENOS = QtGui.QLineEdit(self)
        self.PROM_Y_MENOS.setGeometry(QtCore.QRect(10, 180, 111, 29))
        self.PROM_Y_MENOS.setObjectName("PROM_Y_MENOS")
        self.PROM_Y_MAS = QtGui.QLineEdit(self)
        self.PROM_Y_MAS.setGeometry(QtCore.QRect(150, 180, 111, 29))
        self.PROM_Y_MAS.setObjectName("PROM_Y_MAS")
        self.PROM_Z_MENOS = QtGui.QLineEdit(self)
        self.PROM_Z_MENOS.setGeometry(QtCore.QRect(10, 280, 111, 29))
        self.PROM_Z_MENOS.setObjectName("PROM_Z_MENOS")
        self.PROM_Z_MAS = QtGui.QLineEdit(self)
        self.PROM_Z_MAS.setGeometry(QtCore.QRect(150, 280, 111, 29))
        self.PROM_Z_MAS.setObjectName("PROM_Z_MAS")
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(10, 320, 251, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.ENVIAR = QtGui.QPushButton(self)
        self.ENVIAR.setGeometry(QtCore.QRect(60, 350, 147, 41))
        self.ENVIAR.setObjectName("ENVIAR")
        self.SALIR = QtGui.QPushButton(self)
        self.SALIR.setGeometry(QtCore.QRect(154, 420, 111, 41))
        self.SALIR.setObjectName("SALIR")
        self.INICIAR = QtGui.QPushButton(self)
        self.INICIAR.setGeometry(QtCore.QRect(10, 420, 111, 41))
        self.INICIAR.setObjectName("INICIAR")
        self.line_2 = QtGui.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(10, 400, 251, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(Form)
        QtCore.QObject.connect(self.SALIR, QtCore.SIGNAL("pressed()"), self.salir)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("Form", "CALIBRAR ACELERÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.X_MENOS.setText(QtGui.QApplication.translate("Form", "X-", None, QtGui.QApplication.UnicodeUTF8))
        self.X_MAS.setText(QtGui.QApplication.translate("Form", "X+", None, QtGui.QApplication.UnicodeUTF8))
        self.Y_MENOS.setText(QtGui.QApplication.translate("Form", "Y-", None, QtGui.QApplication.UnicodeUTF8))
        self.Y_MAS.setText(QtGui.QApplication.translate("Form", "Y+", None, QtGui.QApplication.UnicodeUTF8))
        self.Z_MENOS.setText(QtGui.QApplication.translate("Form", "Z-", None, QtGui.QApplication.UnicodeUTF8))
        self.Z_MAS.setText(QtGui.QApplication.translate("Form", "Z+", None, QtGui.QApplication.UnicodeUTF8))
        self.ENVIAR.setText(QtGui.QApplication.translate("Form", "ENVIAR PARÁMETROS", None, QtGui.QApplication.UnicodeUTF8))
        self.SALIR.setText(QtGui.QApplication.translate("Form", "SALIR", None, QtGui.QApplication.UnicodeUTF8))
        self.INICIAR.setText(QtGui.QApplication.translate("Form", "INICIAR", None, QtGui.QApplication.UnicodeUTF8))

    def salir(self):
        self.close()
        self.windowFinished.emit()