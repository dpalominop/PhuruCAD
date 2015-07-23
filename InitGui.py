'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''

import FreeCADGui

class PhuruWorkbench ( Workbench ):
	"Phuru workbench object"
	Icon = """
			/* XPM */
			static const char *test_icon[]={
			"16 16 2 1",
			"a c #000000",
			". c None",
			"................",
			"................",
			"..############..",
			"..############..",
			"..############..",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"................",
			"................"};
			"""
	MenuText = "Phuru"
	ToolTip = "Phuru workbench"

	def Initialize(self):
		from Conectividad import PhUSB, PhWifi
		from Avanzado import Configuracion
		self.appendToolbar("PHURU", ["USB_Tool"])
		self.appendToolbar("PHURU", ["WIFI_Tool"])
		self.appendMenu(["PHURU", "Conectividad"], ["WIFI_Tool", "USB_Tool"])
		self.appendMenu(["PHURU", "Avanzado ..."], ["Separator", "Configuracion"])

	def GetClassName(self):
		#return "PhuruGui::Workbench"
		return "Gui::PythonWorkbench"

	def Activated(self):
		# do something here if needed...
		Msg ("PhuruWorkbench.Activated()\n")

	def Deactivated(self):
		# do something here if needed...
		Msg ("PhuruWorkbench.Deactivated()\n")

FreeCADGui.addWorkbench(PhuruWorkbench())