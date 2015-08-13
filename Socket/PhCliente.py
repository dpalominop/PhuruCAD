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

MAX_WAIT_LEN  = 8
PORT = 2323
IP_NUMBER = "192.168.4.1"

def encodeData(dev_id, cmd, payload):
    my_xor = chr(64)
    msg = "$PHURU$"+chr(len(payload))+chr(dev_id)+chr(cmd)+payload+my_xor
    return msg, my_xor

def decodeData(data):
    return {"CAB": data[0:7], "LEN": ord(data[7]),
             "ID": ord(data[8]), "CMD": data[9],
             "PAYLOAD": data[10:len(data)-1],
             "XOR": data[len(data)-1]}

# est = {"HEADER": 0, "LENGTH": 1, "DEVICE": 2, "COMMAND": 3, "PAYLOAD": 4, "XOR": 5}

class PhCliente(QTcpSocket):
    data_ready = pyqtSignal(unicode)
    
    def __init__(self):
        QTcpSocket.__init__(self)
        self.wait_len = ''
        self.temp = ''
        #self.setSocketOption(QTcpSocket.KeepAliveOption, QVariant(1))
        #self.readyRead.connect(self.on_ready_read)
        #self.connected.connect(self.on_connected)
        self.disconnected.connect(self.on_disconnect)
        self.error.connect(self.on_error)
        self.data_ready.connect(self.print_command)

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
        self.writeData('%s' % data)
    
    def on_ready_read(self):
        if self.bytesAvailable():
            data = str(self.readAll())
            
            print "data: ", data
            
            return data
        else:
            return ""

    def print_command(self, data):
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
        
        estado = "HEADER"
        rheader = ""
        rlen = 0
        rxor = ""
        rdata = ""
        rdevice = 0
        rcmd = 0
        
        complete = False
        cont = 0
        while not complete:
            if self.waitForReadyRead(msecs=1000):
                for c in self.on_ready_read():
                    if estado == "HEADER":
                        rheader = rheader + c
                        if len(rheader)==7: 
                            if rheader=="$PHURU$":
                                estado = "LENGTH"
                            else:
                                rheader = rheader[1:]
                            
                    elif estado == "LENGTH":
                        rlen = ord(c)
                        estado = "DEVICE"
                        
                    elif estado == "DEVICE":
                        rdevice = ord(c)
                        estado = "COMMAND"
                        
                    elif estado == "COMMAND":
                        rcmd = ord(c)
                        if rlen == 2:
                            estado = "XOR"
                        else:
                            estado = "PAYLOAD"
                        
                    elif estado == "PAYLOAD":
                        rdata = rdata + c
                        if len(rdata) == (rlen-2):
                            estado = "XOR"
                            
                    elif estado == "XOR":
                        rxor = c
                        complete = True
                
            else:
                print "ERORR: TRANSFER FAILED"
                cont = cont +1
                if cont == 3:
                    print "ERROR: NONE DATA"
                    complete = True
        
        print "received: rheader, rlen, rdevice, rcmd, rdata, rxor"
        print (rheader, rlen, rdevice, rcmd, rdata, rxor)
        return (rheader, rlen, rdevice, rcmd, rdata, rxor)
        

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    main_socket = PhCliente()
    state_timer = QTimer()
    state_timer.setInterval(1000)
    state_timer.timeout.connect(main_socket.get_sstate)
    state_timer.start()
    main_socket.connectToHost(IP_NUMBER, PORT)
    main_socket.sendReceive(1, 1, "cucharos")
    sys.exit(app.exec_())
    