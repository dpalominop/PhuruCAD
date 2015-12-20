'''
Created on 19/12/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.ip
'''

from PySide import QtCore

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
import math

from Socket.PhCliente import *
from Vistas.PhWCalibracionAcelerometro import *

class PhCalibracionAcelerometro(QtCore.QObject):
    """Iniciar y detener envio de datos por WIFI"""
    
    start = True
    def GetResources(self):
        return {"MenuText": "&CALIBRAR ACELEROMETRO",
                       "Accel": "Ctrl+N",
                       "ToolTip": "",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        self.wCalibracionAcelerometro = PhWCalibracionAcelerometro()
        
        
Gui.addCommand('CALIBRACION_ACELEROMETRO', PhCalibracionAcelerometro())


if __name__ == '__main__':
    pass
        
        