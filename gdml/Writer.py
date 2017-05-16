from xml.dom import minidom as _minidom
from xml.dom import getDOMImplementation

class Writer :
    def __init__(self, prepend = 'PREPEND') :
        self.prepend = prepend

        self.imp = getDOMImplementation()
        self.doc = self.imp.createDocument(None,"gdml",None)
        self.top = self.doc.documentElement
        self.top.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
        self.top.setAttribute('xsi:noNamespaceSchemaLocation',
                              'http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd')
        
        self.defines   = self.top.appendChild(self.doc.createElement('define'))
        self.materials = self.top.appendChild(self.doc.createElement('materials'))
        self.solids    = self.top.appendChild(self.doc.createElement('solids'))
        self.structure = self.top.appendChild(self.doc.createElement('structure'))
        self.setup     = self.top.appendChild(self.doc.createElement('setup'))
        
        self.defineList        = []
        self.materialList      = []
        self.solidList         = []
        self.logicalVolumeList = []
        self.physicalVolumeList= []

    def addDetector(self, registry) : 
        # loop over defines 
        for define in registry.defineDict :
            pass

        # loop over materials 

        # loop over solids 
        for solidId in registry.solidDict.keys() :
            solid = registry.solidDict[solidId]
            solid.gdmlWrite(self,self.prepend)

        # loop over logical volumes 
        for logicalName in registry.logicalVolumeList  :
            logical = registry.logicalVolumeDict[logicalName]
            logical.gdmlWrite(self,self.prepend)

        self.setup.setAttribute("name","Default")
        self.setup.setAttribute("version","1.0")
        we = self.doc.createElement("world")
        we.setAttribute("ref",self.prepend+'_'+registry.worldName+"_lv")
        self.setup.appendChild(we)

    def write(self, filename) : 
        self.filename = filename

        f = open(filename,'w')
        xmlString = self.doc.toprettyxml()
        f.write(xmlString)
        f.close()

    def writeGmadTester(self, filenameGmad):
        self.filenameGmad = filenameGmad

    def checkDefineName(self, defineName) :
        pass
        
    def checkMaterialName(self, materialName) : 
        pass
    
    def checkSolidName(self, solidName) :
        pass

    def checkLogicalVolumeName(self, logicalVolumeName) :
        pass

    def checkPhysicalVolumeName(Self, physicalVolumeName) :
        pass
