# -*- coding: utf-8 -*-
'''
Created on 30/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''

from PyQt4.QtCore import QTimer, pyqtSignal, QCoreApplication
from PyQt4 import QtCore
import sys
from PyQt4.QtNetwork import QTcpSocket
#import functools

MAX_WAIT_LEN  = 8
PORT = 23
IP_NUMBER = "192.168.4.1"

def encodeData(dev_id, cmd, payload):
    my_xor = chr(10)
    msg = "$PHURU$"+chr(len(payload))+chr(dev_id)+chr(cmd)+payload+my_xor
    return msg, my_xor

def decodeData(data):
    return {"CAB": data[0:7], "LEN": ord(data[7]),
             "ID": ord(data[8]), "CMD": data[9],
             "PAYLOAD": data[10:len(data)-1],
             "XOR": data[len(data)-1]}

est = {"cabecera": 0, "longitud": 1, "device": 2, "comando": 3, "payload": 4, "xor": 5}

class PhCliente(QTcpSocket):
    data_ready = pyqtSignal(unicode)
    
    def __init__(self):
        QTcpSocket.__init__(self)
        self.wait_len = ''
        self.temp = ''
        #self.setSocketOption(QTcpSocket.KeepAliveOption, QVariant(1))
        self.readyRead.connect(self.on_ready_read)
        self.connected.connect(self.on_connected)
        self.disconnected.connect(self.on_disconnect)
        self.error.connect(self.on_error)
        self.data_ready.connect(self.print_command)
        
        self.estado = est["cabecera"]

    def connectToHost(self, host, port):
        print 'connectToHost'
        self.temp = ''
        self.wait_len = ''
        QTcpSocket.abort(self)
        
        QTcpSocket.connectToHost(self, host, port)

    def close(self):
        print 'close!'
        self.disconnectFromHost()

    def send(self, data):
        self.writeData('%s' % (encodeData(data)))
    
    def on_ready_read(self):
        if self.bytesAvailable():
            self.data = str(self.readAll())
            
            print "data: ", self.data

    def print_command(self,data):
        print 'data!'

    def get_sstate(self):
        print "STATE: ", self.state()

    def on_error(self):
        print 'error', self.errorString()
        #self.close()
        #self.connectToHost(IP_NUMBER, PORT)
        #QTimer.singleShot(3000, functools.partial(self.connectToHost, IP_NUMBER, PORT))
        QtCore.QMetaObject.invokeMethod(self, 'do_reconnect',  QtCore.Qt.QueuedConnection)

    @QtCore.pyqtSlot()
    def do_reconnect(self):
        print 'Trying to reconnect'
        self.connectToHost(IP_NUMBER, PORT)

    def on_disconnect(self):
        print 'disconnected!'

    def on_connected(self):
        print 'connected!'
        
    def sendReceive(self, dev_id, cmd, payload):
        
        snd_msg, self.xor = encodeData(dev_id, cmd, payload)
        self.send(snd_msg)
        
        rcv_msg = ""
        complete = False
        while not complete:
            if self.waitForReadyRead(msecs=3000):
                self.on_ready_read()
                if len(self.data)>=7:
                    pass
            else:
                print "ERORR: TRANSFER FAILED"
                self.data = ""
        

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    main_socket = PhCliente()
    state_timer = QTimer()
    state_timer.setInterval(1000)
    state_timer.timeout.connect(main_socket.get_sstate)
    state_timer.start()
    main_socket.connectToHost(IP_NUMBER, PORT)
    sys.exit(app.exec_())
    
