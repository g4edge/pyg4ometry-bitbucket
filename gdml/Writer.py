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
        oe = self.doc.createElement('ellipsoid')
        oe.setAttribute('name', self.prepend + '_' + instance.name)
        oe.setAttribute('ax', str(instance.pRmin))
        oe.setAttribute('ay', str(instance.pRmax))
        oe.setAttribute('az', str(instance.pDPhi))
        self.solids.appendChild(oe)

    def writeEllipticalCone(self, instance):
        pass

    def writeEllipticalTube(self, instance):
        pass

    def writeExtrudedSolid(self, instance):
        #TBC
        oe = self.doc.createElement('extrudedsolid')
        oe.setAttribute('name', self.prepend + '_' + instance.name)
        oe.setAttribute('ax', str(instance.pRmin))
        oe.setAttribute('ay', str(instance.pRmax))
        oe.setAttribute('az', str(instance.pDPhi))
        self.solids.appendChild(oe) 

    def writeHype(self, instance):
        pass

    def writeIntersection(self, instance):
        oe  = self.doc.createElement('intersection')
        oe.setAttribute('name',self.prepend + '_' + instance.name)
        cfe = self.doc.createElement('first')
        cfe.setAttribute('ref',self.prepend + '_' + instance.obj1.name)
        self.solids.appendChild(cfe)
        
        cse = self.doc.createElement('second')
        cse.setAttribute('ref',self.prepend + '_' + instance.obj2.name)
        self.solids.appendChild(cse)

        csce = selfdoc.createElement('positionref')
        csce.setAttribute('ref',self.prepend + '_' + instance.name+'_sol2_pos')
        self.oe.appendChild(csce)
        
        csce1 = self.doc.createElement('rotationref')
        csce1.setAttribute('ref',self.prepend + '_' + instance.name + '_sol2_rot')
        self.oe.appendChild(csce1)
        
        p = self.doc.createElement('position')
        p.setAttribute('name',self.prepend + '_' + instance.name+'_sol2_pos')
        p.setAttribute('x',str(cs.tra2[1][0]))
        p.setAttribute('y',str(cs.tra2[1][1]))
        p.setAttribute('z',str(cs.tra2[1][2]))
        self.de.appendChild(p)
        
        r = self.doc.createElement('rotation')
        r.setAttribute('name',self.prepend + '_' + instance.name + '_sol2_rot')
        r.setAttribute('x', str(cs.tra2[0][0]))
        r.setAttribute('y', str(cs.tra2[0][1]))
        r.setAttribute('z', str(cs.tra2[0][2]))
        self.de.appendChild(r)

    def writeOpticalSurface(self, instance):
        pass

    def writeOrb(self, instance):
        pass

    def writePara(self, instance):
        pass

    def writeParaboloid(self, instance):
        pass
    
    def writePolycone(self, instance):
        #TBC
        oe = self.doc.createElement('polycone')
        oe.setAttribute('name', self.prepend + '_' + instance.name)

    def writePolyhedra(self, instance):
        #TBC
        oe = self.doc.createElement('polyhedra')
        oe.setAttribute('name', self.prepend + '_' + instance.name)

    def writeSphere(self, instance):
        oe = self.doc.createElement('sphere')
        oe.setAttribute('name',self.prepend+'_'+instance.name)
        oe.setAttribute('rmin',str(instance.pRmin))
        oe.setAttribute('rmax',str(instance.pRmax))
        oe.setAttribute('deltaphi',str(instance.pDPhi))
        oe.setAttribute('startphi',str(instance.pSPhi))
        oe.setAttribute('starttheta',str(instance.pSTheta))
        oe.setAttribute('deltatheta',str(instance.pDTheta))
        oe.setAttribute('aunit', 'rad')
        self.solids.appendChild(oe)

    def writeSubtraction(self, instance):
        pass

    def writeTet(self, instance):
        pass

    def writeTorus(self, instance):
        oe = self.doc.createElement('torus')
        oe.setAttribute('name', self.prepend + '_' + instance.name)
        oe.setAttribute('rmin',str(instance.pRmin))
        oe.setAttribute('rmax',str(instance.pRmax))
        oe.setAttribute('rtor',str(instance.pRtor))
        oe.setAttribute('deltaphi',str(instance.pDPhi))
        oe.setAttribute('startphi',str(instance.pSPhi))
        self.solids.appendChild(oe)

    def writeTrap(self, instance):
        pass

    def writeTrd(self, instance):
        oe = self.doc.createElement("trd")
        oe.setAttribute('name',self.prepend + '_' + instance.name)
        oe.setAttribute('x1',str(2*instance.pX1))
        oe.setAttribute('x2',str(2*instance.pX2))
        oe.setAttribute('y1',str(2*instance.pY1))
        oe.setAttribute('y2',str(2*instance.pY2))
        oe.setAttribute('z',str(2*instance.pZ))
        self.solids.appendChild(oe)

    def writeTubs(self, instance):
        oe = self.doc.createElement("tube")
        oe.setAttribute('name',self.prepend+'_'+instance.name)
        oe.setAttribute('rmin',str(instance.pRMin))
        oe.setAttribute('rmax',str(instance.pRMax))
        oe.setAttribute('z',   str(2*instance.pDz))
        oe.setAttribute('startphi',str(instance.pSPhi))
        oe.setAttribute('deltaphi',str(instance.pDPhi))
        self.solids.appendChild(oe)

    def writeTwistedBox(self, instance):
        pass

    def writeTwistedTrap(self, instance):
        pass

    def writeUnion(self, instance):
        oe  = doc.createElement('union')
        oe.setAttribute('name',self.name)
        cfe = doc.createElement('first')
        cfe.setAttribute('ref',self.obj1.name)
        oe.appendChild(cfe)
        
        cse = self.doc.createElement('second')
        cse.setAttribute('ref',self.obj2.name)
        oe.appendChild(cse)
