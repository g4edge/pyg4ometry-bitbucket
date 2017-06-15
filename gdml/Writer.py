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
        for solidId in registry.solidDict.keys():
            solid = registry.solidDict[solidId]
            self.writeSolid(solid)

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

    def writeSolid(self, solid):
        """
        Dispatch to correct member function based on type string in SolidBase.
        """
        try:
            func = getattr(self, 'write'+solid.type) # get the member function
            func(solid) # call it with the solid instance as an argument
        except AttributeError:
            raise ValueError("No such solid "+solid.type)

    def writeBox(self, instance):
        oe = self.doc.createElement('box')
        oe.setAttribute('name', self.prepend+'_'+instance.name)
        oe.setAttribute('lunit','mm')
        oe.setAttribute('x','2*'+str(instance.pX))
        oe.setAttribute('y','2*'+str(instance.pY))
        oe.setAttribute('z','2*'+str(instance.pZ))
        self.solids.appendChild(oe)

    def writeCons(self, instance):
        oe = self.doc.createElement('cons')
        oe.setAttribute('name', self.prepend + '_' + instance.name)
        oe.setAttribute('ax', str(instance.pRmin))
        oe.setAttribute('ay', str(instance.pRmax))
        oe.setAttribute('az', str(instance.pDPhi))
        self.solids.appendChild(oe)

    def writeCutTubs(self, instance):
        pass

    def writeEllipsoid(self, instance):
        pass

    def writeEllipticalCone(self, instance):
        pass

    def writeEllipticalTube(self, instance):
        pass

    def writeExtrudedSolid(self, instance):
        pass

    def writeHype(self, instance):
        pass

    def writeIntersection(self, instance):
        pass

    def writeOpticalSurface(self, instance):
        pass

    def writeOrb(self, instance):
        pass

    def writePara(self, instance):
        pass

    def writeParaboloid(self, instance):
        pass
    
    def writePolycone(self, instance):
        pass

    def writePolyhedra(self, instance):
        pass

    def writeSphere(self, instance):
        pass

    def writeSubtraction(self, instance):
        pass

    def writeTet(self, instance):
        pass

    def writeTorus(self, instance):
        pass

    def writeTrap(self, instance):
        pass

    def writeTrd(self, instance):
        pass

    def writeTubs(self, instance):
        pass

    def writeTwistedBox(self, instance):
        pass

    def writeTwistedTrap(self, instance):
        pass

    def writeUnion(self, instance):
        pass
