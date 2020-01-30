from xml.dom import minidom as _minidom
from xml.dom import getDOMImplementation
#from ..geant4.Parameter import Parameter as _Parameter
#from ..geant4.ParameterVector import ParameterVector as _ParameterVector
from ..geant4.Material import Material as _Material
from ..geant4.Material import Element as _Element
from ..geant4.Material import Isotope as _Isotope
from ..gdml.Defines import (
    Constant as _Constant,
    Quantity as _Quantity,
    Variable as _Variable,
    Position as _Position,
    Rotation as _Rotation,
    Scale as _Scale,
    Matrix as _Matrix,
    Expression as _Expression)

import pyg4ometry.geant4 as _g4

class Writer(object):
    def __init__(self, prepend = ''):
        super(Writer, self).__init__()
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

        self.materials_written = []

        self.defineList        = []
        self.materialList      = []
        self.solidList         = []
        self.logicalVolumeList = []
        self.physicalVolumeList= []

    def addDetector(self, registry) :
        self.registry = self.extractDefinesFromTesselatedSolids(registry)

        # loop over defines
        for define in registry.defineDict :
            self.writeDefine(registry.defineDict[define])

        # loop over materials
        for material in registry.materialDict:
            self.writeMaterial(material)

        # loop over solids
        for solidId in registry.solidDict.keys():
            solid = registry.solidDict[solidId]
            self.writeSolid(solid)

        # loop over logical volumes
        for logicalName in registry.logicalVolumeList  :
            print "writer", logicalName
            logical = registry.logicalVolumeDict[logicalName]
            self.writeLogicalVolume(logical)
            self.writeMaterial(logical.material)

        self.setup.setAttribute("name","Default")
        self.setup.setAttribute("version","1.0")
        we = self.doc.createElement("world")
        we.setAttribute("ref",self.prepend + registry.worldName+"_lv")
        self.setup.appendChild(we)

    def write(self, filename) :
        self.filename = filename

        f = open(filename,'w')
        xmlString = self.doc.toprettyxml()
        f.write(xmlString)
        f.close()

    def extractDefinesFromTesselatedSolids(self, registry):
        #Tesselated solids require their veritces to be declared in the defines.
        #Loop over all tesselated solids and populate the defines dictionary.
        for solidId in registry.solidDict.keys():
            solid = registry.solidDict[solidId]
            if solid.type == "TesselatedSolid":
                name = solid.name
                i = 0
                for vertid in range(len(solid.unique_vertices)):
                    vertex = solid.unique_vertices[vertid]
                    defname   = "V_{}_{}".format(name,vertid)
                    defvertex = _ParameterVector(defname, list(vertex))
                    registry.defineDict[defname] = defvertex
                    i=i+1

        return registry

    def writeGmadTester(self, filenameGmad, writeDefaultLattice=False, zLength=None, preprocessGDML=True):
        self.filenameGmad = filenameGmad

        if writeDefaultLattice:
            self.writeDefaultLattice()

        s = 'e1: element, geometry="gdml:'
        s += str(self.filename)
        if self.registry.parameterDict.has_key("GDML_Size_position_z"):
            s += '", l=' + str(self.registry.parameterDict['GDML_Size_position_z'].value) + '*mm;\n'
        else:
            # be super tolerant incase the meshing fails - still write out
            try:
                ext = _g4.mesh_extent(_g4.registry.worldVolume.mesh)
                dz = ext[1][2] - ext[0][2]
                s += '", l=' + str(dz) + '*mm;\n'
            except TypeError:
                s += '", l=20*m;\n'
        s += 'l1: line = (e1);\n'
        s += 'use,period=l1;\n'
        s += 'sample,all;\n'
        s += 'beam, particle="e-",\n'
        s += 'energy=250.0*GeV;\n'
        if not preprocessGDML:
            s += "option, preprocessGDML=0;"
        f = open(self.filenameGmad, 'w')
        f.write(s)
        f.close()

    def writeDefaultLattice(self, filename='lattice.gmad'):
        s =  'l1: line = (e1);\n'
        s += 'use,period=l1;\n'
        s += 'sample, all;\n'
        s += 'beam, particle="e-",\n'
        s += 'energy=250.0*GeV;\n'
        f = open(filename, 'w')
        f.write(s)
        f.close()

    def checkDefineName(self, defineName) :
        pass

    def checkMaterialName(self, materialName) :
        pass

    def checkSolidName(self, solidName) :
        pass

    def checkLogicalVolumeName(self, logicalVolumeName) :
        pass

    def checkPhysicalVolumeName(self, physicalVolumeName):
        pass

    def writeLogicalVolume(self, lv):
        we = self.doc.createElement('volume')
        we.setAttribute('name', "{}{}_lv".format(self.prepend, lv.name, '_lv'))
        mr = self.doc.createElement('materialref')
        if lv.material.name.find("G4") != -1 :
            mr.setAttribute('ref', lv.material.name)
        else :
            mr.setAttribute('ref', "{}{}".format(self.prepend, lv.material.name))
        we.appendChild(mr)

        sr = self.doc.createElement('solidref')
        sr.setAttribute('ref', "{}{}".format(self.prepend, lv.solid.name))
        we.appendChild(sr)

        for dv in lv.daughterVolumes :
            dve = self.writePhysicalVolume(dv)
            we.appendChild(dve)

        self.structure.appendChild(we)

    def writePhysicalVolume(self, pv):
        pvol = self.doc.createElement('physvol')
        pvol.setAttribute('name',"{}{}_pv".format(self.prepend, pv.name))
        vr = self.doc.createElement('volumeref')
        vr.setAttribute('ref',"{}{}_lv".format(self.prepend, pv.logicalVolume.name))
        pvol.appendChild(vr)

        # phys vol translation
        tlatee = self.doc.createElement('positionref')
        tlatee.setAttribute('ref', str(pv.position.name))
        pvol.appendChild(tlatee)

        # phys vol rotation
        rote = self.doc.createElement('rotationref')
        rote.setAttribute('ref', str(pv.rotation.name))
        pvol.appendChild(rote)

        # phys vol scale
        tscae = self.doc.createElement('scaleref')
        tscae.setAttribute('ref', str(pv.rotation.name))
        pvol.appendChild(tscae)

        return pvol

    def writeDefine(self, define):
        if isinstance(define, _Constant):
            oe = self.doc.createElement('constant')
            oe.setAttribute('name', define.name)
            oe.setAttribute('value', str(define.expr.expression))
        elif isinstance(define, _Quantity):
            oe = self.doc.createElement('quantity')
            oe.setAttribute('name', define.name)
            oe.setAttribute('value', str(define.expr.expression))
            oe.setAttribute('type', str(define.type))
            oe.setAttribute('unit', str(define.unit))
        elif isinstance(define, _Variable):
            oe = self.doc.createElement('variable')
            oe.setAttribute('name', define.name)
            oe.setAttribute('value', str(define.expr.expression))
        elif isinstance(define, _Position):
            oe = self.doc.createElement('position')
            oe.setAttribute('name', define.name)
            oe.setAttribute('x', str(define.x.expression))
            oe.setAttribute('y', str(define.y.expression))
            oe.setAttribute('z', str(define.z.expression))
            #oe.setAttribute('unit', str(define.unit)) #TODO: Units not handled by position right now
        elif isinstance(define, _Rotation):
            oe = self.doc.createElement('rotation')
            oe.setAttribute('name', define.name)
            oe.setAttribute('x', str(define.x.expression))
            oe.setAttribute('y', str(define.y.expression))
            oe.setAttribute('z', str(define.z.expression))
            #oe.setAttribute('unit', str(define.unit)) #TODO: Units not handled by position right now
        elif isinstance(define, _Scale):
            oe = self.doc.createElement('scale')
            oe.setAttribute('name', define.name)
            oe.setAttribute('x', str(define.x.expression))
            oe.setAttribute('y', str(define.y.expression))
            oe.setAttribute('z', str(define.z.expression))
        elif isinstance(define, _Matrix):
            oe = self.doc.createElement('matrix')
            oe.setAttribute('name', define.name)
            oe.setAttribute('coldim', str(define.coldim))
            oe.setAttribute('values', " ".join([val.expression for val in values]))
        elif isinstance(define, _Expression):
            return # Only write out named defines
        else:
            raise Exception("Urecognised define type: {}".format(type(define)))

        self.defines.appendChild(oe)

    def writeParameter(self, param):
        if isinstance(param,_Parameter) :
            oe = self.doc.createElement('variable')
            oe.setAttribute('name', param.name)
            if param.name != param.expr :
                oe.setAttribute('value',param.expr)
            else :
                oe.setAttribute('value',str(float(param)))
            self.defines.appendChild(oe)
        elif isinstance(param,_ParameterVector) :
            oe = self.doc.createElement('position')
            oe.setAttribute('name', param.name)
            oe.setAttribute('unit','mm')
            oe.setAttribute('x',str(param[0]))
            oe.setAttribute('y',str(param[1]))
            oe.setAttribute('z',str(param[2]))
            self.defines.appendChild(oe)

    def writeMaterial(self, material):
        if isinstance(material, _Material) :
            oe = self.doc.createElement('material')
            oe.setAttribute('name', material.name)
            de = self.doc.createElement('D')
            de.setAttribute('value', str(material.density))
            oe.appendChild(de)

            if material.type == 'simple':
                oe.setAttribute('Z', material.atomic_number)
                se  = self.doc.createElement('atom')
                se.setAttribute('value', str(material.atomic_weight))
                oe.appendChild(se)
            elif material.type == 'composite':
                for comp_info in  material.components:
                    name = comp_info[0].name
                    frac_type = comp_info[2]
                    self.writeMaterial(comp_info[0])
                    if frac_type == "massfraction":
                        se = self.doc.createElement('fraction')
                        se.setAttribute('ref', name)
                        se.setAttribute('n', str(comp_info[1]))
                        oe.appendChild(se)
                    if frac_type == "natoms":
                        se = self.doc.createElement('composite')
                        se.setAttribute('ref', name)
                        se.setAttribute('n', str(comp_info[1]))
                        oe.appendChild(se)
            elif material.type == 'nist' or material.type == 'arbitrary':
                # No need to add defines for NIST compounds or
                # materials which are simply names.
                return

        elif isinstance(material, _Element):
            oe = self.doc.createElement('element')
            oe.setAttribute('name', material.name)
            oe.setAttribute('formula', material.symbol)
            if material.type == 'simple':
                oe.setAttribute('Z', str(material.Z))
                se = self.doc.createElement('atom')
                se.setAttribute('value', str(material.A))
                oe.appendChild(se)
            elif material.type == 'composite':
                for comp_info in material.components:
                    name = comp_info[0].name
                    self.writeMaterial(comp_info[0])
                    se = self.doc.createElement('fraction')
                    se.setAttribute('ref', name)
                    se.setAttribute('n', str(comp_info[1]))
                    oe.appendChild(se)

        elif isinstance(material, _Isotope) :
            oe = self.doc.createElement('isotope')
            oe.setAttribute('name', material.name)
            oe.setAttribute('Z', str(material.Z))
            oe.setAttribute('N', str(material.N))
            se = self.doc.createElement('atom')
            se.setAttribute('type', 'A')
            se.setAttribute('value', str(material.a))
            oe.appendChild(se)

        if material.name not in self.materials_written:
            self.materials_written.append(material.name)
            self.materials.appendChild(oe)

    def writeSolid(self, solid):
        """
        Dispatch to correct member function based on type string in SolidBase.
        """
        try:
            func = getattr(self, 'write'+solid.type) # get the member function
            func(solid) # call it with the solid instance as an argument
        except AttributeError:
            print solid.name
            raise ValueError("No such solid "+solid.type)

    def writeBox(self, instance):
        oe = self.doc.createElement('box')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('lunit','mm')
        oe.setAttribute('x','2*'+str(instance.pX.expr.expression))
        oe.setAttribute('y','2*'+str(instance.pY.expr.expression))
        oe.setAttribute('z','2*'+str(instance.pZ.expr.expression))
        self.solids.appendChild(oe)

    def writeCons(self, instance):
        oe = self.doc.createElement('cone')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('rmin1', str(instance.pRmin1.expr))
        oe.setAttribute('rmax1', str(instance.pRmax1.expr.expression))
        oe.setAttribute('rmin2', str(instance.pRmin2.expr.expression))
        oe.setAttribute('rmax2', str(instance.pRmax2.expr.expression))
        oe.setAttribute('z', str(instance.pDz.expr.expression))
        oe.setAttribute('startphi', str(instance.pSPhi.expr.expression))
        oe.setAttribute('deltaphi', str(instance.pDPhi.expr.expression))
        self.solids.appendChild(oe)

    def writeCutTubs(self, instance):
        oe = self.doc.createElement('cutTube')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('z', '2*'+str(instance.pDz.expr.expression))
        oe.setAttribute('rmin', str(instance.pRMin.expr.expression))
        oe.setAttribute('rmax', str(instance.pRMax.expr.expression))
        oe.setAttribute('startphi', str(instance.pSPhi.expr.expression))
        oe.setAttribute('deltaphi', str(instance.pDPhi.expr.expression))
        oe.setAttribute('lowX', str(instance.pLowNorm[0].expr.expression))
        oe.setAttribute('lowY', str(instance.pLowNorm[1].expr.expression))
        oe.setAttribute('lowZ', str(instance.pLowNorm[2].expr.expression))
        oe.setAttribute('highX', str(instance.pHighNorm[0].expr.expression))
        oe.setAttribute('highY', str(instance.pHighNorm[1].expr.expression))
        oe.setAttribute('highZ', str(instance.pHighNorm[2].expr.expression))
        self.solids.appendChild(oe)


    def writeEllipsoid(self, instance):
        oe = self.doc.createElement('ellipsoid')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('ax', str(instance.pxSemiAxis.expr.expression))
        oe.setAttribute('by', str(instance.pySemiAxis.expr.expression))
        oe.setAttribute('cz', str(instance.pzSemiAxis.expr.expression))
        oe.setAttribute('zcut1', str(instance.pzBottomCut.expr.expression))
        oe.setAttribute('zcut2', str(instance.pzTopCut.expr.expression))
        self.solids.appendChild(oe)

    def writeEllipticalCone(self, instance):
        oe = self.doc.createElement('elcone')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('dx', str(instance.pxSemiAxis.expr.expression))
        oe.setAttribute('dy', str(instance.pySemiAxis.expr.expression))
        oe.setAttribute('zmax', str(instance.zMax.expr.expression))
        oe.setAttribute('zcut', str(instance.pzTopCut.expr.expression))
        self.solids.appendChild(oe)

    def writeEllipticalTube(self, instance):
        oe = self.doc.createElement('eltube')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('dx', '2*'+str(instance.pDx.expr.expression))
        oe.setAttribute('dy', '2*'+str(instance.pDy.expr.expression))
        oe.setAttribute('dz', '2*'+str(instance.pDz.expr.expression))
        self.solids.appendChild(oe)

    def createTwoDimVertex(self, x, y):
        td = self.doc.createElement('twoDimVertex')
        td.setAttribute('x', str(x.expr.expression))
        td.setAttribute('y', str(y.expr.expression))
        return td

    def createSection(self, zOrder, zPosition, xOffset, yOffset, scalingFactor):
        s = self.doc.createElement('section')
        s.setAttribute('zOrder', str(zOrder.expr.expression))
        s.setAttribute('zPosition', str(zPosition.expr.expression))
        s.setAttribute('xOffset', str(xOffset.expr.expression))
        s.setAttribute('yOffset', str(yOffset.expr.expression))
        s.setAttribute('scalingFactor', str(scalingFactor.expr.expression))
        return s

    def writeExtrudedSolid(self, instance):
        oe = self.doc.createElement('xtru')
        oe.setAttribute('name', self.prepend + instance.name)

        for vertex in instance.vertices:
            v = self.createTwoDimVertex(vertex[0], vertex[1])
            oe.appendChild(v)

        i = instance
        n = 0
        for z,x,y,s in zip(i.zpos,i.x_offs, i.y_offs, i.scale):
            s = self.createSection(n, z, x, y, s)
            n += 1
            oe.appendChild(s)

        self.solids.appendChild(oe)

    def createrzPoint(self, r, z):
        rz = self.doc.createElement('rzpoint')
        rz.setAttribute('r', str(r.expr.expression))
        rz.setAttribute('z', str(z.expr.expression))
        return rz

    def writeGenericPolycone(self, instance):
        oe = self.doc.createElement('genericPolycone')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('startphi', str(instance.pSPhi.expr.expression))
        oe.setAttribute('deltaphi', str(instance.pDPhi.expr.expression))

        for r,z in zip(instance.pR, instance.pZ):
            p = self.createrzPoint(r, z)
            oe.appendChild(p)

        self.solids.appendChild(oe)

    def createTriangularFacet(self, vertex1, vertex2, vertex3):
        tf = self.doc.createElement('triangular')
        tf.setAttribute('vertex1', str(vertex1))
        tf.setAttribute('vertex2', str(vertex2))
        tf.setAttribute('vertex3', str(vertex3))
        tf.setAttribute('type', 'ABSOLUTE')
        return tf

    def writeTesselatedSolid(self, instance):
        oe = self.doc.createElement('tessellated')
        name     = instance.name
        oe.setAttribute('name', self.prepend + name)

        i = 0
        for indexed_faced in instance.indexed_facet_list:
            vertices = []
            for vertex_id in indexed_faced[0]: #Always 3 elements in a facet
                vertices.append("V_{}_{}".format(name,vertex_id))
                i = i+1
            oe.appendChild(self.createTriangularFacet(*vertices))
        self.solids.appendChild(oe)

    def writeHype(self, instance):
        oe = self.doc.createElement('hype')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('rmin', str(instance.innerRadius.expr.expression))
        oe.setAttribute('rmax', str(instance.outerRadius.expr.expression))
        oe.setAttribute('z', '2*'+str(instance.halfLenZ.expr.expression))
        oe.setAttribute('inst', str(instance.innerStereo.expr.expression))
        oe.setAttribute('outst', str(instance.outerStereo.expr.expression))
        self.solids.appendChild(oe)

    def writeIntersection(self, instance):
        oe  = self.doc.createElement('intersection')
        oe.setAttribute('name',self.prepend + instance.name)

        cfe = self.doc.createElement('first')
        cfe.setAttribute('ref',self.prepend + instance.obj1name)
        oe.appendChild(cfe)

        cse = self.doc.createElement('second')
        cse.setAttribute('ref',self.prepend + instance.obj2name)
        oe.appendChild(cse)

        p = self.doc.createElement('position')
        p.setAttribute('name',self.prepend + instance.name+'_'+'position')
        p.setAttribute('x',str(instance.tra2[1][0].expr.expression))
        p.setAttribute('y',str(instance.tra2[1][1].expr.expression))
        p.setAttribute('z',str(instance.tra2[1][2].expr.expression))
        self.defines.appendChild(p)

        r = self.doc.createElement('rotation')
        r.setAttribute('name',self.prepend + instance.name+'_'+'rotation')
        r.setAttribute('x', str(instance.tra2[0][0].expr.expression))
        r.setAttribute('y', str(instance.tra2[0][1].expr.expression))
        r.setAttribute('z', str(instance.tra2[0][2].expr.expression))
        self.defines.appendChild(r)


        csce = self.doc.createElement('positionref')
        csce.setAttribute('ref',self.prepend + instance.name+'_'+'position')
        oe.appendChild(csce)

        csce1 = self.doc.createElement('rotationref')
        csce1.setAttribute('ref',self.prepend + instance.name+'_'+'rotation')
        oe.appendChild(csce1)


        self.solids.appendChild(oe)

    def writeOpticalSurface(self, instance):
        pass

    def writeOrb(self, instance):
        oe = self.doc.createElement('orb')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('r', str(instance.pRMax.expr.expression))
        self.solids.appendChild(oe)

    def writePara(self, instance):
        oe = self.doc.createElement('para')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('x', str(instance.pX.expr.expression))
        oe.setAttribute('y', str(instance.pY.expr.expression))
        oe.setAttribute('z', str(instance.pZ.expr.expression))
        oe.setAttribute('alpha', str(instance.pAlpha.expr.expression))
        oe.setAttribute('theta', str(instance.pTheta.expr.expression))
        oe.setAttribute('phi', str(instance.pPhi.expr.expression))
        self.solids.appendChild(oe)

    def writeParaboloid(self, instance):
        oe = self.doc.createElement('paraboloid')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('rlo', str(instance.pR1.expr.expression))
        oe.setAttribute('rhi', str(instance.pR2.expr.expression))
        oe.setAttribute('dz', str(instance.pDz.expr.expression))
        self.solids.appendChild(oe)

    def createzPlane(self, rInner, rOuter, zplane):
        d = self.doc.createElement('zplane')
        d.setAttribute('rmin',str(rInner.expr.expression))
        d.setAttribute('rmax', str(rOuter.expr.expression))
        d.setAttribute('z', str(zplane.expr.expression))
        return d

    def writePolycone(self, instance):
        oe = self.doc.createElement('polycone')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('startphi',str(instance.pSPhi.expr.expression))
        oe.setAttribute('deltaphi',str(instance.pDPhi.expr.expression))

        i = instance
        for w,x,y in zip(i.pRMin, i.pRMax, i.pZpl):
            d = self.createzPlane(w,x,y)
            oe.appendChild(d)

        self.solids.appendChild(oe)

    def writePolyhedra(self, instance):
        oe = self.doc.createElement('polyhedra')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('startphi',str(instance.phiStart.expr.expression))
        oe.setAttribute('deltaphi',str(instance.phiTotal.expr.expression))
        oe.setAttribute('numsides',str(instance.numSide.expr.expression))

        i = instance
        for w,x,y in zip(i.rInner, i.rOuter, i.zPlane):
            d = self.createzPlane(w,x,y)
            oe.appendChild(d)

        self.solids.appendChild(oe)

    def writeSphere(self, instance):
        oe = self.doc.createElement('sphere')
        oe.setAttribute('name',self.prepend + instance.name)
        oe.setAttribute('rmin',str(instance.pRmin.expr.expression))
        oe.setAttribute('rmax',str(instance.pRmax.expr.expression))
        oe.setAttribute('deltaphi',str(instance.pDPhi.expr.expression))
        oe.setAttribute('startphi',str(instance.pSPhi.expr.expression))
        oe.setAttribute('starttheta',str(instance.pSTheta.expr.expression))
        oe.setAttribute('deltatheta',str(instance.pDTheta.expr.expression))
        oe.setAttribute('aunit', 'rad')
        self.solids.appendChild(oe)


    def writeSubtraction(self, instance):
        oe  = self.doc.createElement('subtraction')
        oe.setAttribute('name',self.prepend + instance.name)

        cfe = self.doc.createElement('first')
        cfe.setAttribute('ref',self.prepend + instance.obj1name)
        oe.appendChild(cfe)

        cse = self.doc.createElement('second')
        cse.setAttribute('ref',self.prepend + instance.obj2name)
        oe.appendChild(cse)

        p = self.doc.createElement('position')
        p.setAttribute('name',self.prepend + instance.name+'_'+'position')
        p.setAttribute('x',str(instance.tra2[1][0].expression))
        p.setAttribute('y',str(instance.tra2[1][1].expression))
        p.setAttribute('z',str(instance.tra2[1][2].expression))
        self.defines.appendChild(p)

        r = self.doc.createElement('rotation')
        r.setAttribute('name',self.prepend + instance.name+'_'+'rotation')
        r.setAttribute('x', str(instance.tra2[0][0].expression))
        r.setAttribute('y', str(instance.tra2[0][1].expression))
        r.setAttribute('z', str(instance.tra2[0][2].expression))
        self.defines.appendChild(r)


        csce = self.doc.createElement('positionref')
        csce.setAttribute('ref',self.prepend + instance.name+'_'+'position')
        oe.appendChild(csce)

        csce1 = self.doc.createElement('rotationref')
        csce1.setAttribute('ref',self.prepend + instance.name+'_'+'rotation')
        oe.appendChild(csce1)


        self.solids.appendChild(oe)


    def createPosition(self,name, x, y, z):
        p = self.doc.createElement('position')
        p.setAttribute('name',str(name))
        p.setAttribute('x', str(x))
        p.setAttribute('y', str(y))
        p.setAttribute('z', str(z))
        return p

    def writeTet(self, instance):
        j = instance
        oe = self.doc.createElement('tet')
        uniqueName = self.prepend + instance.name
        oe.setAttribute('name', uniqueName)
        v1 = self.createPosition(uniqueName + '_v1', j.anchor[0], j.anchor[1], j.anchor[2])
        self.defines.appendChild(v1)
        v2 = self.createPosition(uniqueName + '_v2', j.p2[0], j.p2[1], j.p2[2])
        self.defines.appendChild(v2)
        v3 = self.createPosition(uniqueName + '_v3', j.p3[0], j.p3[1], j.p3[2])
        self.defines.appendChild(v3)
        v4 = self.createPosition(uniqueName + '_v4', j.p4[0], j.p4[1], j.p4[2])
        self.defines.appendChild(v4)
        oe.setAttribute('vertex1', uniqueName + '_v1')
        oe.setAttribute('vertex2', uniqueName + '_v2')
        oe.setAttribute('vertex3', uniqueName + '_v3')
        oe.setAttribute('vertex4', uniqueName + '_v4')
        self.solids.appendChild(oe)

    def writeTorus(self, instance):
        oe = self.doc.createElement('torus')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('rmin',str(instance.pRmin.expr.expression))
        oe.setAttribute('rmax',str(instance.pRmax.expr.expression))
        oe.setAttribute('rtor',str(instance.pRtor.expr.expression))
        oe.setAttribute('deltaphi',str(instance.pDPhi.expr.expression))
        oe.setAttribute('startphi',str(instance.pSPhi.expr.expression))
        self.solids.appendChild(oe)

    def writeTrap(self, instance):
        oe = self.doc.createElement('trap')
        oe.setAttribute('name', self.prepend + instance.name)
        oe.setAttribute('z','2*'+str(instance.pDz.expr.expression))
        oe.setAttribute('theta',str(instance.pTheta.expr.expression))
        oe.setAttribute('phi',str(instance.pDPhi.expr.expression))
        oe.setAttribute('y1','2*'+str(instance.pDy1.expr.expression))
        oe.setAttribute('x1','2*'+str(instance.pDx1.expr.expression))
        oe.setAttribute('x2','2*'+str(instance.pDx2.expr.expression))
        oe.setAttribute('alpha1',str(instance.pAlp1.expr.expression))
        oe.setAttribute('y2','2*'+str(instance.pDy2.expr.expression))
        oe.setAttribute('x3','2*'+str(instance.pDx3.expr.expression))
        oe.setAttribute('x4','2*'+str(instance.pDx4.expr.expression))
        oe.setAttribute('alpha2',str(instance.pAlp2.expr.expression))
        self.solids.appendChild(oe)

    def writeTrd(self, instance):
        oe = self.doc.createElement("trd")
        oe.setAttribute('name',self.prepend + instance.name)
        oe.setAttribute('x1','2*'+str(instance.pX1.expr.expression))
        oe.setAttribute('x2','2*'+str(instance.pX2.expr.expression))
        oe.setAttribute('y1','2*'+str(instance.pY1.expr.expression))
        oe.setAttribute('y2','2*'+str(instance.pY2.expr.expression))
        oe.setAttribute('z','2*'+str(instance.pZ.expr.expression))
        self.solids.appendChild(oe)

    def writeTubs(self, instance):
        oe = self.doc.createElement("tube")
        oe.setAttribute('name',self.prepend + instance.name)
        oe.setAttribute('rmin',str(instance.pRMin.expr.expression))
        oe.setAttribute('rmax',str(instance.pRMax.expr.expression))
        oe.setAttribute('z',   '2*'+str(instance.pDz.expr.expression))
        oe.setAttribute('startphi',str(instance.pSPhi.expr.expression))
        oe.setAttribute('deltaphi',str(instance.pDPhi.expr.expression))
        self.solids.appendChild(oe)

    def writeTwistedBox(self, instance):
        oe = self.doc.createElement("twistedbox")
        oe.setAttribute('name',self.prepend + instance.name)
        oe.setAttribute('PhiTwist',str(instance.twistedAngle.expr.expression))
        oe.setAttribute('x','2*'+ str(instance.pDx.expr.expression))
        oe.setAttribute('y','2*'+ str(instance.pDy.expr.expression))
        oe.setAttribute('z','2*'+ str(instance.pDz.expr.expression))
        self.solids.appendChild(oe)

    def writeTwistedTrd(self, instance):
        oe = self.doc.createElement("twistedtrd")
        oe.setAttribute('name',self.prepend + instance.name)
        oe.setAttribute('PhiTwist',str(instance.twistedAngle.expr.expression))
        oe.setAttribute('x1','2*'+ str(instance.pDx1.expr.expression))
        oe.setAttribute('x2','2*'+ str(instance.pDx2.expr.expression))
        oe.setAttribute('y1','2*'+ str(instance.pDy1.expr.expression))
        oe.setAttribute('y2','2*'+ str(instance.pDy2.expr.expression))
        oe.setAttribute('z','2*'+ str(instance.pDz.expr.expression))
        self.solids.appendChild(oe)

    def writeTwistedTrap(self, instance):
        oe = self.doc.createElement("twistedtrap")
        oe.setAttribute('name',self.prepend + instance.name)
        oe.setAttribute('PhiTwist',str(instance.twistedangle.expr.expression))
        oe.setAttribute('z','2*'+ str(instance.pDz.expr.expression))
        oe.setAttribute('Theta',str(instance.pTheta.expr.expression))
        oe.setAttribute('Phi',str(instance.pDPhi.expr.expression))
        oe.setAttribute('y1','2*'+ str(instance.pDy1.expr.expression))
        oe.setAttribute('x1','2*'+ str(instance.pDx1.expr.expression))
        oe.setAttribute('x2','2*'+ str(instance.pDx2.expr.expression))
        oe.setAttribute('y2','2*'+ str(instance.pDy2.expr.expression))
        oe.setAttribute('x3','2*'+ str(instance.pDx3.expr.expression))
        oe.setAttribute('x4','2*'+ str(instance.pDx4.expr.expression))
        oe.setAttribute('Alph',str(instance.pAlp.expr.expression))
        self.solids.appendChild(oe)

    def writeUnion(self, instance):
        oe  = self.doc.createElement('union')
        oe.setAttribute('name',self.prepend + instance.name)

        cfe = self.doc.createElement('first')
        cfe.setAttribute('ref',self.prepend + instance.obj1name)
        oe.appendChild(cfe)

        cse = self.doc.createElement('second')
        cse.setAttribute('ref',self.prepend + instance.obj2name)
        oe.appendChild(cse)

        p = self.doc.createElement('position')
        p.setAttribute('name',self.prepend + instance.name+'_'+'position')
        p.setAttribute('x',str(instance.tra2[1][0].expression))
        p.setAttribute('y',str(instance.tra2[1][1].expression))
        p.setAttribute('z',str(instance.tra2[1][2].expression))
        self.defines.appendChild(p)

        r = self.doc.createElement('rotation')
        r.setAttribute('name',self.prepend + instance.name+'_'+'rotation')
        r.setAttribute('x', str(instance.tra2[0][0].expression))
        r.setAttribute('y', str(instance.tra2[0][1].expression))
        r.setAttribute('z', str(instance.tra2[0][2].expression))
        self.defines.appendChild(r)


        csce = self.doc.createElement('positionref')
        csce.setAttribute('ref',self.prepend + instance.name+'_'+'position')
        oe.appendChild(csce)

        csce1 = self.doc.createElement('rotationref')
        csce1.setAttribute('ref',self.prepend + instance.name+'_'+'rotation')
        oe.appendChild(csce1)


        self.solids.appendChild(oe)