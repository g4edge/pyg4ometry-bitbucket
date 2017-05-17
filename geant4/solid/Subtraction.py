from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.transformation import *
import copy as _copy
import sys as _sys

class Subtraction(_SolidBase) :
    """
    output = obj1 - obj2
    name = name
    obj1 = unrotated, untranslated solid
    obj2 = solid rotated and translated according to tra2
    tra2 = [rot,tra]
         = [[a,b,g],[dx,dy,dz]]
    """
    def __init__(self,name, obj1, obj2, tra2):
        self.type = "bools"
        self.name = name
        self.obj1 = obj1
        self.obj2 = obj2
        self.tra2 = tra2
        self.mesh = None
        _registry.addSolid(self)

    def __repr__(self) : 
        return 'Subtraction : ('+str(self.obj1)+') - ('+str(self.obj2)+')'

    def pycsgmesh(self):

        if self.mesh :
            return self.mesh

        rot = tbxyz(self.tra2[0])
        tlate = self.tra2[1]

        m1 = self.obj1.pycsgmesh()
        m2 = _copy.deepcopy(self.obj2.pycsgmesh()) # need top copy this mesh as it is transformed
        m2.rotate(rot[0],rad2deg(rot[1]))
        m2.translate(tlate)
        self.obj2mesh = m2

        self.mesh = m1.subtract(m2)
        if not self.mesh.toPolygons():
            print 'Subtraction null mesh',self.name,self.obj1.name, self.obj2.name
            raise NullMeshError(self)

        self.obj1.mesh = None
        self.obj2.mesh = None

        print 'subtraction mesh ', self.name
        return self.mesh
