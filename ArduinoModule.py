import FreeCAD as App
import FreeCADGui as Gui
import Part

class MyTool:
    "My tool object"
    from PySide import QtCore
    timer = QtCore.QTimer()

    def GetResources(self):
        return {"MenuText": "My Command",
                       "Accel": "Ctrl+M",
                       "ToolTip": "Comando de DANIEL",
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
            """}

    def IsActive(self):
        return True
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True

    def Activated(self):
        # do something here...
        print "Activando comando"
        self.iniciarProceso()
        
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

Gui.addCommand('ArduinoCAD', MyTool())