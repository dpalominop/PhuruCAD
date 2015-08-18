# -*- coding: utf-8 -*-
'''
Created on 30/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.io
'''

import sys
from PySide import QtCore
from PySide.QtNetwork import QTcpSocket

MAX_WAIT_LEN  = 8
PORT = 2323
IP_NUMBER = "192.168.4.1"

def encodeData(dev_id, cmd, payload):
    my_xor = chr(64)
    msg = "$PHURU$"+chr(len(payload))+chr(dev_id)+chr(cmd)+payload+my_xor
    return msg, my_xor

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
            if rcv_msg["rlen"] == 2:
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
        #self.connected.connect(self.on_connected)
        self.disconnected.connect(self.on_disconnect)
        self.error.connect(self.on_error)
        self.data_ready.connect(self.print_command)

    def connectToHost(self, host, port):
        print 'connectToHost'
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
        self.writeData('%s' % data)

    def receiveData(self):
        print 'read!'
        return str(self.readAll())
    
    def sendCommand(self, dev_id, cmd, payload):
        
        snd_msg, self.xor = encodeData(dev_id, cmd, payload)
        self.sendData(snd_msg)
        
        rcv_msg = {
        "restado"    : "HEADER",
        "rheader"   : "",
        "rlen"      : 0,
        "rxor"      : "",
        "rdata"     : "",
        "rdevice"   : 0,
        "rcmd"      : 0
        }
        
        cont = 0
        while rcv_msg["restado"] != "COMPLETE":
            if self.waitForReadyRead(msecs=1000):
                decodeData(self.on_ready_read(), rcv_msg)
            else:
                cont = cont +1
                if cont == 3:
                    print "ERROR: NONE DATA"
                    rcv_msg["restado"] = "COMPLETE"

        print rcv_msg
        return rcv_msg
    
    @QtCore.pyqtSlot()
    def print_command(self, data):
        print 'data!'
        
    @QtCore.pyqtSlot()
    def get_sstate(self):
        print "SOCKET STATE: ", socketStateToString(self.state())
        
    @QtCore.pyqtSlot()
    def on_error(self):
        print 'error', self.errorString()
        self.close()
        #self.connectToHost(IP_NUMBER, PORT)
        #QTimer.singleShot(3000, functools.partial(self.connectToHost, IP_NUMBER, PORT))
        QtCore.QMetaObject.invokeMethod(self, 'do_reconnect',  QtCore.Qt.QueuedConnection)

    @QtCore.pyqtSlot()
    def do_reconnect(self):
        print 'Trying to reconnect'
        self.connectToHost(IP_NUMBER, PORT)
        
    @QtCore.pyqtSlot()
    def on_disconnect(self):
        print 'disconnected!'
        
    @QtCore.pyqtSlot()
    def on_connected(self):
        print 'connected!'
        

if __name__ == "__main__":
    app = QtCore.QCoreApplication(sys.argv)
    main_socket = PhCliente()
    state_timer = QtCore.QTimer()
    state_timer.setInterval(1000)
    state_timer.timeout.connect(main_socket.get_sstate)
    state_timer.start()
    main_socket.connectToHost(IP_NUMBER, PORT)
    main_socket.sendCommand(1, 1, "CUCHAROS")
    sys.exit(app.exec_())
    