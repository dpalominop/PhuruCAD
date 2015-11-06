'''
Created on 5/11/2015

@author: dpalominop
'''

from PySide import QtCore

import FreeCADGui as Gui
import FreeCAD as App
import Part

from Socket.PhCliente import *
#from Calibracion.PhGiroscopo import *

class PhControlOrientacion(QtCore.QObject):
    """Iniciar y detener envio de datos por WIFI"""
    
    start = True
    def GetResources(self):
        return {"MenuText": "&CONTROL SOLO ORIENTACION",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Verificar solo la orientacion del giro del dispositivo",
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
            self.doc = App.newDocument("PhGyroscope")
        
        App.ActiveDocument.addObject("Part::Box","Box")
        App.ActiveDocument.ActiveObject.Label = "Box"
        App.getDocument("PhGyroscope").getObject("Box").Width = '40 mm'
        App.getDocument("PhGyroscope").getObject("Box").Length = '20 mm'
        App.getDocument("PhGyroscope").getObject("Box").Height = '10 mm'
        App.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewAxometric()
        
        
        self.timer = QtCore.QTimer()
        self.socket = PhCliente()
        self.timer.timeout.connect(self.controlGiro)
        #self.timer.start(1000)
        
    def detenerProceso(self):
        self.timer.disconnect()
        self.timer.stop()
        self.timer.killTimer()
    
    def controlGiro(self):
        rmsg = self.socket.sendCommand(1, 4, "CUCHAROS")
        
        if rmsg["rsucces"]:
            yaw,pitch,roll,time = rmsg["rdata"]
            
            App.getDocument("PhGyroscope").Box.Placement=App.Placement(App.Vector(0,0,0), 
                                                                         App.Rotation(yaw, pitch, roll), 
                                                                         App.Vector(0,0,0))
            #App.ActiveDocument.recompute()
            App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        
Gui.addCommand('GYROSCOPE_1', PhControlOrientacion())


if __name__ == '__main__':
    pass