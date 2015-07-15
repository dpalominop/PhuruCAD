# Phuru gui init module
# (c) 2001 Juergen Riegel LGPL

class PhuruWorkbench ( Workbench ):
	"Phuru workbench object"
	MenuText = "Phuru"
	ToolTip = "Phuru workbench"
	def Initialize(self):
		# load the module
		import PhuruGui
		
		
	def GetClassName(self):
		return "PhuruGui::Workbench"
	
	def Activated(self):
		# do something here if needed...
		Msg ("MyWorkbench.Activated()\n")

	def Deactivated(self):
		# do something here if needed...
		Msg ("MyWorkbench.Deactivated()\n")

Gui.addWorkbench(PhuruWorkbench())
