from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Plane as _Plane
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
from pygeometry.geant4.solid.Layer import Layer as _Layer
import numpy as _np

class TwoVector(object):
    def __init__(self, xIn, yIn):
        self.x = xIn
        self.y = yIn

    def Rotated(self, angle):
        # do rotation
        xr = self.x*_np.cos(angle) - self.y*_np.sin(angle)
        yr = self.x*_np.sin(angle) + self.y*_np.cos(angle)
        return TwoVector(xr,yr)

    def __repr__(self):
        s = '(' + str(self.x) + ', ' + str(self.y) + ')'
        return s

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Invalid index "+str(index))

    def __add__(self, other):
        if type(other) == TwoVector:
            return TwoVector(self.x + other.x, self.y + other.y)
        elif type(other) == float or type(other) == int:
            return TwoVector(self.x + other, self.y + other)
        else:
            raise ValueError("unsupported type " + str(type(other)))
    
    def __sub__(self, other):
        if type(other) == TwoVector:
            return TwoVector(self.x - other.x, self.y - other.y)
        elif type(other) == float or type(other) == int:
            return TwoVector(self.x - other, self.y - other)
        else:
            raise ValueError("unsupported type " + str(type(other)))
              
    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return TwoVector(self.x * other, self.y * other)
        else:
            raise ValueError("unsupported type " + str(type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)
              
    def __div__(self, other):
        if type(other) == float or type(other) == int:
            return TwoVector(self.x / other, self.y / other)
        else:
            raise ValueError("unsupported type " + str(type(other)))
