# -*- coding: utf-8 -*-
'''
Created on 30/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''

from PySide import QtCore
from PySide.QtNetwork import QTcpSocket, QAbstractSocket
import struct
import FreeCAD as App

MAX_WAIT_LEN  = 8
PORT = 2323
IP_NUMBER = "192.168.4.1"

def genXor(msg):
    """
    Calculate xor 
    """
    my_xor = 0x00
    for ch in msg:
        my_xor^=ord(ch)
        
    return chr(my_xor)

def encodeData(dev_id, cmd, payload):
    msg = chr(len(payload)+2)+chr(dev_id)+chr(cmd)+payload ## 2 is by id and cmd
    msg = "$PHURU$" + msg + genXor(msg)
    return msg

def decodeData(data, rcv_msg):
    
# ESTADOS:   "HEADER":    0, 
#            "LENGTH":    1, 
#            "DEVICE":    2, 
#            "COMMAND":    3, 
#            "PAYLOAD":    4, 
#            "XOR":        5, 
#            "COMPLETE":    6}

    for c in data:
        if rcv_msg["restado"] == "HEADER":
            rcv_msg["rheader"] = rcv_msg["rheader"] + c
            if len(rcv_msg["rheader"])==7:
                if rcv_msg["rheader"]=="$PHURU$":
                    rcv_msg["restado"] = "LENGTH"
                else:
                    rcv_msg["rheader"] = rcv_msg["rheader"][1:]
                
        elif rcv_msg["restado"] == "LENGTH":
            rcv_msg["rlen"] = ord(c)
            rcv_msg["restado"] = "DEVICE"
            
        elif rcv_msg["restado"] == "DEVICE":
            rcv_msg["rdevice"] = ord(c)
            rcv_msg["restado"] = "COMMAND"
            
        elif rcv_msg["restado"] == "COMMAND":
            rcv_msg["rcmd"] = ord(c)
            if rcv_msg["rlen"] <= 2:
                rcv_msg["restado"] = "XOR"
            else:
                rcv_msg["restado"] = "PAYLOAD"
            
        elif rcv_msg["restado"] == "PAYLOAD":
            rcv_msg["rdata"] = rcv_msg["rdata"] + c
            if len(rcv_msg["rdata"]) == (rcv_msg["rlen"]-2):
                rcv_msg["restado"] = "XOR"
                
        elif rcv_msg["restado"] == "XOR":
            rcv_msg["rxor"] = c
            rcv_msg["restado"] = "COMPLETE"
            
            rcv_msg["rxor_rigth"] = genXor(chr(rcv_msg["rlen"])
                                         +chr(rcv_msg["rdevice"])
                                         +chr(rcv_msg["rcmd"])
                                         +rcv_msg["rdata"])
            if rcv_msg["rxor"] == rcv_msg["rxor_rigth"]:
                rcv_msg["rsucces"] = True
            else:
                rcv_msg["rerror"] = "XOR INCORRECT"


def socketStateToString(num):
    if num == 0:
        return "UnconnectedState"
    elif num == 1:
        return "HostLookupState"
    elif num == 2:
        return "ConnectingState"
    elif num == 3:
        return "ConnectedState"
    elif num == 4:
        return "BoundState"
    elif num == 5:
        return "ListeningState"
    elif num == 6:
        return "ClosingState"

class PhCliente(QTcpSocket):
    data_ready = QtCore.Signal(unicode)
    hwCheckedOk = QtCore.Signal()
    
    def __init__(self):
        QTcpSocket.__init__(self)
        self.setSocketOption(QTcpSocket.KeepAliveOption, 1)
        #self.readyRead.connect(self.on_ready_read)
        #self.connected.connect(self.on_connected)
        #self.disconnected.connect(self.on_disconnect)
        self.error.connect(self.on_error)
        self.data_ready.connect(self.print_command)

    def connectToHost(self, host, port):
        print 'connectingToHost'
        #QTcpSocket.abort(self)
        QTcpSocket.connectToHost(self, host, port)
        if QTcpSocket.waitForConnected(self, 1000):
            App.Console.PrintMessage("Connected OK\n")
        else:
            App.Console.PrintMessage("Fail Connection!\n")

    def close(self):
        print 'close!'
        self.disconnectFromHost()
        if self.isOpen():
            if (self.state() == QAbstractSocket.UnconnectedState or self.waitForDisconnected(1000)):
                App.Console.PrintMessage("SOCKET DISCONECTED!\n")
            else:
                App.Console.PrintMessage(" ERROR IN SOCKET. DISCONECTING PROCESS!\n")

    
    def on_ready_read(self):
        if self.bytesAvailable():
            App.Console.PrintMessage('read!\n')
            return str(self.readAll())
        else:
            return ""
        
    def sendData(self, data):
        App.Console.PrintMessage('write!\n')
        self.writeData('%s' % data, len(data))

    def receiveData(self):
        App.Console.PrintMessage('read!\n')
        return str(self.readAll())
    
    def sendCommand(self, dev_id, cmd, payload):
        rcv_msg = {
            "restado"    : "HEADER",
            "rheader"   : "",
            "rlen"      : -1,
            "rxor"      : "",
            "rxor_rigth": "",
            "rdata"     : "",
            "rdevice"   : -1,
            "rcmd"      : -1,
            "rstate"    : -1,
            "rerror"    : "",
            "rsucces"   : False
            }
        
        self.connectToHost(IP_NUMBER, PORT)
        
        if self.isOpen():
            self.sendData(encodeData(dev_id, cmd, payload)) 
            
            cont = 0
            while rcv_msg["restado"] != "COMPLETE":
                if self.waitForReadyRead(msecs=1000):
                    decodeData(self.on_ready_read(), rcv_msg)
                else:
                    cont = cont +1
                    if cont == 3:
                        rcv_msg["rsucces"] = False
                        rcv_msg["rerror"] = "DATA INCOMPLETE"
                        break
    
            if rcv_msg["rsucces"]:
                
                if (cmd ==  0):
                    pass

                elif (cmd ==  1):
                    pass

                elif (cmd ==  2):
                    pass
                
                elif (cmd ==  3):
                    pass
                
                elif (cmd ==  4) and (rcv_msg["rlen"] == 19):
                    rcv_msg["rdata"] = [ord(rcv_msg["rdata"][0]),
                                        struct.unpack('f', rcv_msg["rdata"][1:5])[0],
                                        struct.unpack('f', rcv_msg["rdata"][5:9])[0],
                                        struct.unpack('f', rcv_msg["rdata"][9:13])[0],
                                        struct.unpack('f', rcv_msg["rdata"][13:])[0]]
                    
                elif (cmd ==  5) and (rcv_msg["rlen"] == 42):
                    rcv_msg["rdata"] = [[struct.unpack('f', rcv_msg["rdata"][0:4])[0],
                                        struct.unpack('f', rcv_msg["rdata"][4:8])[0],
                                        struct.unpack('f', rcv_msg["rdata"][8:12])[0]],
                                        
                                        [struct.unpack('f', rcv_msg["rdata"][12:16])[0],
                                        struct.unpack('f', rcv_msg["rdata"][16:20])[0],
                                        struct.unpack('f', rcv_msg["rdata"][20:24])[0]],
                                        
                                        [struct.unpack('f', rcv_msg["rdata"][24:28])[0],
                                        struct.unpack('f', rcv_msg["rdata"][28:32])[0],
                                        struct.unpack('f', rcv_msg["rdata"][32:36])[0]],
                                        
                                        struct.unpack('f', rcv_msg["rdata"][36:40])[0]]
                    
                elif (cmd ==  6) and (rcv_msg["rlen"] == 18):
                    rcv_msg["rdata"] = [struct.unpack('f', rcv_msg["rdata"][0:4])[0],
                                        struct.unpack('f', rcv_msg["rdata"][4:8])[0],
                                        struct.unpack('f', rcv_msg["rdata"][8:12])[0],
                                        struct.unpack('f', rcv_msg["rdata"][12:16])[0]]
                
                elif (cmd ==  7) and (rcv_msg["rlen"] == 14):
                    rcv_msg["rdata"] = [struct.unpack('f', rcv_msg["rdata"][0:4])[0],
                                        struct.unpack('f', rcv_msg["rdata"][4:8])[0],
                                        struct.unpack('f', rcv_msg["rdata"][8:12])[0]]
                
                elif (cmd ==  8):
                    pass
                
                elif (cmd ==  9):
                    pass
                
                elif (cmd ==  10):
                    pass
                
                elif (cmd ==  11) and (rcv_msg["rlen"] == 19):
                    rcv_msg["rdata"] = [ord(rcv_msg["rdata"][0]),
                                        struct.unpack('f', rcv_msg["rdata"][1:5])[0],
                                        struct.unpack('f', rcv_msg["rdata"][5:9])[0],
                                        struct.unpack('f', rcv_msg["rdata"][9:13])[0],
                                        struct.unpack('f', rcv_msg["rdata"][13:])[0]]
                elif (cmd == 12):
                    pass
                
                else:
                    num = rcv_msg["rlen"] - 2
                    rcv_msg["rdata"] = [struct.unpack('f', rcv_msg["rdata"][4*i:4*i+4])[0] for i in range(num)]
                
            self.close()
        
        else:
            print "SOCKET IS CLOSED!"
            rcv_msg["rerror"] = "SOCKET IS CLOSED"
            rcv_msg["rsucces"] = False
        
        return rcv_msg
    
    @QtCore.Slot()
    def print_command(self, data):
        App.Console.PrintMessage('data!\n')
        
    @QtCore.Slot()
    def get_sstate(self):
        App.Console.PrintMessage("SOCKET STATE: " + socketStateToString(self.state()) + "\n")
        
    @QtCore.Slot()
    def on_error(self):
        App.Console.PrintMessage('error: ' + self.errorString() + "\n")
        self.close()
        #self.connectToHost(IP_NUMBER, PORT)
        #QTimer.singleShot(3000, functools.partial(self.connectToHost, IP_NUMBER, PORT))
        #QtCore.QMetaObject.invokeMethod(self, 'do_reconnect',  QtCore.Qt.QueuedConnection)

    @QtCore.Slot()
    def do_reconnect(self):
        App.Console.PrintMessage('Trying to reconnect\n')
        self.close()
        self.connectToHost(IP_NUMBER, PORT)
        
    @QtCore.Slot()
    def on_disconnect(self):
        App.Console.PrintMessage('disconnected!\n')
        
    @QtCore.Slot()
    def on_connected(self):
        App.Console.PrintMessage('connected!\n')
        
    @QtCore.Slot()
    def on_checkHardware(self):
        rmsg =  main_socket.sendCommand(1, 2, "LAS CUQUIS")
        if rmsg["rsucces"]:
            self.hwCheckedOk.emit()
        

if __name__ == "__main__":
    
    main_socket = PhCliente()
    
    total_xor_fail = 0
    total_errores = 0
    for i in range(200):
        
        rmsg =  main_socket.sendCommand(1, 8, "LAS CUQUIS")
        print rmsg
        if rmsg["rerror"] == "XOR INCORRECT":
            total_xor_fail += 1
        if rmsg["rsucces"] == False:
            total_errores += 1
        
    print "Numero Total de errores: ", total_errores
    print "Numero de errores en xor: ", total_xor_fail
