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
from Vistas.PhWControlOrientacion import *

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
        self.wControlOrientacion = PhWControlOrientacion()
        self.wControlOrientacion.Pausar.setEnabled(False)
        
        QtCore.QObject.connect(self.wControlOrientacion.Iniciar, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("IniciarProceso()"))
        
        QtCore.QObject.connect(self.wControlOrientacion.Pausar, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("PausarProceso()"))
        
        QtCore.QObject.connect(self.wControlOrientacion, 
                               QtCore.SIGNAL("windowFinished()"), 
                               self, 
                               QtCore.SLOT("DetenerProceso()"))
        self.crearVista()
        
    @QtCore.Slot()
    def IniciarProceso(self):
        App.Console.PrintMessage("Iniciado Proceso ...\n")
        self.wControlOrientacion.Iniciar.setEnabled(False)
        self.wControlOrientacion.Pausar.setEnabled(True)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.controlGiro)
        self.timer.start(100)
        self.socket = PhCliente()
        App.Console.PrintMessage("Proceso Iniciado\n")
       
    @QtCore.Slot() 
    def PausarProceso(self):
        App.Console.PrintMessage("Pausando Proceso ...\n")
        self.wControlOrientacion.Iniciar.setEnabled(True)
        self.wControlOrientacion.Pausar.setEnabled(False)
        self.timer.stop()
        self.timer.disconnect()
        self.timer.deleteLater()
        self.socket.deleteLater()
        App.Console.PrintMessage("Proceso Pausado.\n")
        
    @QtCore.Slot()
    def DetenerProceso(self):
        App.Console.PrintMessage("Finalizando Proceso ...\n")
        self.timer.stop()
        self.timer.disconnect()
        self.timer.deleteLater()
        self.socket.deleteLater()
        App.Console.PrintMessage("Proceso Finalizado.\n")
        
    def crearVista(self):
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
        
        Gui.getDocument("PhGyroscope").getObject("Line").LineColor = (0.00,0.00,1.00)
        Gui.getDocument("PhGyroscope").getObject("Line001").LineColor = (0.00,1.00,0.00)
        Gui.getDocument("PhGyroscope").getObject("Line002").LineColor = (1.00,0.00,0.00)
        Gui.getDocument("PhGyroscope").getObject("Line").PointColor = (0.67,0.67,1.00)
        Gui.getDocument("PhGyroscope").getObject("Line001").PointColor = (0.67,0.67,1.00)
        Gui.getDocument("PhGyroscope").getObject("Line002").PointColor = (0.67,0.67,1.00)
        
    def controlGiro(self):
        rmsg = self.socket.sendCommand(1, 6, "CUCHAROS")
        App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        if rmsg["rsucces"]:
            #yaw,pitch,roll = rmsg["rdata"]
            q0, q1, q2, q3 = rmsg["rdata"]
            yaw,pitch,roll = self.quat2Euler(q0, q1, q2, q3)
            
            App.getDocument("PhGyroscope").Box.Placement=App.Placement(App.Vector(0,0,0), 
                                                                         App.Rotation(yaw, pitch, roll),
                                                                         App.Vector(10,10,10))
            #App.ActiveDocument.recompute()
            App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        else:
            App.Console.PrintMessage("rerror: " + str(rmsg["rerror"]) + "\n")
            
    def quat2Euler(self, q0, q1, q2, q3):
        
        R11 = 2.0 * q0 * q0 - 1.0 + 2.0 * q1 * q1
        R21 = 2.0 * (q1 * q2 + q0 * q3)
        R31 = 2.0 * (q1 * q3 - q0 * q2)
        R32 = 2.0 * (q2 * q3 + q0 * q1)
        R33 = 2.0 * q0 * q0 - 1.0 + 2.0 * q3 * q3
    
        yaw = math.atan2(R32, R33)*180/math.pi
        pitch = -math.atan(R31 * ((1 - R31 * R31)**-1/2))*180/math.pi
        roll = math.atan2(R21, R11)*180/math.pi
        
        return (yaw, pitch, roll)
        
Gui.addCommand('CONTROL_ORIENTACION', PhControlOrientacion())


if __name__ == '__main__':
    pass
