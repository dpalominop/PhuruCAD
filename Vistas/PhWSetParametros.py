# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWSetParametros.ui'
#
# Created: Sun Nov 29 17:16:47 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PhWSetParametros(QtGui.QWidget):
    windowFinished = QtCore.Signal()
    
    def __init__(self):
        super(PhWSetParametros, self).__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(317, 309)
        self.SetMagnetometro = QtGui.QPushButton(self)
        self.SetMagnetometro.setGeometry(QtCore.QRect(30, 30, 251, 27))
        self.SetMagnetometro.setObjectName("SetMagnetometro")
        self.SetAcelerometro = QtGui.QPushButton(self)
        self.SetAcelerometro.setGeometry(QtCore.QRect(30, 100, 251, 27))
        self.SetAcelerometro.setObjectName("SetAcelerometro")
        self.SetGiroscopo = QtGui.QPushButton(self)
        self.SetGiroscopo.setGeometry(QtCore.QRect(30, 160, 251, 27))
        self.SetGiroscopo.setObjectName("SetGiroscopo")
        self.Salir = QtGui.QPushButton(self)
        self.Salir.setGeometry(QtCore.QRect(190, 270, 89, 27))
        self.Salir.setObjectName("Salir")
        self.Detener = QtGui.QPushButton(self)
        self.Detener.setGeometry(QtCore.QRect(160, 220, 121, 27))
        self.Detener.setObjectName("Detener")
        self.Iniciar = QtGui.QPushButton(self)
        self.Iniciar.setGeometry(QtCore.QRect(28, 220, 121, 27))
        self.Iniciar.setObjectName("Iniciar")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(Form)
        QtCore.QObject.connect(self.Salir, QtCore.SIGNAL("pressed()"), self.cancelar)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("Form", "CALIBRAR SENSORES", None, QtGui.QApplication.UnicodeUTF8))
        self.SetMagnetometro.setText(QtGui.QApplication.translate("Form", "CALIBRAR MAGNETÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.SetAcelerometro.setText(QtGui.QApplication.translate("Form", "CALIBRAR ACELERÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.SetGiroscopo.setText(QtGui.QApplication.translate("Form", "CALIBRAR GIRÓSCOPO", None, QtGui.QApplication.UnicodeUTF8))
        self.Salir.setText(QtGui.QApplication.translate("Form", "SALIR", None, QtGui.QApplication.UnicodeUTF8))
        self.Detener.setText(QtGui.QApplication.translate("Form", "DETENER", None, QtGui.QApplication.UnicodeUTF8))
        self.Iniciar.setText(QtGui.QApplication.translate("Form", "INICIAR", None, QtGui.QApplication.UnicodeUTF8))

    def cancelar(self):
        self.close()
        self.windowFinished.emit()
    
    def aceptar(self):
        self.close()
        self.windowFinished.emit()