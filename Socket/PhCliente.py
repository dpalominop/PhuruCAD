# -*- coding: utf-8 -*-
'''
Created on 30/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''

import sys
from PySide import QtCore
from PySide.QtNetwork import QTcpSocket
import struct

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
            
            if rcv_msg["rxor"] != genXor(chr(rcv_msg["rlen"])
                                         +chr(rcv_msg["rdevice"])
                                         +chr(rcv_msg["rcmd"])
                                         +rcv_msg["rdata"]):
                rcv_msg["rsucces"] = False
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
    
    def __init__(self):
        QTcpSocket.__init__(self)
        self.setSocketOption(QTcpSocket.KeepAliveOption, 1)
        #self.readyRead.connect(self.on_ready_read)
        self.connected.connect(self.on_connected)
        self.disconnected.connect(self.on_disconnect)
        self.error.connect(self.on_error)
        self.data_ready.connect(self.print_command)

    def connectToHost(self, host, port):
        print 'connectingToHost'
        QTcpSocket.abort(self)
        QTcpSocket.connectToHost(self, host, port)

    def close(self):
        print 'close!'
        self.disconnectFromHost()

    
    def on_ready_read(self):
        if self.bytesAvailable():
            print 'read!'
            return str(self.readAll())
        else:
            return ""
        
    def sendData(self, data):
        print 'write!'
        self.writeData('%s' % data, len(data))

    def receiveData(self):
        print 'read!'
        return str(self.readAll())
    
    def sendCommand(self, dev_id, cmd, payload):
        self.connectToHost(IP_NUMBER, PORT)
        
        self.sendData(encodeData(dev_id, cmd, payload)) 
        
        rcv_msg = {
        "restado"    : "HEADER",
        "rheader"   : "",
        "rlen"      : 0,
        "rxor"      : "",
        "rdata"     : "",
        "rdevice"   : 0,
        "rcmd"      : 0,
        "rerror"    : "",
        "rsucces"   : True
        }
        
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

        if rcv_msg["rsucces"] and (rcv_msg["rlen"] == 18):
            rcv_msg["rdata"] = [struct.unpack('f', rcv_msg["rdata"][0:4])[0],
                                struct.unpack('f', rcv_msg["rdata"][4:8])[0],
                                struct.unpack('f', rcv_msg["rdata"][8:12])[0],
                                struct.unpack('f', rcv_msg["rdata"][12:])[0]]
            
        self.close()
        return rcv_msg
    
    @QtCore.Slot()
    def print_command(self, data):
        print 'data!'
        
    @QtCore.Slot()
    def get_sstate(self):
        print "SOCKET STATE: ", socketStateToString(self.state())
        
    @QtCore.Slot()
    def on_error(self):
        print 'error', self.errorString()
        self.close()
        #self.connectToHost(IP_NUMBER, PORT)
        #QTimer.singleShot(3000, functools.partial(self.connectToHost, IP_NUMBER, PORT))
        QtCore.QMetaObject.invokeMethod(self, 'do_reconnect',  QtCore.Qt.QueuedConnection)

    @QtCore.Slot()
    def do_reconnect(self):
        print 'Trying to reconnect'
        self.connectToHost(IP_NUMBER, PORT)
        
    @QtCore.Slot()
    def on_disconnect(self):
        print 'disconnected!'
        
    @QtCore.Slot()
    def on_connected(self):
        print 'connected!'
        

if __name__ == "__main__":
    #app = QtCore.QCoreApplication(sys.argv)
    main_socket = PhCliente()
    #state_timer = QtCore.QTimer()
    #state_timer.setInterval(1000)
    #state_timer.timeout.connect(main_socket.get_sstate)
    #state_timer.start()
    #main_socket.connectToHost(IP_NUMBER, PORT)
    main_socket.sendCommand(1, 4, "CUCHAROS")
    #sys.exit(app.exec_())
    
