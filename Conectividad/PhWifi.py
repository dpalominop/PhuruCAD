'''
Created on 22/7/2015

@author: Daniel Palomino
@email: dpalomino@phuru.pe
'''
import FreeCADGui as Gui
class Ph_Wifi():
    def GetResources(self):
        return {"MenuText": "WIFI",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Iniciar dispositivo por WIFI",
                       "Pixmap"  : """
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
            "..##..####..##..",
            "..##..####..##..",
            "..##..####..##..",
            "..##..####..##..",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "......####......",
            "................",
            "................"};
            """}

    def IsActive(self):
        return True

    def Activated(self):
        return True

Gui.addCommand('WIFI_Tool', Ph_Wifi())