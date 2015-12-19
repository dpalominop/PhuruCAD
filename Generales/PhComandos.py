'''
Created on 18/12/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
import math

from PySide.QtCore import *
from Vistas.PhWComandos import *
from Socket.PhCliente import *

class PhComandos(QtCore.QObject):
    
    def GetResources(self):
        return {"MenuText": "&COMANDOS",
                       "Accel": "Ctrl+N",
                       "ToolTip": "llll",
                       "Pixmap"  : ""
        }
        
    def IsActive(self):
        return True
    
    def Activated(self):
        self.wComandos = PhWComandos()
        QtCore.QObject.connect(self.wComandos.Reset, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doReset()"))
        
        QtCore.QObject.connect(self.wComandos.Version, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doVersion()"))
        
        QtCore.QObject.connect(self.wComandos.ACK, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doACK()"))
        
        QtCore.QObject.connect(self.wComandos.Error, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doError()"))
        
        QtCore.QObject.connect(self.wComandos.Sensores, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doLeerSensores()"))
        
        QtCore.QObject.connect(self.wComandos.Euler, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doLeerEuler()"))
        
        QtCore.QObject.connect(self.wComandos.Quaternion, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doQuaternion()"))
        
        QtCore.QObject.connect(self.wComandos.Posicion, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doLeerPosicion()"))
        
        QtCore.QObject.connect(self.wComandos.Velocidad, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doLeerVelocidad()"))
        
        QtCore.QObject.connect(self.wComandos.Magnetometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doCalMag()"))
        
        QtCore.QObject.connect(self.wComandos.Acelerometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doCalAcel()"))
        
        QtCore.QObject.connect(self.wComandos.Giroscopo, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doCalGiros()"))
        
        QtCore.QObject.connect(self.wComandos.Extra, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("doExtra()"))

        QtCore.QObject.connect(self.wComandos.Habilitar, 
                               QtCore.SIGNAL("stateChanged()"), 
                               self, 
                               QtCore.SLOT("doHabilitar()"))
        
        #self.wComandos.Extra.setEnabled(False)
        #self.wComandos.Valor.setEnabled(False)
        self.wComandos.Respuesta.setReadOnly(True)
        
    @QtCore.Slot()
    def doReset(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 1, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doVersion(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 2, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doACK(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 3, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doError(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 12, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doLeerSensores(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 5, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doLeerEuler(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 7, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doQuaternion(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 6, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doLeerPosicion(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 11, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doLeerVelocidad(self):
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 4, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doCalMag(self):
        self.activarBotones(False)
        self.activarBotones(True)
        
    @QtCore.Slot()
    def doCalAcel(self):
        self.activarBotones(False)
        self.activarBotones(True)
    
    @QtCore.Slot()
    def doCalGiros(self):
        self.activarBotones(False)
        self.activarBotones(True)
        
    @QtCore.Slot()
    def doExtra(self):
        var = self.wComandos.Valor.text()
        App.Console.PrintMessage(var)
        self.activarBotones(False)
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, int(var), "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
        self.activarBotones(True)
        
    
    @QtCore.Slot(int)
    def doHablitar(self, val):
        if val == 0:
            self.wComandos.Extra.setEnabled(False)
            self.wComandos.Valor.setEnabled(False)
        else:
            self.wComandos.Extra.setEnabled(True)
            self.wComandos.Valor.setEnabled(True)

    def activarBotones(self, val):
        self.wComandos.Reset.setEnabled(val)
        self.wComandos.Version.setEnabled(val)
        self.wComandos.ACK.setEnabled(val)
        self.wComandos.Error.setEnabled(val)
        
        self.wComandos.Sensores.setEnabled(val)
        self.wComandos.Euler.setEnabled(val)
        self.wComandos.Quaternion.setEnabled(val)
        self.wComandos.Posicion.setEnabled(val)
        self.wComandos.Velocidad.setEnabled(val)
        
        self.wComandos.Magnetometro.setEnabled(val)
        self.wComandos.Acelerometro.setEnabled(val)
        self.wComandos.Giroscopo.setEnabled(val)
        
        self.wComandos.Habilitar.setEnabled(val)
        self.wComandos.Extra.setEnabled(val)
        self.wComandos.Valor.setEnabled(val)
        
Gui.addCommand('COMANDOS', PhComandos())

if __name__ == '__main__':
    pass   