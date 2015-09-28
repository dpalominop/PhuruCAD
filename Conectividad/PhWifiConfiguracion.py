'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''
from PySide import QtCore

import FreeCADGui as Gui
import FreeCAD as App
import Part

from Vistas.PhWConfiguracion import *
from Socket.PhCliente import *

class PhWifiConfiguracion(QtCore.QObject):
    """Configurar dispositivo por WIFI"""
    
    
    def GetResources(self):
        return {"MenuText": "&WIFI",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Configurar dispositivo por WIFI",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        
        #app = QtCore.QCoreApplication(sys.argv)
        self.timer = QtCore.QTimer()
        self.socket = PhCliente()
        self.wConfiguracion = PhWConfiguracion()
        
        QtCore.QObject.connect(self.wConfiguracion.PrimerSiguiente, 
                               QtCore.SIGNAL("pressed()"), 
                               self.socket, 
                               QtCore.SLOT("on_checkHardware()"))
        
        QtCore.QObject.connect(self.socket,
                               QtCore.SIGNAL("hwCheckedOk()"),
                               self.wConfiguracion,
                               QtCore.SLOT("segundaVentana()"))
        
        QtCore.QObject.connect(self.wConfiguracion,
                               QtCore.SIGNAL("windowFinished()"),
                               self,
                               QtCore.SLOT("iniciarProceso()")
                               )
        #self.wConfiguracion.connect(QtCore.SIGNAL("windowFinished()"), QtCore.SLOT("iniciarProceso()"))
        
    @QtCore.Slot()
    def iniciarProceso(self):
        self.doc = App.activeDocument()
        if self.doc == None:
            self.doc = App.newDocument("PHURU")

        self.l = Part.Line()
        self.l.StartPoint = App.Vector(0.0,0.0,0.0)
        self.timer.timeout.connect(self.dibujarPunto)
        self.timer.start(3000)
        
    def detenerProceso(self):
        #self.PuertoSerie.close()
        #self.PuertoSerie = None
        pass
    
    def dibujarPunto(self):
        #if self.PuertoSerie == None:
        #    return
        #else:
        rmsg = self.socket.sendCommand(1, 4, "CUCHAROS")
        App.Console.PrintMessage(rmsg)
        
        if rmsg["rsucces"]:
            x,y,z,d = rmsg["rdata"]
            self.l.EndPoint = self.l.EndPoint.add(App.Vector(float(x),float(y),float(z)))
            
            self.doc.addObject("Part::Feature","Line").Shape = self.l.toShape() 
            self.doc.recompute()
            self.l.StartPoint = self.l.EndPoint.add(App.Vector(0.0,0.0,0.0))
        

Gui.addCommand('WIFI_Tool', PhWifiConfiguracion())

if __name__ == '__main__':
    pass