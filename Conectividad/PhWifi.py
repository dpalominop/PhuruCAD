'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''
import FreeCADGui as Gui
import FreeCAD as App
import Part
from mi_ventana import Principal
#from mi_ventana_pyside import Principal
from Socket.PhCliente import *


class Ph_Wifi(QtCore.QObject):
    "Iniciar dispositivo por WIFI"
    timer = QtCore.QTimer()
    
    def GetResources(self):
        return {"MenuText": "&WIFI",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Iniciar dispositivo por WIFI",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        #app = QtCore.QCoreApplication(sys.argv)
        self.socket = PhCliente()
        self.principal = Principal()
        
        QtCore.QObject.connect(self.principal.PrimerSiguiente, 
                               QtCore.SIGNAL("pressed()"), 
                               self.socket, 
                               QtCore.SLOT("on_checkHardware()"))
        
        QtCore.QObject.connect(self.socket,
                               QtCore.SIGNAL("hwCheckedOk()"),
                               self.principal,
                               QtCore.SLOT("segundaVentana()"))
        
        QtCore.QObject.connect(self.principal,
                               QtCore.SIGNAL("windowFinished()"),
                               self,
                               QtCore.SLOT("iniciarProceso()")
                               )
        #self.principal.connect(QtCore.SIGNAL("windowFinished()"), QtCore.SLOT("iniciarProceso()"))
        
    @QtCore.Slot()
    def iniciarProceso(self):
        self.doc = App.activeDocument()
        if self.doc == None:
            self.doc = App.newDocument("PHURU")

        self.l = Part.Line()
        self.l.StartPoint = App.Vector(0.0,0.0,0.0)
        self.timer.timeout.connect(self.dibujarPunto)
        self.timer.start(100)
        
    def detenerProceso(self):
        #self.PuertoSerie.close()
        #self.PuertoSerie = None
        pass
    
    def dibujarPunto(self):
        #if self.PuertoSerie == None:
        #    return
        #else:
        rmsg = self.socket.sendCommand(1, 4, "CUCHAROS")
        
        if rmsg["rsucces"]:
            x,y,z,d = rmsg["rdata"]
            self.l.EndPoint = self.l.EndPoint.add(App.Vector(float(x),float(y),float(z)))
            
            self.doc.addObject("Part::Feature","Line").Shape = self.l.toShape() 
            self.doc.recompute()
            self.l.StartPoint = self.l.EndPoint.add(App.Vector(0.0,0.0,0.0))
        

Gui.addCommand('WIFI_Tool', Ph_Wifi())