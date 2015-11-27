'''
Created on 5/11/2015

@author: dpalominop
'''

from PySide import QtCore

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
import math

from Socket.PhCliente import *
#from Calibracion.PhGiroscopo import *

class PhControlOrientacionTraslacion(QtCore.QObject):
    """Iniciar y detener envio de datos por WIFI"""
    
    start = True
    def GetResources(self):
        return {"MenuText": "&CONTROL COMPLETO",
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
        App.getDocument("PhGyroscope").getObject("Box").Width = '20 mm'
        App.getDocument("PhGyroscope").getObject("Box").Length = '20 mm'
        App.getDocument("PhGyroscope").getObject("Box").Height = '20 mm'
        Draft.makeLine(App.Vector(10,10,10),App.Vector(10,10,50))
        Draft.makeLine(App.Vector(10,10,10),App.Vector(10,50,10))
        Draft.makeLine(App.Vector(10,10,10),App.Vector(50,10,10))
        #App.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewAxometric()
        
        
        self.timer = QtCore.QTimer()
        self.socket = PhCliente()
        self.timer.timeout.connect(self.controlGiro)
        self.timer.start(100)
        
    def detenerProceso(self):
        self.timer.disconnect()
        self.timer.stop()
        self.timer.killTimer()
    
    def controlGiro(self):
        rmsg = self.socket.sendCommand(1, 7, "CUCHAROS")
        
        if rmsg["rsucces"]:
            #yaw,pitch,roll = rmsg["rdata"]
            q0, q1, q2, q3 = rmsg["rdata"]
            yaw,pitch,roll = self.quat2Euler(q0, q1, q2, q3)
            
            App.getDocument("PhGyroscope").Box.Placement=App.Placement(App.Vector(0,0,0), 
                                                                         App.Rotation(yaw, pitch, roll),
                                                                         App.Vector(10,10,10))
            #App.ActiveDocument.recompute()
            App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
            
    def quat2Euler(self, q0, q1, q2, q3):
        
        R11 = 2.0 * q0 * q0 - 1.0 + 2.0 * q1 * q1
        R21 = 2.0 * (q1 * q2 + q0 * q3)
        R31 = 2.0 * (q1 * q3 - q0 * q2)
        R32 = 2.0 * (q2 * q3 + q0 * q1)
        R33 = 2.0 * q0 * q0 - 1.0 + 2.0 * q3 * q3
    
        yaw = math.atan2(R32, R33)
        pitch = -math.atan(R31 * ((1 - R31 * R31)**-1/2))
        roll = math.atan2(R21, R11)
        
        return (yaw, pitch, roll)
        
Gui.addCommand('GYROSCOPE_ACCELEROMETER', PhControlOrientacionTraslacion())


if __name__ == '__main__':
    pass
