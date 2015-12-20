# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhWCalibracionAcelerometro.ui'
#
# Created: Sat Dec 19 19:02:58 2015
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
        self.resize(290, 408)
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 111, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(158, 20, 111, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtGui.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 120, 111, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtGui.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(158, 120, 111, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtGui.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 220, 111, 51))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtGui.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(160, 220, 111, 51))
        self.pushButton_6.setObjectName("pushButton_6")
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 80, 111, 29))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 80, 111, 29))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtGui.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 180, 111, 29))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtGui.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 180, 111, 29))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtGui.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(20, 280, 111, 29))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtGui.QLineEdit(self)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 280, 111, 29))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtGui.QLineEdit(self)
        self.lineEdit_7.setGeometry(QtCore.QRect(90, 360, 113, 29))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(20, 320, 251, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 340, 111, 17))
        self.label.setObjectName("label")

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("Form", "CALIBRAR MAGNETÓMETRO", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "X-", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "X+", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Form", "Y-", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Form", "Y+", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("Form", "Z-", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("Form", "Z+", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "PROMEDIO TOTAL:", None, QtGui.QApplication.UnicodeUTF8))

