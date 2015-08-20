# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana.ui'
#
# Created: Thu Jul 23 19:05:18 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Principal(QtGui.QStackedWidget):
    def __init__(self):
        super(Principal, self).__init__()
        self.setupUi()
        self.show()
    
    def setupUi(self):
        self.setObjectName("Principal")
        self.resize(421, 270)
        self.setMinimumSize(QtCore.QSize(421, 270))
        self.setMaximumSize(QtCore.QSize(421, 270))
        
        self.PrimeraPagina = QtGui.QWidget()
        self.PrimeraPagina.setEnabled(True)
        self.PrimeraPagina.setMinimumSize(QtCore.QSize(421, 270))
        self.PrimeraPagina.setMaximumSize(QtCore.QSize(421, 270))
        self.PrimeraPagina.setObjectName("PrimeraPagina")
        
        self.formLayoutWidget = QtGui.QWidget(self.PrimeraPagina)
        self.formLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 421, 271))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        
        self.PrimerLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.PrimerLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        #self.PrimerLayout.setMargin(0)
        self.PrimerLayout.setContentsMargins(0, 0, 0, 0)
        self.PrimerLayout.setObjectName("PrimerLayout")
        
        self.PrimerTexto = QtGui.QTextBrowser(self.formLayoutWidget)
        self.PrimerTexto.setObjectName("PrimerTexto")
        self.PrimerLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.PrimerTexto)
        
        self.PrimerSiguiente = QtGui.QPushButton(self.formLayoutWidget)
        self.PrimerSiguiente.setObjectName("PrimerSiguiente")
        self.PrimerLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.PrimerSiguiente)
        
        self.PrimerCancelar = QtGui.QPushButton(self.formLayoutWidget)
        self.PrimerCancelar.setObjectName("PrimerCancelar")
        self.PrimerLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.PrimerCancelar)
        self.addWidget(self.PrimeraPagina)
        
        
        self.SegundaPagina = QtGui.QWidget()
        self.SegundaPagina.setEnabled(False)
        self.SegundaPagina.setMinimumSize(QtCore.QSize(421, 270))
        self.SegundaPagina.setMaximumSize(QtCore.QSize(421, 270))
        self.SegundaPagina.setObjectName("SegundaPagina")
        
        self.formLayoutWidget_2 = QtGui.QWidget(self.SegundaPagina)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 421, 271))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        
        self.SegundoLayout = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.SegundoLayout.setContentsMargins(0, 0, 0, 0)
        self.SegundoLayout.setObjectName("SegundoLayout")
        
        self.SegundoTexto = QtGui.QTextBrowser(self.formLayoutWidget_2)
        self.SegundoTexto.setObjectName("SegundoTexto")
        self.SegundoLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.SegundoTexto)
        
        self.PrimerAceptar = QtGui.QPushButton(self.formLayoutWidget_2)
        self.PrimerAceptar.setObjectName("PrimerAceptar")
        self.SegundoLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.PrimerAceptar)
        
        self.Router = QtGui.QPushButton(self.formLayoutWidget_2)
        self.Router.setObjectName("Router")
        self.SegundoLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.Router)
        
        self.addWidget(self.SegundaPagina)

        self.retranslateUi()
       
        #QtCore.QMetaObject.connectSlotsByName(Principal)
        QtCore.QObject.connect(self.PrimerSiguiente, QtCore.SIGNAL("pressed()"), self.segundaVentana)
        QtCore.QObject.connect(self.PrimerCancelar, QtCore.SIGNAL("pressed()"), self.cancelar)
        QtCore.QObject.connect(self.PrimerAceptar, QtCore.SIGNAL("pressed()"), self.aceptar)
        

    def retranslateUi(self):
        self.setWindowTitle(_translate("Principal", "StackedWidget", None))
        self.PrimerTexto.setHtml(_translate("Principal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#55aa7f;\">Se va a iniciar el proceso de configuración de su dispositivo PHURU :D</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/icons/wifi.png\" /></p></body></html>", None))
        self.PrimerSiguiente.setText(_translate("Principal", "Siguiente", None))
        self.PrimerCancelar.setText(_translate("Principal", "Cancelar", None))
        self.SegundoTexto.setHtml(_translate("Principal", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#55aa7f;\">Su dispositio se acaba de conectar :D</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#55aa7f;\">GO GO GO</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; color:#55aa7f;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#55aa7f;\">Si desea conectarse a través de un router externo presiones &quot;Siguiente&quot;, </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#55aa7f;\">de lo contrario presione &quot;Aceptar&quot;</span></p></body></html>", None))
        self.PrimerAceptar.setText(_translate("Principal", "Aceptar", None))
        self.Router.setText(_translate("Principal", "Router", None))
    
    @QtCore.Slot()
    def segundaVentana(self):
        self.PrimeraPagina.setVisible(False)
        self.PrimeraPagina.setEnabled(False)
        
        self.SegundaPagina.setVisible(True)
        self.SegundaPagina.setEnabled(True)
        
        self.PrimerAceptar.setVisible(True)
        self.Router.setVisible(True)
        
    def cancelar(self):
        self.close()
    
    def aceptar(self):
        self.close()

#import Phuru_rc
