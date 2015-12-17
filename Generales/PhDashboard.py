'''
Created on 16/12/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''
import FreeCADGui as Gui
import FreeCAD as App

from PySide import QtCore

class PhDashboard(QtCore.QObject):
    '''
    classdocs
    '''


    def GetResources(self):
        return {"MenuText": "&CONTROL SOLO ORIENTACION",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Verificar solo la orientacion del giro del dispositivo",
                       "Pixmap"  : ""
        }
        
    def IsActive(self):
        return True
        
Gui.addCommand('DASHBOARD', PhDashboard())

if __name__ == '__main__':
    pass