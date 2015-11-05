'''
Created on 5/11/2015

@author: dpalominop
'''
from __future__ import division # allows floating point division from integers
import FreeCAD, Part
from FreeCAD import Base

class PhCube():
    pass

def makeReferenceSystem():
    doc = FreeCAD.activeDocument()
    if doc == None:
        doc = FreeCAD.newDocument("PhGyroscope")
    gyros=doc.addObject("Part::FeaturePython","Gyroscope") #add object to document
    
    gyros.ViewObject.Proxy=0
    
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")