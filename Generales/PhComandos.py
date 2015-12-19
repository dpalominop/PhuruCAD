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
        #self.wComandos.Pausar.setEnabled(False)
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
        
        QtCore.QObject.connect(self.wComandos.Quaterniobn, 
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
        

    @QtCore.Slot()
    def doReset(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 1, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doVersion(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 2, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doACK(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 3, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doError(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 12, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doLeerSensores(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 5, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doLeerEuler(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 7, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doQuaternion(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 6, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doLeerPosicion(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 11, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doLeerVelocidad(self):
        self.socket = PhCliente()
        rmsg = self.socket.sendCommand(1, 4, "")
        self.wComandos.Respuesta.document().setPlainText(str(rmsg))
        self.socket.deleteLater()
    
    @QtCore.Slot()
    def doCalMag(self):
        pass
    
    @QtCore.Slot()
    def doCalAcel(self):
        pass
    
    @QtCore.Slot()
    def doCalGiros(self):
        pass

        
Gui.addCommand('COMANDOS', PhComandos())

if __name__ == '__main__':
    pass   