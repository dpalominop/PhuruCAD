# Phuru gui init module
# (c) 2001 Juergen Riegel LGPL

import FreeCAD as App
import FreeCADGui as Gui
import Part,PartGui

class PhuruWorkbench ( Workbench ):
	from PySide import QtGui,QtCore
	"Phuru workbench object"
	MenuText = "Phuru"
	ToolTip = "Phuru workbench"
	timer = QtCore.QTimer()
	#doc = App.newDocument("PHURU")
	#l = Part.Line()
	
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
		import serial
		#from PySide import QtGui,QtCore
		
		doc = App.newDocument("PHURU")
		l = Part.Line()
		l.StartPoint = App.Vector(0.0,0.0,0.0)
		
		PuertoSerie = serial.Serial('/dev/ttyUSB0', 9600)
		
		def dibujarPunto():
			sDatos = PuertoSerie.readline()
			x,y,z,d = sDatos.split(",")
			
			l.EndPoint = l.EndPoint.add(App.Vector(float(x),float(y),float(z)))
			
			doc.addObject("Part::Feature","Line").Shape = l.toShape() 
			doc.recompute()
			l.StartPoint = l.EndPoint.add(App.Vector(0.0,0.0,0.0))

		#timer = QtCore.QTimer()
		self.timer.timeout.connect(dibujarPunto)
		self.timer.start(1000)
		

Gui.addWorkbench(PhuruWorkbench())
