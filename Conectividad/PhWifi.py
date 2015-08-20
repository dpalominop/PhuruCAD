'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''
import FreeCADGui as Gui
from mi_ventana import Principal
#from mi_ventana_pyside import Principal
from Socket.PhCliente import *

class Ph_Wifi():
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
                               QtCore.SLOT("do_reconnect()"))
        
        QtCore.QObject.connect(self.socket,
                               QtCore.SIGNAL("connected()"),
                               self.principal,
                               QtCore.SLOT("segundaVentana()"))
        
        self.proceso()
        
    def proceso(self):
        self.socket.sendCommand(1, 1, "CUCHAROS")
        

Gui.addCommand('WIFI_Tool', Ph_Wifi())