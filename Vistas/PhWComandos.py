# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWComandos.ui'
#
# Created: Fri Dec 18 23:45:24 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class PhWComandos(QtGui.QWidget):
    windowFinished = QtCore.Signal()
    
    def __init__(self):
        super(PhWComandos, self).__init__()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(377, 582)
        self.Reset = QtGui.QPushButton(self)
        self.Reset.setGeometry(QtCore.QRect(40, 40, 141, 27))
        self.Reset.setObjectName("Reset")
        self.Version = QtGui.QPushButton(self)
        self.Version.setGeometry(QtCore.QRect(200, 40, 141, 27))
        self.Version.setObjectName("Version")
        self.ACK = QtGui.QPushButton(self)
        self.ACK.setGeometry(QtCore.QRect(40, 80, 141, 27))
        self.ACK.setObjectName("ACK")
        self.Velocidad = QtGui.QPushButton(self)
        self.Velocidad.setGeometry(QtCore.QRect(200, 260, 141, 27))
        self.Velocidad.setObjectName("Velocidad")
        self.Sensores = QtGui.QPushButton(self)
        self.Sensores.setGeometry(QtCore.QRect(40, 180, 141, 27))
        self.Sensores.setObjectName("Sensores")
        self.Quaterniobn = QtGui.QPushButton(self)
        self.Quaterniobn.setGeometry(QtCore.QRect(200, 220, 141, 27))
        self.Quaterniobn.setObjectName("Quaterniobn")
        self.Euler = QtGui.QPushButton(self)
        self.Euler.setGeometry(QtCore.QRect(40, 220, 141, 27))
        self.Euler.setObjectName("Euler")
        self.Posicion = QtGui.QPushButton(self)
        self.Posicion.setGeometry(QtCore.QRect(40, 260, 141, 27))
        self.Posicion.setObjectName("Posicion")
        self.Respuesta = QtGui.QPlainTextEdit(self)
        self.Respuesta.setGeometry(QtCore.QRect(20, 460, 341, 101))
        self.Respuesta.setObjectName("Respuesta")
        self.Magnetometro = QtGui.QPushButton(self)
        self.Magnetometro.setGeometry(QtCore.QRect(40, 350, 141, 27))
        self.Magnetometro.setObjectName("Magnetometro")
        self.Acelerometro = QtGui.QPushButton(self)
        self.Acelerometro.setGeometry(QtCore.QRect(200, 350, 141, 27))
        self.Acelerometro.setObjectName("Acelerometro")
        self.Giroscopo = QtGui.QPushButton(self)
        self.Giroscopo.setGeometry(QtCore.QRect(40, 390, 141, 27))
        self.Giroscopo.setObjectName("Giroscopo")
        self.Error = QtGui.QPushButton(self)
        self.Error.setGeometry(QtCore.QRect(200, 80, 141, 27))
        self.Error.setObjectName("Error")
        self.linea_02 = QtGui.QFrame(self)
        self.linea_02.setGeometry(QtCore.QRect(30, 300, 311, 16))
        self.linea_02.setFrameShape(QtGui.QFrame.HLine)
        self.linea_02.setFrameShadow(QtGui.QFrame.Sunken)
        self.linea_02.setObjectName("linea_02")
        self.linea_03 = QtGui.QFrame(self)
        self.linea_03.setGeometry(QtCore.QRect(40, 440, 301, 16))
        self.linea_03.setFrameShape(QtGui.QFrame.HLine)
        self.linea_03.setFrameShadow(QtGui.QFrame.Sunken)
        self.linea_03.setObjectName("linea_03")
        self.linea_01 = QtGui.QFrame(self)
        self.linea_01.setGeometry(QtCore.QRect(40, 130, 301, 16))
        self.linea_01.setFrameShape(QtGui.QFrame.HLine)
        self.linea_01.setFrameShadow(QtGui.QFrame.Sunken)
        self.linea_01.setObjectName("linea_01")
        self.Calibracion = QtGui.QLabel(self)
        self.Calibracion.setGeometry(QtCore.QRect(40, 320, 87, 17))
        self.Calibracion.setObjectName("Calibracion")
        self.Control = QtGui.QLabel(self)
        self.Control.setGeometry(QtCore.QRect(40, 10, 62, 17))
        self.Control.setObjectName("Control")
        self.Obtener = QtGui.QLabel(self)
        self.Obtener.setGeometry(QtCore.QRect(40, 150, 60, 17))
        self.Obtener.setObjectName("Obtener")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(Form)
        #QtCore.QObject.connect(self.Salir, QtCore.SIGNAL("pressed()"), self.cancelar)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("Form", "COMANDOS", None, QtGui.QApplication.UnicodeUTF8))
        self.Reset.setText(QtGui.QApplication.translate("Form", "RESET", None, QtGui.QApplication.UnicodeUTF8))
        self.Version.setText(QtGui.QApplication.translate("Form", "VERSIÓN", None, QtGui.QApplication.UnicodeUTF8))
        self.ACK.setText(QtGui.QApplication.translate("Form", "ACK", None, QtGui.QApplication.UnicodeUTF8))
        self.Velocidad.setText(QtGui.QApplication.translate("Form", "VELOCIDAD", None, QtGui.QApplication.UnicodeUTF8))
        self.Sensores.setText(QtGui.QApplication.translate("Form", "LEER SENSORES", None, QtGui.QApplication.UnicodeUTF8))
        self.Quaterniobn.setText(QtGui.QApplication.translate("Form", "QUATERNIÓN", None, QtGui.QApplication.UnicodeUTF8))
        self.Euler.setText(QtGui.QApplication.translate("Form", "ÁNGULOS DE EULER", None, QtGui.QApplication.UnicodeUTF8))
        self.Posicion.setText(QtGui.QApplication.translate("Form", "POSICIÓN", None, QtGui.QApplication.UnicodeUTF8))
        self.Magnetometro.setText(QtGui.QApplication.translate("Form", "MAGNETÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.Acelerometro.setText(QtGui.QApplication.translate("Form", "ACELERÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.Giroscopo.setText(QtGui.QApplication.translate("Form", "GIRÓSCOPO", None, QtGui.QApplication.UnicodeUTF8))
        self.Error.setText(QtGui.QApplication.translate("Form", "ERROR", None, QtGui.QApplication.UnicodeUTF8))
        self.Calibracion.setText(QtGui.QApplication.translate("Form", "CALIBRACIÓN:", None, QtGui.QApplication.UnicodeUTF8))
        self.Control.setText(QtGui.QApplication.translate("Form", "CONTROL:", None, QtGui.QApplication.UnicodeUTF8))
        self.Obtener.setText(QtGui.QApplication.translate("Form", "OBTENER:", None, QtGui.QApplication.UnicodeUTF8))

    def cancelar(self):
        self.close()
        self.windowFinished.emit()
    
    def aceptar(self):
        self.close()
        self.windowFinished.emit()
