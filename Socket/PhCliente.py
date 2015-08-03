'''
Created on 30/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from operator import xor
import binascii

PORTS = (9998, 9999)
PORT = 2323
IP_NUMBER = "192.168.4.1"
SIZEOF_UINT32 = 4

def bin2int(b):
    return int(binascii.hexlify(b), 16)
    #return int(b,2)

def bin2string(b):
    return binascii.hexlify(b)

class PhCliente(QObject):

    def __init__(self):
        super(QObject, self).__init__()
        # Initialize socket
        self.socket = QTcpSocket()
        self.my_xor = 0
        self.lastError = QString()

        self.socket.disconnected.connect(self.serverHasStopped)
        #self.socket.connect(self.serverHasError, SIGNAL("error(QAbstractSocket::SocketError)"))
        #self.connect(self.socket,SIGNAL("error(QAbstractSocket::SocketError)"),self.serverHasError)

    # Create connection to server
    def connectToServer(self):
        self.socket.connectToHost(IP_NUMBER, PORT)
        if(self.socket.waitForConnected(1000)):
            qDebug("Connected!")

    def sendToServer(self, comando, idd):
        self.request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_2)
        
        self.my_xor = xor(idd, comando)
        stream.writeRawData("$PHURU$")
        stream.writeRawData("\0\0\0")
        stream.writeRawData(chr(idd))
        stream.writeRawData(chr(comando))
        stream.writeRawData(chr(self.my_xor))
        
        self.socket.write(self.request)

    def readFromServer(self):
        
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_4_8)

        while True:
            print "datos: "
            print stream.readRawData(1024)
        #print "data: ", self.data

    def serverHasStopped(self):
        self.socket.close()

    def serverHasError(self):
        self.lastError = QString("Error: {}".format(self.socket.errorString()))
        self.socket.close()
