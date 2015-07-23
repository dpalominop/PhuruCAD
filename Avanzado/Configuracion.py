'''
Created on 23/7/2015

@author: dpalominop
'''
import FreeCADGui as Gui
class Ph_Configuracion(object):
    '''
    classdocs
    '''
        
    def GetResources(self):
        return {"MenuText": "Configuracion",
                       "Accel": "Ctrl+O",
                       "ToolTip": "Configuraciones Avanzadas",
                       "Pixmap"  : ":icons/tuerca.png"
        }

    def IsActive(self):
        return True

    def Activated(self):
        return True
        
Gui.addCommand('Configuracion', Ph_Configuracion())