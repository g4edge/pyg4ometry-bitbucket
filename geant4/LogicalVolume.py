from pygeometry.geant4 import solid as _solid
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.pycsg.geom import Vector as _Vector
from matplotlib.cbook import flatten as _flatten
import numpy as _np

import sys as _sys

class LogicalVolume :

    imeshed = 0

    def __init__(self, solid, material, name, debug= False) :
        self.solid           = solid
        self.material        = material
        self.name            = name
        self.daughterVolumes = [] 
        self.mesh            = None
        self.debug           = debug
        _registry.addLogicalVolume(self)

    def __repr__(self) : 
        return 'Logical volume : '+self.name+' '+str(self.solid)+' '+str(self.material)
    
    def pycsgmesh(self) :
        # count the logical volumes meshed
        LogicalVolume.imeshed = LogicalVolume.imeshed + 1
        if self.debug :
            print 'LogiacalVolume mesh count',LogicalVolume.imeshed

        #if self.mesh :
        #    return self.mesh

        # see if the volume should be skipped
        try :
            _registry.logicalVolumeMeshSkip.index(self.name)
            if self.debug :
                print "Logical volume skipping ---------------------------------------- ",self.name
            return []
        except ValueError :
            pass

        if len(self.daughterVolumes) == 0 :
            self.mesh = [self.solid.pycsgmesh()]
            self.mesh[0].alpha     = 0.5
            self.mesh[0].wireframe = False
            self.mesh[0].colour    = [1,1,1]

        else :
            daughterMeshes = []
            for dv in self.daughterVolumes :
                dvMesh = dv.pycsgmesh() 
                daughterMeshes.append(dvMesh)
                self.mesh = [self.solid.pycsgmesh(),daughterMeshes]

            self.mesh[0].alpha     = 0.5
            self.mesh[0].wireframe = False
            self.mesh[0].colour    = [1,0,0]
            self.mesh[0].logical   = True

        if self.debug :
            print 'logical mesh', self.name
        return self.mesh

    def add(self, physicalVolume) :
        self.daughterVolumes.append(physicalVolume)

    def getSize(self):
        self.pycsgmesh();
        extent = _np.array(mesh_extent(self.mesh[1:]))

        # size and centre
        self.size = extent[1] - extent[0]
        self.centre = extent[1] - self.size/2.0

        return [self.size, self.centre]

    def setClip(self):
        [size, centre] = self.getSize()
        self.setSize(size)
        self.setCentre(centre)

    def setSize(self, size):
        # if a box
        if isinstance(self.solid,_solid.Box) :
            self.solid.pX = size[0] / 2.
            self.solid.pY = size[1] / 2.
            self.solid.pZ = size[2] / 2.
        elif isinstance(self.solid,_solid.Subtraction) :
            self.solid.obj1.pX = size[0] / 2.
            self.solid.obj1.pY = size[1] / 2.
            self.solid.obj1.pZ = size[2] / 2.

    def setCentre(self,centre):
        self.centre = centre
        for dv in self.daughterVolumes:
            dv.position = list(-_np.array(self.centre) + _np.array(dv.position))

        # Move the beam pipe if a subtraction solid
        if isinstance(self.solid, _solid.Subtraction):
            self.solid.tra2[1] = self.solid.tra2[1] - _np.array(self.centre)

    def gdmlWrite(self, gw, prepend) :
        we = gw.doc.createElement('volume')
        we.setAttribute('name',prepend+'_'+self.name+'_lv')
        mr = gw.doc.createElement('materialref')
        if self.material.find("G4") != -1 :          
            mr.setAttribute('ref',self.material)
        else :
            mr.setAttribute('ref',prepend+'_'+self.material)
        we.appendChild(mr)

        sr = gw.doc.createElement('solidref')
        sr.setAttribute('ref',prepend+'_'+self.solid.name)
        we.appendChild(sr)
        
        for dv in self.daughterVolumes : 
            dve = dv.gdmlWrite(gw,prepend)
            we.appendChild(dve)

        gw.structure.appendChild(we)

def mesh_extent(nlist) :
    '''Function to determine extent of an tree of meshes'''

    vMin = _Vector([1e50,1e50,1e50])
    vMax = _Vector([-1e50,-1e50,-1e50])

    for m in _flatten(nlist) :
        polys = m.toPolygons()
        for p in polys :
            for vert in p.vertices :
                v = vert.pos
                if v[0] < vMin[0] :
                    vMin[0] = v[0]
                if v[1] < vMin[1] :
                    vMin[1] = v[1]
                if v[2] < vMin[2] :
                    vMin[2] = v[2]
                if v[0] > vMax[0] :
                    vMax[0] = v[0]
                if v[1] > vMax[1] :
                    vMax[1] = v[1]
                if v[2] > vMax[2] :
                    vMax[2] = v[2]

    return [vMin,vMax]
