from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
import numpy as _np

import math as _math
from math import cos as _cos
from math import sin as _sin
from math import acos as _acos
from math import asin as _asin

class Para(_SolidBase):
    def __init__(self,name,pDx,pDy,pDz,pAlpha,pTheta,pPhi):
        """
        Constructs a parallelepiped.

        Inputs:
          name:  string, name of the volume
          pX:    float, half-length along x
          pY:    float, half-length along y
          pZ:    float, half-length along z
          pAlpha: float, angle formed by the y axis and the plane joining the centres of the faces parallel tothe z-x plane at -dy and +dy
          pTheta: float, polar angle of the line joining the centres of the faces at -dz and +dz in z
          pPhi:   float, azimuthal angle of the line joining the centres of the faces at -dx and +dz in z
        """

        self.type     = 'para'
        self.name   = name
        self.pX     = pDx
        self.pY     = pDy
        self.pZ     = pDz
        self.pAlpha = pAlpha
        self.pTheta = pTheta
        self.pPhi   = pPhi
        self.dx_y   = self.pY*_sin(self.pAlpha)  #changes sign as the y component
        self.dx_z   = +self.pZ*_sin(self.pTheta) #changes sign as the z component
        self.dy     = self.pZ*_sin(self.pPhi)
        self.dz     = self.pZ-self.pZ*_cos(pPhi)

    def pycsgmesh(self) :
        self.mesh  = _CSG.fromPolygons([_Polygon([_Vertex(_Vector(-self.pX-self.dx_y-self.dx_z,-self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector(-self.pX+self.dx_y-self.dx_z, self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector( self.pX+self.dx_y-self.dx_z, self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector( self.pX-self.dx_y-self.dx_z,-self.pY-self.dy,-self.pZ+self.dz), None)]),
                                        _Polygon([_Vertex(_Vector(-self.pX-self.dx_y+self.dx_z,-self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector( self.pX-self.dx_y+self.dx_z,-self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector( self.pX+self.dx_y+self.dx_z, self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector(-self.pX+self.dx_y+self.dx_z, self.pY+self.dy, self.pZ-self.dz), None)]),
                                        _Polygon([_Vertex(_Vector(-self.pX-self.dx_y-self.dx_z,-self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector( self.pX-self.dx_y-self.dx_z,-self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector( self.pX-self.dx_y+self.dx_z,-self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector(-self.pX-self.dx_y+self.dx_z,-self.pY+self.dy, self.pZ-self.dz), None)]),
                                        _Polygon([_Vertex(_Vector(-self.pX+self.dx_y-self.dx_z, self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector(-self.pX+self.dx_y+self.dx_z, self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector( self.pX+self.dx_y+self.dx_z, self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector( self.pX+self.dx_y-self.dx_z, self.pY-self.dy,-self.pZ+self.dz), None)]),
                                        _Polygon([_Vertex(_Vector(-self.pX-self.dx_y-self.dx_z,-self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector(-self.pX-self.dx_y+self.dx_z,-self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector(-self.pX+self.dx_y+self.dx_z, self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector(-self.pX+self.dx_y-self.dx_z, self.pY-self.dy,-self.pZ+self.dz), None)]),
                                        _Polygon([_Vertex(_Vector( self.pX-self.dx_y-self.dx_z,-self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector( self.pX+self.dx_y-self.dx_z, self.pY-self.dy,-self.pZ+self.dz), None),
                                                  _Vertex(_Vector( self.pX+self.dx_y+self.dx_z, self.pY+self.dy, self.pZ-self.dz), None),
                                                  _Vertex(_Vector( self.pX-self.dx_y+self.dx_z,-self.pY+self.dy, self.pZ-self.dz), None)])])


        return self.mesh

