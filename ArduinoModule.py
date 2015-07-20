import FreeCAD as App
import FreeCADGui as Gui
import Part
from PySide import QtCore
import serial

class USBTool():
    "Iniciar dispositivo por USB"
    
    PuertoSerie = None
    
    timer = QtCore.QTimer()
    #timer.timeout.connect(dibujarPunto)
    timer.start(500)
    

    def GetResources(self):
        return {"MenuText": "USB",
                       "Accel": "Ctrl+M",
                       "ToolTip": "Iniciar dispositivo por USB",
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
        if self.PuertoSerie == None:
            self.iniciarProceso()
        else:
            self.detenerProceso()
        
    def iniciarProceso(self):
        self.doc = App.activeDocument()
        if self.doc == None:
            self.doc = App.newDocument("PHURU")

        self.l = Part.Line()
        self.l.StartPoint = App.Vector(0.0,0.0,0.0)
        
        self.PuertoSerie = serial.Serial('/dev/ttyUSB0', 9600)
        
    def detenerProceso(self):
        self.PuertoSerie.close()
        self.PuertoSerie = None
        
    def dibujarPunto(self):
        if self.PuertoSerie == None:
            return
        else:
            sDatos = self.PuertoSerie.readline()
            x,y,z,d = sDatos.split(",")
            
            self.l.EndPoint = self.l.EndPoint.add(App.Vector(float(x),float(y),float(z)))
            
            self.doc.addObject("Part::Feature","Line").Shape = self.l.toShape() 
            self.doc.recompute()
            self.l.StartPoint = self.l.EndPoint.add(App.Vector(0.0,0.0,0.0))

Gui.addCommand('USBTool', USBTool())
    