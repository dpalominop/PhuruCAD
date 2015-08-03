import sys
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

PORT = 2323
SIZEOF_UINT32 = 4

class ServerDlg(QPushButton):

    def __init__(self, parent=None):
        super(ServerDlg, self).__init__(
                "&Close Server", parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.tcpServer = QTcpServer(self)               
        self.tcpServer.listen(QHostAddress("0.0.0.0"), PORT)
        self.connect(self.tcpServer, SIGNAL("newConnection()"), 
                    self.addConnection)
        self.connections = []
        self.users = {}

        self.connect(self, SIGNAL("clicked()"), self.close)
        font = self.font()
        font.setPointSize(24)
        self.setFont(font)
        self.setWindowTitle("Server")

    def auth(self,s):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_8)
        stream.writeUInt32(0)
        stream << QByteArray("AUTH") << QByteArray("<p>What's you name?</p>")
        stream.device().seek(0)
        stream.writeUInt32(reply.size() - SIZEOF_UINT32)
        s.write(reply)

    def addConnection(self):
        clientConnection = self.tcpServer.nextPendingConnection()
        clientConnection.nextBlockSize = 0
        self.connections.append(clientConnection)
        self.connect(clientConnection, SIGNAL("readyRead()"), 
                self.receiveMessage)
        self.connect(clientConnection, SIGNAL("disconnected()"), 
                self.removeConnection)
        self.connect(clientConnection, SIGNAL("error()"), 
                self.socketError)
        self.sendAuth(clientConnection)


    def receiveMessage(self):
        for s in self.connections:
            if s.bytesAvailable() > 0:
                stream = QDataStream(s)
                stream.setVersion(QDataStream.Qt_4_8)

                if s.nextBlockSize == 0:
                    if s.bytesAvailable() < SIZEOF_UINT32:
                        return
                    s.nextBlockSize = stream.readUInt32()
                if s.bytesAvailable() < s.nextBlockSize:
                    return

                action = QByteArray()
                textFromClient = QByteArray()
                stream >> action >> textFromClient
                if action == "SEND":
                    s.nextBlockSize = 0

                    self.sendMessage(textFromClient, 
                                 s.socketDescriptor())
                    s.nextBlockSize = 0
                elif action == "AUTH":
                    s.nextBlockSize = 0
                    self.authMsg(s,textFromClient)
                    s.nextBlockSize = 0

    def sendAuth(self,s):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_8)
        stream.writeUInt32(0)
        message = QByteArray("<p>Connected,please input your username</p>")
        stream << QByteArray("AUTH") << QByteArray(message)
        stream.device().seek(0)
        stream.writeUInt32(reply.size() - SIZEOF_UINT32)
        s.write(reply)

    def authMsg(self,s,text):

        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_8)
        stream.writeUInt32(0)
        if self.users.has_key(text):
            stream << QByteArray("AUTH") << QByteArray(text + " is taken,please change one.")
        else:
            self.users[text] = s
            stream << QByteArray("CHAT") << QByteArray(text + ",Great,now you can chat!")
        stream.device().seek(0)
        stream.writeUInt32(reply.size() - SIZEOF_UINT32)
        s.write(reply)

    def sendMessage(self, text, socketId):
        now = datetime.datetime.now()
        for user in self.users:
            if self.users[user].socketDescriptor() == socketId:
                sender = user
                break
        for user in self.users:
            #if self.users[user].socketDescriptor() == socketId:
                #message = "<p>"+str(now.strftime("%Y-%m-%d %H:%M:%S")) + "</p>" +  "<font color=red>You</font> > {}".format(text)
            #else:
                #message = "<p>"+str(now.strftime("%Y-%m-%d %H:%M:%S")) + "</p>" + "<font color=blue>" + sender + "</font>" +" > {}".format(text)
            message = text
            print "message:", message
            reply = QByteArray()
            stream = QDataStream(reply, QIODevice.WriteOnly)
            stream.setVersion(QDataStream.Qt_4_8)
            stream.writeUInt32(0)
            stream << QByteArray("CHAT") << QByteArray(message)
            print "QByteArray(message):", QByteArray(message).size()
            print "QByteArray(CHAT)", QByteArray("CHAT").size()
            stream.device().seek(0)
            stream.writeUInt32(reply.size() - SIZEOF_UINT32)
            self.users[user].write(reply)

    def removeConnection(self):
        pass

    def socketError(self):
        pass


app = QApplication(sys.argv)
form = ServerDlg()
form.show()
form.move(0, 0)
app.exec_()