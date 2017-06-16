from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
import numpy as _np

class TwistedTrap(_SolidBase) :
    def __init__(self, name, twistedangle, pDz, pTheta, pDPhi, pDy1, pDx1, pDx2, pDy2, pDx3, pDx4, pAlp) :
        """
        Constructs a general trapezoid with a twist around one axis. 

        Inputs:
          name:          string, name of the volume
          twisted angle: float, angle of twist (<90 deg)
          pDz:           float, half length along z
          pDx1:          float, half length along x of the side at y=-pDy1
          pDx2:          float, half length along x of the side at y=+pDy1
          pTheta:        float, polar angle of the line joining the centres of the faces at -/+pDz
          pPhi:          float, azimuthal angle of the line joining the centres of the faces at -/+pDz
          pDy1:          float, half-length at -pDz
          pDy2:          float, half-length at +pDz
          pDx3:          float, halg-length of the side at y=-pDy2 of the face at +pDz
          pDx4:          float, halg-length of the side at y=+pDy2 of the face at +pDz
          pAlp:          float, angle wrt the y axi from the centre of the side
        """
        self.type         = 'trap'
        self.name         = name
        self.twistedangle = twistedangle
        self.pDz          = pDz
        self.pTheta       = pTheta
        self.pDPhi        = pDPhi
        self.pDy1         = pDy1
        self.pDx1         = pDx1
        self.pDx2         = pDx2
        self.pDy2         = pDy2
        self.pDx3         = pDx3
        self.pDx4         = pDx4
        self.pAlp        = pAlp

    def pycsgmesh(self):
        print 'Mesh not yet completed.'
        pass
