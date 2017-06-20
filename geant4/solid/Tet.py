from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
from pygeometry.geant4.solid.Plane import Plane as _Plane
import numpy as _np

class Tet(_SolidBase) :
    def __init__(self, name, anchor, p2, p3, p4, degeneracyFlag = False) :
        """
        Constructs a tetrahedra. 

        Inputs:
          name:           string, name of the volume
          anchor:         list, anchor point
          p2:             list, point 2
          p3:             list, point 3
          p4:             list, point 4
          degeneracyFlag: bool, indicates degeneracy of points
        """
        self.type    = 'Tet'
        self.name    = name
        self.anchor  = anchor
        self.p2      = p2
        self.p3      = p3
        self.p4      = p4
        self.degen   = degeneracyFlag
        _registry.addSolid(self)                


    def pycsgmesh(self):
        vert_ancr = _Vertex(_Vector(self.anchor[0], self.anchor[1], self.anchor[2]), None)
        base      = [self.p2, self.p3, self.p4]
        vert_base = []
        
        for i in range(len(base)):
            vert_base.append(_Vertex(_Vector(base[i][0],base[i][1],base[i][2]), None))

        self.mesh = _CSG.fromPolygons([_Polygon([vert_base[2], vert_base[1], vert_base[0]], None),
                                       _Polygon([vert_base[1], vert_ancr, vert_base[0]], None),
                                       _Polygon([vert_base[2], vert_ancr, vert_base[1]], None),
                                       _Polygon([vert_base[0], vert_ancr, vert_base[2]], None)])

        return self.mesh
