'''
Created on 18/12/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
import math

from PySide.QtCore import *
from Vistas.PhWComandos import *
from Socket.PhCliente import *

class PhComandos(QtCore.QObject):
    
    def GetResources(self):
        return {"MenuText": "&COMANDOS",
                       "Accel": "Ctrl+N",
                       "ToolTip": "llll",
                       "Pixmap"  : ""
        }
        
    def IsActive(self):
        return True
    
    def Activated(self):
        self.wComandos = PhWComandos()
        #self.wComandos.Pausar.setEnabled(False)
        QtCore.QObject.connect(self.wComandos , 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("IniciarProceso()"))
        
        QtCore.QObject.connect(self.wComandos, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("PausarProceso()"))
        
        QtCore.QObject.connect(self.wComandos, 
                               QtCore.SIGNAL("windowFinished()"), 
                               self, 
                               QtCore.SLOT("DetenerProceso()"))

    
    @QtCore.Slot()
    def IniciarProceso(self):
        App.Console.PrintMessage("Iniciado Proceso ...\n")
        #self.wComandos.Iniciar.setEnabled(False)
        #self.wComandos.Pausar.setEnabled(True)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.actualizarVista)
        self.timer.start(100)
        self.socket = PhCliente()
        App.Console.PrintMessage("Proceso Iniciado\n")
       
    @QtCore.Slot() 
    def PausarProceso(self):
        App.Console.PrintMessage("Pausando Proceso ...\n")
        #self.wComandos.Iniciar.setEnabled(True)
        s#elf.wComandos.Pausar.setEnabled(False)
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
        
Gui.addCommand('COMANDOS', PhComandos())

if __name__ == '__main__':
    pass   