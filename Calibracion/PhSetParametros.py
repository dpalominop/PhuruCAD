'''
Created on 12/11/2015

@author: dpalominop
'''

from PySide import QtCore

import FreeCADGui as Gui
import FreeCAD as App
import Part

from Vistas.PhWSetParametros import *
from Socket.PhCliente import *
from Vistas.PhWSetParametros import *

class PhSetParametros(QtCore.QObject):
    """Settear parametros de los sensores"""
    
    def GetResources(self):
        return {"MenuText": "&SET PARAMETROS DE CALIBRACION",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Settear parametros de calibracion del dispositivo.",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        
        #app = QtCore.QCoreApplication(sys.argv)
        self.timer = QtCore.QTimer()
        self.socket = PhCliente()
        
        self.wCalibracion = PhWSetParametros()
        
        QtCore.QObject.connect(self.wCalibracion.SetMagnetometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("M_CAL_MAG()"))
        
        QtCore.QObject.connect(self.wCalibracion.SetAcelerometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("M_CAL_ACC()"))
        
        QtCore.QObject.connect(self.wCalibracion.SetGiroscopo, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("M_CAL_GYR()"))
        
        QtCore.QObject.connect(self.wCalibracion.Salir,
                               QtCore.SIGNAL("pressed()"),
                               self,
                               QtCore.SLOT("exit()"))
        
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
        App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        
        if rmsg["rsucces"]:
            bstate, x,y,z,t = rmsg["rdata"]
            self.l.EndPoint = self.l.EndPoint.add(App.Vector(float(x),float(y),float(z)))
            
            self.doc.addObject("Part::Feature","Line").Shape = self.l.toShape() 
            self.doc.recompute()
            self.l.StartPoint = self.l.EndPoint.add(App.Vector(0.0,0.0,0.0))

    @QtCore.Slot()
    def M_CAL_MAG(self):
        pass
    
    @QtCore.Slot()
    def M_CAL_ACC(self):
        pass
    
    @QtCore.Slot()
    def M_CAL_GYR(self):
        pass
        

Gui.addCommand('SET_PARAMETROS_CALIBRACION', PhSetParametros())

if __name__ == '__main__':
    pass