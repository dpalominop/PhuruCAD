'''
Created on 27/8/2015

@author: dpalominop
'''

from PySide import QtCore

import FreeCADGui as Gui
import FreeCAD as App
import Part

from Socket.PhCliente import *

class PhWifiEjecucion(QtCore.QObject):
    """Iniciar y detener envio de datos por WIFI"""
    
    start = True
    def GetResources(self):
        return {"MenuText": "&PLAY/STOP",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Iniciar y detener envio de datos por WIFI",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        if self.start:
            self.iniciarProceso()
            self.start = False
        else:
            self.detenerProceso()
            self.start = True
        
        
    @QtCore.Slot()
    def iniciarProceso(self):
        self.doc = App.activeDocument()
        if self.doc == None:
            self.doc = App.newDocument("PHURU")

        self.l = Part.Line()
        self.l.StartPoint = App.Vector(0.0,0.0,0.0)
        
        
        self.timer = QtCore.QTimer()
        self.socket = PhCliente()
        self.timer.timeout.connect(self.dibujarPunto)
        self.timer.start(100)
        
    def detenerProceso(self):
        self.timer.disconnect()
        self.timer.stop()
        self.timer.killTimer()
    
    def dibujarPunto(self):
        rmsg = self.socket.sendCommand(1, 4, "CUCHAROS")
        
        if rmsg["rsucces"]:
            x,y,z,d = rmsg["rdata"]
            self.l.EndPoint = self.l.EndPoint.add(App.Vector(float(x),float(y),float(z)))
            
            self.doc.addObject("Part::Feature","Line").Shape = self.l.toShape() 
            self.doc.recompute()
            self.l.StartPoint = self.l.EndPoint.add(App.Vector(0.0,0.0,0.0))
        
Gui.addCommand('WIFI_EXEC', PhWifiEjecucion())


if __name__ == '__main__':
    pass