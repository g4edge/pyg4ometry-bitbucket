from SolidBase import SolidBase as _SolidBase
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Polycone import Polycone as _Polycone
import numpy as _np


class Polyhedra(_SolidBase) :
    def __init__(self, name, phiStart, phiTotal, numSide, numZPlanes, zPlane, rInner, rOuter) :
        """
        Constructs a polyhedra. 

        Inputs:
          name:       string, name of the volume
          phiStart:   float, start phi angle
          phiTotal:   float, delta phi angle
          numSide:    int, number of sides
          numZPlanes: int, number of planes along z
          zPlane:     list, position of z planes
          rInner:     list, tangent distance to inner surface per z plane
          rOuter:     list, tangent distance to outer surface per z plane
          
        """
        self.type       = 'polyhedra'
        self.name       = name
        self.phiStart   = phiStart
        self.phiTotal   = phiTotal
        self.numSide    = numSide
        self.numZPlanes = numZPlanes
        self.zPlane     = zPlane
        self.rInner     = rInner
        self.rOuter     = rOuter
        self.mesh = None
        _registry.addSolid(self)


    def pycsgmesh(self):
        if self.mesh :
            return self.mesh

        self.basicmesh()
        self.csgmesh()

        return self.mesh

    def basicmesh(self):
        fillfrac  = self.phiTotal/(2*_np.pi)
        slices    = (self.numSide)/fillfrac 
        
        ph        = _Polycone(self.name, self.phiStart, self.phiTotal, self.zPlane, self.rInner, self.rOuter, nslice=int(_np.ceil(slices)))
        self.mesh = ph.pycsgmesh()

        return self.mesh

    def csgmesh(self):
        return self.mesh

    def gdmlWrite(self, gw, prepend):
        #oe = gw.doc.createElement('polyhedra')
        #oe.setAttribute('name', prepend + '_' + self.name)
        print "Solid Polyhedra not written out: not supported in writer yet!"


    
