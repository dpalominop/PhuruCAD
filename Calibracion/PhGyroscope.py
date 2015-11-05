'''
Created on 28/9/2015

@author: dpalominop
'''
        
from __future__ import division # allows floating point division from integers
import FreeCAD, Part
from FreeCAD import Base
from wx import Height

class PhGyroscope:
    def __init__(self, obj):
        ''' Add the properties: Radius, Eccentricity, Height, Segments (see Property View) '''
        #obj.addProperty("App::PropertyLength","Radius","Gyroscope","Base radius").Radius=60.0
        #obj.addProperty("App::PropertyLength","Eccentricity","Gyroscope","Rotor eccentricity").Eccentricity=12.0
        obj.addProperty("App::PropertyLength","Height","Gyroscope","Height of the block").Height=10.0
        #obj.addProperty("App::PropertyLength","Segments","Gyroscope","Number of the line segments").Segments=72
        #obj.addProperty("App::PropertyLength","Twenty","Gyroscope","Twenty").Twenty=20.0
        obj.Proxy = self

    def onChanged(self, fp, prop): 
        #if prop == "Radius" or prop == "Eccentricity" or prop == "Height" or prop == "Segments": #if one of these is changed
        self.execute(fp)

    def execute(self, fp): #main part of script
        #steps=int(fp.Segments) #get value from property
        #e=fp.Eccentricity
        #r=fp.Radius
        h=fp.Height
        #halfw=r+e+20
        #halfw = int(r)+int(e)+20
        #halfh=int(r)+int(e)+20
        
        halfw = 20
        halfh = 20
        
        edge1 = Part.makeLine((-halfw,halfh,0), (halfw,halfh,0)) #lines needed to create rectangle
        edge2 = Part.makeLine((halfw,halfh,0), (halfw,-halfh,0))
        edge3 = Part.makeLine((halfw,-halfh,0), (-halfw,-halfh,0))
        edge4 = Part.makeLine((-halfw,-halfh,0), (-halfw,halfh,0))
        wire1 = Part.Wire([edge1,edge2,edge3,edge4]) #rectangle
        face1 = Part.Face(wire1) #face from rectangle
        ext=face1.extrude(Base.Vector(0,0,h)) #extrude the cut (face)
        fp.Shape = ext #result shape

def makeReferenceSystem():
    doc = FreeCAD.activeDocument()
    if doc == None:
        doc = FreeCAD.newDocument("PhGyroscope")
    gyros=doc.addObject("Part::FeaturePython","Gyroscope") #add object to document
    #gyros.Label = "Gyroscope"
    PhGyroscope(gyros)
    gyros.ViewObject.Proxy=0
    
    
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")

if __name__ == "__main__": #feature will be generated after macro execution
    makeReferenceSystem()
    import Draft
    Draft.rotate(FreeCAD.ActiveDocument.ActiveObject,45)