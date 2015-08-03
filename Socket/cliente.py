import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
import string

PORTS = (9998, 9999)
PORT = 2323
SIZEOF_UINT32 = 4
IP_NUMBER = "192.168.4.1"
#IP_NUMBER = "localhost"

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Ititialize socket
        self.socket = QTcpSocket()

        # Initialize data IO variables
        self.nextBlockSize = 0
        self.request = None
        self.firstTime = True

        # Create widgets/layout
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit("Enter text here, dummy")
        self.lineedit.selectAll()
        self.connectButton = QPushButton("Connect")
        self.connectButton.setEnabled(True)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        layout.addWidget(self.connectButton)
        self.setLayout(layout)
        self.lineedit.setFocus()

        # Signals and slots for line edit and connect button
        self.lineedit.returnPressed.connect(self.issueRequest)
        self.connectButton.clicked.connect(self.connectToServer)

        self.setWindowTitle("Client")
        # Signals and slots for networking
        self.socket.readyRead.connect(self.readFromServer)
        self.socket.disconnected.connect(self.serverHasStopped)
        self.connect(self.socket,SIGNAL("error(QAbstractSocket::SocketError)"),self.serverHasError)

    # Update GUI
    def updateUi(self, text):
        self.browser.append(QString(text))

    # Create connection to server
    def connectToServer(self):
        self.connectButton.setEnabled(False)
        self.socket.connectToHost(IP_NUMBER, PORT)

    def issueRequest(self):
        self.request = QByteArray()
        stream = QDataStream(self.request, QIODevice.WriteOnly)
        stream.setVersion(QDataStream.Qt_4_8)
        stream.writeUInt32(0)
        if self.firstTime:
            stream << QByteArray("AUTH") << QByteArray(str("%s" % self.lineedit.text()))
            self.firstTime = False
        else:
            stream << QByteArray("SEND") << QByteArray(str("%s" % self.lineedit.text()))
            
        stream.device().seek(0)
        stream.writeUInt32(self.request.size() - SIZEOF_UINT32)
        print "mensaje: ", self.request
        self.socket.write(self.request)
        self.nextBlockSize = 0
        self.request = None
        self.lineedit.setText("")

    def readFromServer(self):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_4_8)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT32:
                    print "break 1"
                    break
                self.nextBlockSize = stream.readUInt32()
                
            if self.socket.bytesAvailable() < self.nextBlockSize:
                print "break 2"
                #break
            
            print "self.nextBlockSize: ", self.nextBlockSize
            print "self.socket.bytesAvailable(): ", self.socket.bytesAvailable()
            
            #action = QByteArray()
            #textFromServer = QByteArray()
            #stream >> action >> textFromServer
            print "self.socket.readAll()", self.socket.readAll()
            #print "tamano: ", (action.size() +textFromServer.size()) 
            #if action == "CHAT":
            #    self.updateUi(textFromServer)
            #elif action =="AUTH":
            #    self.updateUi(textFromServer)
            #    self.firstTime = True
            #else:
                #print "pinta todo"
            #    self.updateUi(textFromServer)
            #    print textFromServer
            #print "QByteArray(SEND).size()",QByteArray("SEND").size()
                
            self.nextBlockSize = 0

    def serverHasStopped(self):
        self.socket.close()
        self.connectButton.setEnabled(True)

    def serverHasError(self):
        self.updateUi("Error: {}".format(
                self.socket.errorString()))
        self.socket.close()
        self.connectButton.setEnabled(True)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()