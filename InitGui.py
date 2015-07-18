# Phuru gui init module
# (c) 2001 Juergen Riegel LGPL¿

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
		import ArduinoModule
		self.appendToolbar("My Tools", ["ArduinoCAD"])
		self.appendMenu("My Tools", ["ArduinoCAD"])

	def GetClassName(self):
		#return "PhuruGui::Workbench"
		return "Gui::PythonWorkbench"

	def Activated(self):
		# do something here if needed...
		Msg ("PhuruWorkbench.Activated()\n")

	def Deactivated(self):
		# do something here if needed...
		Msg ("PhuruWorkbench.Deactivated()\n")

FreeCADGui.addWorkbench(PhuruWorkbench)
