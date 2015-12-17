'''
Created on 16/12/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''
import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
import math

from PySide import QtCore
from Vistas.PhWDashboard import *
from Socket.PhCliente import *

class PhDashboard(QtCore.QObject):
    
    def GetResources(self):
        return {"MenuText": "&DASHBOARD",
                       "Accel": "Ctrl+N",
                       "ToolTip": "llll",
                       "Pixmap"  : ""
        }
        
    def IsActive(self):
        return True
    
    def Activated(self):
        self.wDashboard = PhWDashboard()
        self.wDashboard.Pausar.setEnabled(False)
        QtCore.QObject.connect(self.wDashboard.Iniciar, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("IniciarProceso()"))
        
        QtCore.QObject.connect(self.wDashboard.Pausar, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("PausarProceso()"))
        
        QtCore.QObject.connect(self.wDashboard, 
                               QtCore.SIGNAL("windowFinished()"), 
                               self, 
                               QtCore.SLOT("DetenerProceso()"))
        self.crearVista()
        
    def crearVista(self):
        self.Document = App.newDocument("PhDashboard")
        self.GuiDocument = Gui.getDocument(self.Document.Name)
        App.ActiveDocument = self.Document
        Gui.ActiveDocument = self.GuiDocument
        
        #Sistema de referencia general
        Draft.makeLine(App.Vector(0,0,0),App.Vector(10,0,0))
        Draft.makeLine(App.Vector(0,0,0),App.Vector(0,10,0))
        Draft.makeLine(App.Vector(0,0,0),App.Vector(0,0,10))
        
        
        #App.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")
        self.GuiDocument.activeView().viewAxometric()
        
        #Coloreado de sistema de referencia general
        self.GuiDocument.getObject("Line").LineColor = (1.00,0.00,0.00)
        self.GuiDocument.getObject("Line001").LineColor = (0.00,1.00,0.00)
        self.GuiDocument.getObject("Line002").LineColor = (0.00,0.00,1.00)
        self.GuiDocument.getObject("Line").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line001").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line002").PointColor = (0.67,0.67,1.00)
    
    @QtCore.Slot()
    def IniciarProceso(self):
        App.Console.PrintMessage("Iniciado Proceso ...\n")
        self.wDashboard.Iniciar.setEnabled(False)
        self.wDashboard.Pausar.setEnabled(True)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.actualizarVista())
        self.timer.start(100)
        self.socket = PhCliente()
        App.Console.PrintMessage("Proceso Iniciado\n")
       
    @QtCore.Slot() 
    def PausarProceso(self):
        App.Console.PrintMessage("Pausando Proceso ...\n")
        self.wDashboard.Iniciar.setEnabled(True)
        self.wDashboard.Pausar.setEnabled(False)
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
        
    def actualizarVista(self):
        rmsg = self.socket.sendCommand(1, 4, "")
        #App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        
        if rmsg["rsucces"]:
            #yaw,pitch,roll = rmsg["rdata"]
            boton, x, y, z, time = rmsg["rdata"]
            
            App.ActiveDocument = self.Document
            Draft.makePoint(x,y,z)
            #self.Document.recompute()
            
            App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        else:
            App.Console.PrintMessage("rerror: " + str(rmsg["rerror"]) + "\n")
        
Gui.addCommand('DASHBOARD', PhDashboard())

if __name__ == '__main__':
    pass