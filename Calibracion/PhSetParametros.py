'''
Created on 12/11/2015

@author: dpalominop
'''

#from PySide import QtCore
from PySide.QtCore import *
from PySide.QtSql import *

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft

from Vistas.PhWSetParametros import *
from Socket.PhCliente import *
from Vistas.PhWSetParametros import *

#def computeHash(original):
#    return QCryptographicHash.hash(QString(original).toUtf8(), QCryptographicHash.Md5).toHex()

# Estimar parametros
def fitfunc(p,coords):
    x0,y0,z0,a,b,c=p
    x,y,z=coords.T
    return ((x-x0)/a)**2+((y-y0)/b)**2+((z-z0)/c)**2


class PhSetParametros(QtCore.QObject):
    """Settear parametros de los sensores"""
    
    def GetResources(self):
        return {"MenuText": "&SET PARAMETROS DE CALIBRACION",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Settear parametros de calibracion del dispositivo.",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        
        #app = QtCore.QCoreApplication(sys.argv)
        self.timer = QtCore.QTimer()
        self.socket = PhCliente()
        
        self.wCalibracion = PhWSetParametros()
        
        QtCore.QObject.connect(self.wCalibracion.SetMagnetometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("M_CAL_MAG()"))
        
        QtCore.QObject.connect(self.wCalibracion.SetAcelerometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("M_CAL_ACC()"))
        
        QtCore.QObject.connect(self.wCalibracion.SetGiroscopo, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("M_CAL_GYR()"))
        
        QtCore.QObject.connect(self.wCalibracion.Salir,
                               QtCore.SIGNAL("pressed()"),
                               self,
                               QtCore.SLOT("exit()"))
        
        self.iniciarProceso()
        #self.wConfiguracion.connect(QtCore.SIGNAL("windowFinished()"), QtCore.SLOT("iniciarProceso()"))
        
    @QtCore.Slot()
    def iniciarProceso(self):
        self.doc = App.activeDocument()
        if self.doc == None:
            self.doc = App.newDocument("Parametros")

        self.dbConnect()
        self.desp = 50
        #Sistema de referencia general
        Draft.makeLine(App.Vector(0,0,0),App.Vector(10,0,0))
        Draft.makeLine(App.Vector(0,0,0),App.Vector(0,10,0))
        Draft.makeLine(App.Vector(0,0,0),App.Vector(0,0,10))
        
        #Sistema de referencia del Magnetometro
        Draft.makeLine(App.Vector(self.desp,self.desp,0),App.Vector(40+self.desp,self.desp,0))
        Draft.makeLine(App.Vector(self.desp,self.desp,0),App.Vector(self.desp,40+self.desp,0))
        Draft.makeLine(App.Vector(self.desp,self.desp,0),App.Vector(self.desp,self.desp,40))
        Draft.makeLine(App.Vector(self.desp,self.desp,0),App.Vector(10+self.desp,10+self.desp,10))
        
        #Sistema de referencia del Accelerometro
        Draft.makeLine(App.Vector(-self.desp,-self.desp,0),App.Vector(40-self.desp,-self.desp,0))
        Draft.makeLine(App.Vector(-self.desp,-self.desp,0),App.Vector(-self.desp,40-self.desp,0))
        Draft.makeLine(App.Vector(-self.desp,-self.desp,0),App.Vector(-self.desp,-self.desp,40))
        Draft.makeLine(App.Vector(-self.desp,-self.desp,0),App.Vector(10-self.desp,10-self.desp,10))
        
        #Sistema de referencia del Giroscopo
        Draft.makeLine(App.Vector(0,0,self.desp),App.Vector(40,0,self.desp))
        Draft.makeLine(App.Vector(0,0,self.desp),App.Vector(0,40,self.desp))
        Draft.makeLine(App.Vector(0,0,self.desp),App.Vector(0,0,40+self.desp))
        Draft.makeLine(App.Vector(0,0,self.desp),App.Vector(10,10,10+self.desp))
        
        
        #App.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewAxometric()
        
        #Coloreado de sistema de referencia general
        Gui.getDocument(self.doc.Label).getObject("Line").LineColor = (1.00,0.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line001").LineColor = (0.00,1.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line002").LineColor = (0.00,0.00,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line001").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line002").PointColor = (0.67,0.67,1.00)
        
        #Coloreado de sistema de referencia del Magnetometro
        Gui.getDocument(self.doc.Label).getObject("Line003").LineColor = (1.00,0.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line004").LineColor = (0.00,1.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line005").LineColor = (0.00,0.00,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line006").LineColor = (1.00,1.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line003").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line004").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line005").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line006").PointColor = (0.67,0.67,1.00)
        
        #Coloreado de sistema de referencia del Acelerometro
        Gui.getDocument(self.doc.Label).getObject("Line007").LineColor = (1.00,0.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line008").LineColor = (0.00,1.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line009").LineColor = (0.00,0.00,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line010").LineColor = (0.00,1.00,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line007").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line008").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line009").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line010").PointColor = (0.67,0.67,1.00)
        
        #Coloreado de sistema de referencia del Giroscopo
        Gui.getDocument(self.doc.Label).getObject("Line011").LineColor = (1.00,0.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line012").LineColor = (0.00,1.00,0.00)
        Gui.getDocument(self.doc.Label).getObject("Line013").LineColor = (0.00,0.00,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line014").LineColor = (1.00,0.00,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line011").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line012").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line013").PointColor = (0.67,0.67,1.00)
        Gui.getDocument(self.doc.Label).getObject("Line014").PointColor = (0.67,0.67,1.00)
        
        self.timer.timeout.connect(self.dibujarPunto)
        #self.timer.start(100)
        
    def detenerProceso(self):
        #self.PuertoSerie.close()
        #self.PuertoSerie = None
        pass
    
    def dibujarPunto(self):
        #if self.PuertoSerie == None:
        #    return
        #else:
        rmsg = self.socket.sendCommand(1, 5, "")
        App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
        
        if rmsg["rsucces"]:
            v_mag, v_accel, v_gyr, t = rmsg["rdata"]
            self.dbInsert(v_mag, v_accel, v_gyr, t)
            
            Gui.getDocument(self.doc.Label).getObject("Line003").End = (v_mag[0]+self.desp, v_mag[1]+self.desp, v_mag[2])
            Gui.getDocument(self.doc.Label).getObject("Line003").End = (v_accel[0]-self.desp, v_accel[1]-self.desp, v_accel[2])
            Gui.getDocument(self.doc.Label).getObject("Line003").End = (v_gyr[0], v_gyr[1], v_gyr[2]+self.desp)

    @QtCore.Slot()
    def M_CAL_MAG(self):
        pass
    
    @QtCore.Slot()
    def M_CAL_ACC(self):
        pass
    
    @QtCore.Slot()
    def M_CAL_GYR(self):
        pass
    
    def dbConnect(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        filename = "phuru.db"
        database =  QFile(filename)
        if not database.exists():
            App.Console.PrintMessage("Database not found. Creating and opening")
            self.db.setDatabaseName(filename)
            self.db.open()
            self.query = QSqlQuery()
            self.query.exec_("create table ph_sensors "
                        "(id integer primary key autoincrement, "
                        "mag_x float(4), "
                        "mag_y float(4), "
                        "mag_z float(4), "
                        "accel_x float(4)), "
                        "accel_y float(4)), "
                        "accel_z float(4)), "
                        "gyr_x float(4), "
                        "gyr_y float(4), "
                        "gyr_z float(4), "
                        "time float(4)")
        else:
            App.Console.PrintMessage("Database found. Opening")
            self.db.setDatabaseName(filename)
            self.db.open()
            
        return self.db.isOpen()
    
    def dbInsert(self, v_mag, v_accel, v_gyr, t):
        self.query.prepare("insert into ph_sensors "
                          "(mag_x, mag_x, mag_x, accel_x, accel_y, accel_z, gyr_x, gyr_y, gyr_z, time) " 
                          "values(:mag_x, :mag_y, :mag_z, :accel_x :accel_y :accel_z, :gyr_x, :gyr_y, :gyr_z, :time)")
                            
        self.query.bindValue(":mag_x", v_mag[0])
        self.query.bindValue(":mag_y", v_mag[1])
        self.query.bindValue(":mag_z", v_mag[2])
        self.query.bindValue(":accel_x", v_accel[0])
        self.query.bindValue(":accel_y", v_accel[1])
        self.query.bindValue(":accel_z", v_accel[2])
        self.query.bindValue(":gyr_x", v_gyr[0])
        self.query.bindValue(":gyr_y", v_gyr[1])
        self.query.bindValue(":gyr_z", v_gyr[2])
        self.query.bindValue(":time", t)
        
        self.query.exec_()

Gui.addCommand('SET_PARAMETROS_CALIBRACION', PhSetParametros())

if __name__ == '__main__':
    pass