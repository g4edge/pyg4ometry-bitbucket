from SolidBase import SolidBase as _SolidBase
from Wedge import Wedge as _Wedge
from pyg4ometry.pycsg.core import CSG as _CSG
from pyg4ometry.pycsg.geom import Vector as _Vector
from pyg4ometry.pycsg.geom import Vertex as _Vertex
from pyg4ometry.pycsg.geom import Polygon as _Polygon

import logging as _log
import numpy as _np
import math as _math

class Para(_SolidBase):
    """
    Constructs a parallelepiped.

    :param name: of the volume
    :type name: str
    :param pX: length along x
    :type pX: float, Constant, Quantity, Variable
    :param pY: length along y
    :type pY: float, Constant, Quantity, Variable
    :param pZ: length along z
    :type pZ: float, Constant, Quantity, Variable
    :param pAlpha: angle formed by the y axis and the plane joining the centres of the faces parallel tothe z-x plane at -dy/2 and +dy/2
    :type pAlpha: float, Constant, Quantity, Variable
    :param pTheta: polar angle of the line joining the centres of the faces at -dz/2 and +dz/2 in z
    :type pTheta: float, Constant, Quantity, Variable
    :param pPhi: azimuthal angle of the line joining the centres of the faces at -dx/2 and +dz/2 in z
    :type pPhi: float, Constant, Quantity, Variable
    :param registry: for storing solid
    :type registry: Registry
    :param lunit: length unit (nm,um,mm,m,km) for solid
    :type lunit: str
    :param aunit: angle unit (rad,deg) for solid
    :type aunit: str

    """

    def __init__(self,name,pDx,pDy,pDz,pAlpha,pTheta,pPhi, registry,
                 lunit="mm", aunit="rad", addRegistry=True):
        self.type     = 'Para'
        self.name   = name
        self.pX     = pDx
        self.pY     = pDy
        self.pZ     = pDz
        self.pAlpha = pAlpha
        self.pTheta = pTheta
        self.pPhi   = pPhi
        self.lunit  = lunit
        self.aunit  = aunit

        self.dependents = []

        self.varNames = ["pX", "pY", "pZ","pAlpha","pPhi"]

        if addRegistry:
            registry.addSolid(self)

        self.registry=registry

    def __repr__(self):
        return "Para : {} {} {} {} {} {}".format(self.pX, self.pY, self.pZ,
                                                 self.pAlpha, self.pTheta, self.pPhi)

    def pycsgmesh(self):

        _log.info("para.antlr>")
        import pyg4ometry.gdml.Units as _Units #TODO move circular import
        luval = _Units.unit(self.lunit)
        auval = _Units.unit(self.aunit)

        pX     = self.evaluateParameter(self.pX)*luval
        pY     = self.evaluateParameter(self.pY)*luval
        pZ     = self.evaluateParameter(self.pZ)*luval
        pAlpha = self.evaluateParameter(self.pAlpha)*auval
        pTheta = self.evaluateParameter(self.pTheta)*auval
        pPhi   = self.evaluateParameter(self.pPhi)*auval

        _log.info("para.pycsgmesh>")
        dx_y   = pY*_math.sin(pAlpha)  #changes sign as the y component
        dx_z   = pZ*_math.sin(pTheta)  #changes sign as the z component
        dy     = pZ*_math.sin(pPhi)
        dz     = pZ-pZ*_math.cos(pPhi)

        mesh  = _CSG.fromPolygons([_Polygon([_Vertex(_Vector(-pX-dx_y-dx_z,-pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(-pX+dx_y-dx_z, pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(pX+dx_y-dx_z, pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(pX-dx_y-dx_z,-pY-dy,-pZ+dz), None)]),
                                        _Polygon([_Vertex(_Vector(-pX-dx_y+dx_z,-pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(pX-dx_y+dx_z,-pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(pX+dx_y+dx_z, pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(-pX+dx_y+dx_z, pY+dy, pZ-dz), None)]),
                                        _Polygon([_Vertex(_Vector(-pX-dx_y-dx_z,-pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(pX-dx_y-dx_z,-pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(pX-dx_y+dx_z,-pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(-pX-dx_y+dx_z,-pY+dy, pZ-dz), None)]),
                                        _Polygon([_Vertex(_Vector(-pX+dx_y-dx_z, pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(-pX+dx_y+dx_z, pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(pX+dx_y+dx_z, pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(pX+dx_y-dx_z, pY-dy,-pZ+dz), None)]),
                                        _Polygon([_Vertex(_Vector(-pX-dx_y-dx_z,-pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(-pX-dx_y+dx_z,-pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(-pX+dx_y+dx_z, pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(-pX+dx_y-dx_z, pY-dy,-pZ+dz), None)]),
                                        _Polygon([_Vertex(_Vector(pX-dx_y-dx_z,-pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(pX+dx_y-dx_z, pY-dy,-pZ+dz), None),
                                                  _Vertex(_Vector(pX+dx_y+dx_z, pY+dy, pZ-dz), None),
                                                  _Vertex(_Vector(pX-dx_y+dx_z,-pY+dy, pZ-dz), None)])])


        return mesh
