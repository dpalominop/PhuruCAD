'''
Created on 12/11/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''

#from PySide import QtCore
from PySide.QtCore import *
from PySide.QtSql import *

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
from scipy.optimize import leastsq
import numpy as np
import os

from Vistas.PhWSetParametros import *
from Socket.PhCliente import *
from Vistas.PhWSetParametros import *
from atk import Document


# Estimar parametros
def fitfunc(p,coords):
    x0,y0,z0,a,b,c=p
    x,y,z=coords.T
    return ((x-x0)/a)**2+((y-y0)/b)**2+((z-z0)/c)**2

def normalizar(v, scale):
    mod = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
    v = ((1/mod)*v[0]*scale, (1/mod)*v[1]*scale, (1/mod)*v[2]*scale)
    return v

class PhSetParametros(QtCore.QObject):
    """Settear parametros de los sensores"""
    
    cal_mag = QtCore.Signal()
    cal_acc = QtCore.Signal()
    cal_gyr = QtCore.Signal()
    tabla   = ""
    
    def GetResources(self):
        return {"MenuText": "&SET PARAMETROS DE CALIBRACION",
                       "Accel": "Ctrl+N",
                       "ToolTip": "Settear parametros de calibracion del dispositivo.",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        self.wCalibracion = PhWSetParametros()
        self.enableCommandos(False)
        self.wCalibracion.Iniciar.setEnabled(True)
        self.wCalibracion.Detener.setEnabled(False)
        
        QtCore.QObject.connect(self.wCalibracion.SetMagnetometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("INIT_CONT()"))
        
        QtCore.QObject.connect(self.wCalibracion.SetAcelerometro, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("INIT_CONT()"))
        
        QtCore.QObject.connect(self.wCalibracion.SetGiroscopo, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("INIT_CONT()"))
        
        QtCore.QObject.connect(self.wCalibracion.Iniciar,
                               QtCore.SIGNAL("pressed()"),
                               self,
                               QtCore.SLOT("IniciarProceso()"))
        
        QtCore.QObject.connect(self.wCalibracion.Detener,
                               QtCore.SIGNAL("pressed()"),
                               self,
                               QtCore.SLOT("PausarProceso()"))
        
        QtCore.QObject.connect(self.wCalibracion,
                               QtCore.SIGNAL("windowFinished()"),
                               self,
                               QtCore.SLOT("FinalizarProceso()"))
        
        self.crearVista()
        self.dbCrear()
        
    def crearVista(self):
        self.Document = App.newDocument("PhCalibrarSensores")
        self.GuiDocument = Gui.getDocument(self.Document.Name)
        App.ActiveDocument = self.Document
        Gui.ActiveDocument = self.GuiDocument
        
        self.desp = 80
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
        self.GuiDocument.activeView().viewAxometric()
        
        #Coloreado de sistema de referencia general
        self.GuiDocument.getObject("Line").LineColor = (1.00,0.00,0.00)
        self.GuiDocument.getObject("Line001").LineColor = (0.00,1.00,0.00)
        self.GuiDocument.getObject("Line002").LineColor = (0.00,0.00,1.00)
        self.GuiDocument.getObject("Line").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line001").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line002").PointColor = (0.67,0.67,1.00)
        
        #Coloreado de sistema de referencia del Magnetometro
        self.GuiDocument.getObject("Line003").LineColor = (1.00,0.00,0.00)
        self.GuiDocument.getObject("Line004").LineColor = (0.00,1.00,0.00)
        self.GuiDocument.getObject("Line005").LineColor = (0.00,0.00,1.00)
        self.GuiDocument.getObject("Line006").LineColor = (1.00,1.00,0.00)
        self.GuiDocument.getObject("Line003").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line004").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line005").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line006").PointColor = (0.67,0.67,1.00)
        
        #Coloreado de sistema de referencia del Acelerometro
        self.GuiDocument.getObject("Line007").LineColor = (1.00,0.00,0.00)
        self.GuiDocument.getObject("Line008").LineColor = (0.00,1.00,0.00)
        self.GuiDocument.getObject("Line009").LineColor = (0.00,0.00,1.00)
        self.GuiDocument.getObject("Line010").LineColor = (0.00,1.00,1.00)
        self.GuiDocument.getObject("Line007").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line008").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line009").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line010").PointColor = (0.67,0.67,1.00)
        
        #Coloreado de sistema de referencia del Giroscopo
        self.GuiDocument.getObject("Line011").LineColor = (1.00,0.00,0.00)
        self.GuiDocument.getObject("Line012").LineColor = (0.00,1.00,0.00)
        self.GuiDocument.getObject("Line013").LineColor = (0.00,0.00,1.00)
        self.GuiDocument.getObject("Line014").LineColor = (1.00,0.00,1.00)
        self.GuiDocument.getObject("Line011").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line012").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line013").PointColor = (0.67,0.67,1.00)
        self.GuiDocument.getObject("Line014").PointColor = (0.67,0.67,1.00)
    
    def dibujarPunto(self):
        rmsg = self.socket.sendCommand(1, 5, "")
        
        if rmsg["rsucces"]:
            App.Console.PrintMessage("rdata: " + str(rmsg["rdata"]) + "\n")
            v_mag, v_accel, v_gyr, t = rmsg["rdata"]
            v_mag = normalizar(v_mag, 40)
            v_accel = normalizar(v_accel, 40)
            v_gyr = normalizar(v_gyr, 40)
            
            self.Document.getObject("Line006").End = (v_mag[0]+self.desp, v_mag[1]+self.desp, v_mag[2])
            self.Document.getObject("Line010").End = (v_accel[0]-self.desp, v_accel[1]-self.desp, v_accel[2])
            self.Document.getObject("Line014").End = (v_gyr[0], v_gyr[1], v_gyr[2]+self.desp)
            self.Document.recompute()
            
            if self.grabar:
                self.dbInsert(v_mag, v_accel, v_gyr, t) 
                self.cont = self.cont + 1
                
                if self.cont == 200:
                    self.timer.stop()
                    self.cont = 0
                    self.grabar = False
                    self.enviarParamteros(self.M_CAL_MAG())
                        
                    if not self.timer.isActive():
                        self.timer = QtCore.QTimer()
                        self.timer.timeout.connect(self.dibujarPunto)
                        self.timer.start(100)
                        
                    self.enableCommandos(True)
        else:
            App.Console.PrintMessage("rerror: " + str(rmsg["rerror"]) + "\n")

    def enviarParamteros(self, p):
        v_max_min = struct.pack("ffffff", 
                                p[0]+p[3],p[1]+p[4],p[2]+p[5],
                                p[0]-p[3],p[1]-p[4],p[2]-p[5])
                    
        rmsg = self.socket.sendCommand(1, 8, v_max_min)
        while rmsg["rsucces"]:
            rmsg = self.socket.sendCommand(1, 8, v_max_min)

    def enableCommandos(self, val):
        if val:
            self.wCalibracion.SetMagnetometro.setEnabled(True)
            self.wCalibracion.SetAcelerometro.setEnabled(True)
            self.wCalibracion.SetGiroscopo.setEnabled(True)
        else:
            self.wCalibracion.SetMagnetometro.setEnabled(False)
            self.wCalibracion.SetAcelerometro.setEnabled(False)
            self.wCalibracion.SetGiroscopo.setEnabled(False)

    @QtCore.Slot()
    def INIT_CONT(self):
        self.enableCommandos(False)
        self.dbCrearTabla()
        self.grabar = True
        self.cont = 0

    @QtCore.Slot()
    def M_CAL_MAG(self):
        coords = self.dbSelect("mag")
        coords = np.array(coords)
        
        #coords_max, coords_min = self.dbSelectMaxMin("mag")
        #coords_max = np.array(coords_max)
        #coords_min = np.array(coords_min)
        #media = (coords_max + coords_min)/2
        #diff = (coords_max - coords_min)/2
        
        #p0 = media + diff
        #p0 = np.array(p0)
        p0 = np.concatenate(((coords.max(axis=0)+coords.min(axis=0))/2, (coords.max(axis=0)-coords.min(axis=0))/2), axis=0)
        
        errfunc = lambda p,x: fitfunc(p,x)-1
        p, flag = leastsq(errfunc,p0,args=(coords,))
        
        return p
    
    @QtCore.Slot()
    def M_CAL_ACC(self):
        pass
    
    @QtCore.Slot()
    def M_CAL_GYR(self):
        pass
    
    def dbCrear(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        filename = os.path.dirname(os.path.abspath(__file__)) + "/../phuru.db"
        App.Console.PrintMessage("rpath: " + filename + "\n")
        #database =  QFile(filename)
        self.db.setDatabaseName(filename)
        self.db.open()

        return self.db.isOpen()
    
    def dbCrearTabla(self):
        self.tabla = "ph_sensors_" + self.dbCalcularNumTablas()
        self.query = QSqlQuery(self.db)
        self.query.exec_("""create table {0}
                        (id integer primary key autoincrement,
                        mag_x float(4),
                        mag_y float(4),
                        mag_z float(4),
                        accel_x float(4),
                        accel_y float(4),
                        accel_z float(4),
                        gyr_x float(4),
                        gyr_y float(4),
                        gyr_z float(4),
                        time float(4))""".format(self.tabla))
    
    def dbInsert(self, v_mag, v_accel, v_gyr, t):
        self.query = QSqlQuery(self.db)
        self.query.prepare("""insert into {0}  
                          (mag_x, mag_y, mag_z, accel_x, accel_y, accel_z, gyr_x, gyr_y, gyr_z, time) 
                          values (:mag_x, :mag_y, :mag_z, :accel_x, :accel_y, :accel_z, :gyr_x, :gyr_y, :gyr_z, :time)""".format(self.tabla))
                            
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
        
    def dbSelectMaxMin(self, campo):
        q = QSqlQuery("""select max({0}_x) as A, max({0}_y) as B, 
                      max({0}_z) as C, min({0}_x) as D, min({0}_y) as E, 
                      min({0}_z) as F from {1}""".format(campo, self.tabla))
        
        rec = q.record()
        
        A = rec.indexOf("A")
        B = rec.indexOf("B")
        C = rec.indexOf("C")
        D = rec.indexOf("D")
        E = rec.indexOf("E")
        F = rec.indexOf("F")
        
        q.next() 
            
        return [[q.value(A), q.value(B), q.value(C)], [q.value(D), q.value(E),q.value(F)]]
    
    def dbSelect(self, campo):
        q = QSqlQuery("""select {0}_x as A, {0}_y as B, 
                      {0}_z as C from {1}""".format(campo, self.tabla))
        rec = q.record()
        
        A = rec.indexOf("A")
        B = rec.indexOf("B")
        C = rec.indexOf("C")
        
        resp = []
        while q.next():
            resp.append([q.value(A), q.value(B), q.value(C)])
        return resp
    
    def dbCalcularNumTablas(self):
        try:
            q = QSqlQuery("SELECT Count(*) AS NUM FROM sqlite_master")
            rec = q.record()
            num = rec.indexOf("NUM")
            q.next()
            return str(q.value(num))
        except:
            return "0"

    @QtCore.Slot()
    def FinalizarProceso(self):
        App.Console.PrintMessage("Finalizando Proceso ...\n")
        self.timer.stop()
        self.timer.disconnect()
        self.timer.killTimer()
        self.timer.deleteLater()
        self.socket.deleteLater()
        App.Console.PrintMessage("Proceso Finalizado\n")
        #self.deleteLater()
        
    @QtCore.Slot()
    def IniciarProceso(self):
        App.Console.PrintMessage("Iniciando Proceso ...\n")
        self.socket = PhCliente()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.dibujarPunto)
        self.timer.start(100)
        self.enableCommandos(True)
        self.wCalibracion.Iniciar.setEnabled(False)
        self.wCalibracion.Detener.setEnabled(True)
        App.Console.PrintMessage("Proceso Iniciado\n")
    
    @QtCore.Slot()
    def PausarProceso(self):
        App.Console.PrintMessage("Pausando Proceso ...\n")
        self.timer.stop()
        self.wCalibracion.Detener.setEnabled(False)
        self.wCalibracion.Iniciar.setEnabled(True)
        self.timer.deleteLater()
        self.socket.deleteLater()
        App.Console.PrintMessage("Proceso Pausado\n")
        

Gui.addCommand('SET_PARAMETROS_CALIBRACION', PhSetParametros())

if __name__ == '__main__':
    pass