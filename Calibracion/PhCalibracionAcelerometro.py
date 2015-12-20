'''
Created on 19/12/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.ip
'''

from PySide import QtCore
from PySide.QtSql import *

import FreeCADGui as Gui
import FreeCAD as App
import Part, Draft
import math
import os

from Socket.PhCliente import *
from Vistas.PhWCalibracionAcelerometro import *

class PhCalibracionAcelerometro(QtCore.QObject):
    """Iniciar y detener envio de datos por WIFI"""
    
    start = True
    def GetResources(self):
        return {"MenuText": "&CALIBRAR ACELEROMETRO",
                       "Accel": "Ctrl+N",
                       "ToolTip": "",
                       "Pixmap"  : ""
        }

    def IsActive(self):
        return True

    def Activated(self):
        self.wCalibracionAcelerometro = PhWCalibracionAcelerometro()
        self.habilitarBotones(False)
        self.wCalibracionAcelerometro.INICIAR.setEnabled(True)
        self.wCalibracionAcelerometro.SALIR.setEnabled(True)
        
        self.dbCrearDB()
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.INICIAR, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("onIniciar()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.X_MENOS, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("calcularPromedioParcial()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.X_MAS, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("calcularPromedioParcial()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.Y_MENOS, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("calcularPromedioParcial()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.Y_MAS, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("calcularPromedioParcial()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.Z_MENOS, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("calcularPromedioParcial()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.Z_MAS, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("calcularPromedioParcial()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro.ENVIAR, 
                               QtCore.SIGNAL("pressed()"), 
                               self, 
                               QtCore.SLOT("onEnviarParametros()"))
        
        QtCore.QObject.connect(self.wCalibracionAcelerometro, 
                               QtCore.SIGNAL("windowFinished()"), 
                               self, 
                               QtCore.SLOT("onSalir()"))
        
        
    def habilitarBotones(self, val):
        self.wCalibracionAcelerometro.X_MENOS.setEnabled(val)
        self.wCalibracionAcelerometro.PROM_X_MENOS.setEnabled(val)
        self.wCalibracionAcelerometro.X_MAS.setEnabled(val)
        self.wCalibracionAcelerometro.PROM_X_MAS.setEnabled(val)
        
        self.wCalibracionAcelerometro.Y_MENOS.setEnabled(val)
        self.wCalibracionAcelerometro.PROM_Y_MENOS.setEnabled(val)
        self.wCalibracionAcelerometro.Y_MAS.setEnabled(val)
        self.wCalibracionAcelerometro.PROM_Y_MAS.setEnabled(val)
        
        self.wCalibracionAcelerometro.Z_MENOS.setEnabled(val)
        self.wCalibracionAcelerometro.PROM_Z_MENOS.setEnabled(val)
        self.wCalibracionAcelerometro.Z_MAS.setEnabled(val)
        self.wCalibracionAcelerometro.PROM_Z_MAS.setEnabled(val)
        
        self.wCalibracionAcelerometro.INICIAR.setEnabled(val)
        self.wCalibracionAcelerometro.ENVIAR.setEnabled(val)
        self.wCalibracionAcelerometro.SALIR.setEnabled(val)
      
      
        
    @QtCore.Slot()
    def onIniciar(self):
        self.dbCrearTabla()
        self.habilitarBotones(True)
          
    @QtCore.Slot()
    def calcularPromedioParcial(self):
        prom = "EXITO"
        if self.wCalibracionAcelerometro.X_MENOS == self.sender():
            self.wCalibracionAcelerometro.PROM_X_MENOS.setText(prom)
        elif self.wCalibracionAcelerometro.X_MAS == self.sender():
            self.wCalibracionAcelerometro.PROM_X_MAS.setText(prom)
        elif self.wCalibracionAcelerometro.Y_MENOS == self.sender():
            self.wCalibracionAcelerometro.PROM_Y_MENOS.setText(prom)
        elif self.wCalibracionAcelerometro.Y_MAS == self.sender():
            self.wCalibracionAcelerometro.PROM_Y_MAS.setText(prom)
        elif self.wCalibracionAcelerometro.Z_MENOS == self.sender():
            self.wCalibracionAcelerometro.PROM_Z_MENOS.setText(prom)
        elif self.wCalibracionAcelerometro.Z_MAS == self.sender():
            self.wCalibracionAcelerometro.PROM_Z_MAS.setText(prom)

    @QtCore.Slot()
    def onEnviarParametros(self):
        pass
    
    @QtCore.Slot()
    def onSalir(self):
        pass
        
    def dbCrearDB(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        filename = os.path.dirname(os.path.abspath(__file__)) + "/../calibracion_acelerometro.db"
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
        
Gui.addCommand('CALIBRACION_ACELEROMETRO', PhCalibracionAcelerometro())


if __name__ == '__main__':
    pass
        
        