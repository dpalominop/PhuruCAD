'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''
import FreeCADGui as Gui
#from mi_ventana import Principal
from Socket.PhThread import *
from PyQt4.QtCore import QThread

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
        #self.ex = Example()
        #self.principal = Principal()
        #from Socket.PhCliente import *
        
        self.proceso()
        
    def proceso(self):
        
        myThread = QThread()
        
        myThread.start()
        

Gui.addCommand('WIFI_Tool', Ph_Wifi())