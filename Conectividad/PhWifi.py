'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''
import FreeCADGui as Gui
from Ventanas import *

class Ph_Wifi():
    def GetResources(self):
        return {"MenuText": "WIFI",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Iniciar dispositivo por WIFI",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        self.ex = Example()

Gui.addCommand('WIFI_Tool', Ph_Wifi())