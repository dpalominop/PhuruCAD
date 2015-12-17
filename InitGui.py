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
			"a c #AA0000",
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
		#from Conectividad import PhUSB
		#from Conectividad import PhWifiConfiguracion
		#from Conectividad import PhWifiEjecucion
		from Avanzado import PhConfiguracion
		from Calibracion import PhControlOrientacion, PhSetParametros
		from Generales import PhDashboard

		#self.appendToolbar("PHURU", ["USB_Tool"])
		#self.appendToolbar("PHURU", ["WIFI_Tool"])
		#self.appendToolbar("PHURU", ["WIFI_EXEC"])
		self.appendToolbar("PHURU", ["CONTROL_ORIENTACION"])
		self.appendToolbar("PHURU", ["SET_PARAMETROS_CALIBRACION"])
		#self.appendMenu(["PHURU", "&Conectividad"], ["WIFI_Tool", "WIFI_EXEC"])
		self.appendMenu(["PHURU", "&Conectividad"],[])
		self.appendMenu(["PHURU", "&Generales"], ["DASHBOARD"])
		self.appendMenu(["PHURU", "&Avanzado"], ["Separator", "Configuracion"])
		self.appendMenu(["PHURU", "&Calibración"], 
					["CONTROL_ORIENTACION", "SET_PARAMETROS_CALIBRACION"])

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