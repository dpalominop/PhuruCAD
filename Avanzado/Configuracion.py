'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''

import FreeCADGui as Gui
from Ventanas import *

class Ph_Configuracion(object):
    '''
    classdocs
    '''
        
    def GetResources(self):
        return {"MenuText": "Configuracion",
                       "Accel": "Ctrl+O",
                       "ToolTip": "Configuraciones Avanzadas",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        self.ex = Example()
    
    
        
Gui.addCommand('Configuracion', Ph_Configuracion())