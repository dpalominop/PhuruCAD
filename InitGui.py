# Phuru gui init module
# (c) 2001 Juergen Riegel LGPL

import sys
import os
import random

import FreeCAD,FreeCADGui
#from FreeCAD import Vector
import Part,PartGui

#from PyQt4 import QtGui,QtCore
#import serial

#PuertoSerie = serial.Serial('/dev/ttyUSB0', 9600)
	
#doc = App.newDocument("PHURU")
#l = Part.Line()

class PhuruWorkbench ( Workbench ):
	"Phuru workbench object"
	MenuText = "Phuru"
	ToolTip = "Phuru workbench"
	
	def Initialize(self):
		# load the module
		Msg ("Iniciando ...\n")
		
		self.iniciarProceso()
		
	def GetClassName(self):
		return "PhuruGui::Workbench"
	
	def Activated(self):
		# do something here if needed...
		Msg ("PhuruWorkbench.Activated()\n")

	def Deactivated(self):
		# do something here if needed...
		Msg ("PhuruWorkbench.Deactivated()\n")
	
	def iniciarProceso(self):
		from PyQt4 import QtGui,QtCore
		from FreeCAD import Vector
		import serial
		
		Msg (" .... \n")
		doc = App.newDocument("PHURU")
		l = Part.Line()
		l.StartPoint = Vector(0.0,0.0,0.0)
		
		Msg ("Iniciado funcion\n")
		PuertoSerie = serial.Serial('/dev/ttyUSB0', 9600)
		def dibujarPunto():
			Msg ("Dibujar Punto \n")
			sDatos = PuertoSerie.readline()
			x,y,z,d = sDatos.split(",")
			
			Msg ("sumar punto \n")
			l.EndPoint = l.EndPoint.add(Vector(float(x),float(y),float(z)))
			Msg ("Punto sumado")
			
			doc.addObject("Part::Feature","Line").Shape = l.toShape() 
			doc.recompute()
			#l.StartPoint = Vector(l.EndPoint.x, l.EndPoint.y, l.EndPoint.z)
			
		dibujarPunto()
		Msg ("Iniciando Timer\n")
		timer = QtCore.QTimer()
		timer.timeout.connect(dibujarPunto)
		timer.start(1000)
		Msg ("Finalizando Timer\n")

FreeCADGui.addWorkbench(PhuruWorkbench())
