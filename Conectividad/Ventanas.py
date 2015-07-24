'''
Created on 23/7/2015

@author: Daniel Palomino
@contact: dpalomino@phuru.pe
'''

from PyQt4 import QtGui, QtCore
import Part, FreeCAD
from FreeCAD import Base

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Mi Ventana')
        
        self.lengthLabel = QtGui.QLabel("Length: ", self)
        self.lengthLabel.move(50,15)
        
        self.length = QtGui.QLineEdit(self)
        self.length.move(100,15)
        
        self.widthLabel = QtGui.QLabel("Width: ", self)
        self.widthLabel.move(50,50)
        
        self.width = QtGui.QLineEdit(self)
        self.width.move(100,50)
        
        self.heightLabel = QtGui.QLabel("Height: ", self)
        self.heightLabel.move(50,85)
        
        self.height = QtGui.QLineEdit(self)
        self.height.move(100,85)
        
        self.centered = QtGui.QCheckBox("Center on XY: ", self)
        self.centered.move(80,115)
        
        self.centerBox = False
        
        self.centered.stateChanged.connect(self.changeState)
        
        self.okButton = QtGui.QPushButton("Create Box", self)
        self.okButton.move(160,150)
        self.show()
        
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("pressed()"), self.box)
        
    def changeState(self, state):
        console = FreeCAD.Console
        
        if state == QtCore.Qt.Checked:
            console.PrintMessage("Box will be centered\n")
            self.centerBox = True
        else:
            self.centerBox = False
            
    def box(self):
        l = float(self.length.text())
        w = float(self.width.text())
        h = float(self.height.text())

        if self.centerBox == True:
            box = Part.makeBox(l, w, h)
            box.translate(Base.Vector(-1/2, -w/2, 0))
        else:
            box =  Part.makeBox(l,w,h)
            
        Part.show(box)
