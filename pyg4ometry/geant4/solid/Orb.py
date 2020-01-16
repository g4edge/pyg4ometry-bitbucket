from SolidBase import SolidBase as _SolidBase
from Wedge import Wedge as _Wedge
from ...pycsg.core import CSG as _CSG
from ...pycsg.geom import Vector as _Vector
from ...pycsg.geom import Vertex as _Vertex
from ...pycsg.geom import Polygon as _Polygon

import logging as _log
import numpy as _np

class Orb(_SolidBase):
    """
    Constructs a solid sphere.
    
    :param name: of the sold
    :type name: str
    :param pRMax: outer radius
    :type pRMax: float, Constant, Quantity, Variable, Expression
    :param registry: for storing solid
    :type registry: Registry
    :param lunit: length unit (nm,um,mm,m,km) for solid
    :type lunit: str
    :param nslice: number of phi elements for meshing
    :type nslice: int  
    :param nstack: number of theta elements for meshing
    :type nstack: int     
    """

    def __init__(self, name, pRMax, registry, lunit="mm", nslice=16, nstack=16, addRegistry=True):
        self.type = 'Orb'
        self.name = name
        self.pRMax = pRMax
        self.lunit = lunit
        self.nslice = nslice
        self.nstack = nstack

        self.dependents = []

        self.varNames = ["pRMax"]

        if addRegistry:
            registry.addSolid(self)

        self.registry = registry

    def __repr__(self):
        return "Orb : {} {}".format(self.name, self.pRMax)

    ''''
    def pycsgmeshOld(self):
        _log.info("orb.antlr>")

        import pyg4ometry.gdml.Units as _Units #TODO move circular import 
        luval = _Units.unit(self.lunit)

        pRMax = self.evaluateParameter(self.pRMax)*luval

        _log.info("orb.pycsgmesh>")
        mesh = _CSG.sphere(center=[0,0,0], radius=pRMax,
                           slices=self.nslice, stacks=self.nstack)
        return mesh
    '''
    def pycsgmesh(self):

        _log.info("orb.antlr>")

        import pyg4ometry.gdml.Units as _Units  # TODO move circular import 
        luval = _Units.unit(self.lunit)

        pRMax = self.evaluateParameter(self.pRMax) * luval

        polygons = []

        _log.info("orb.pycsgmesh>")


        dPhi = 2 * _np.pi / self.nslice
        dTheta = _np.pi / self.nstack
        
        for i in range(0, self.nslice, 1):

            i1 = i
            i2 = i+1

            p1 = dPhi*i1
            p2 = dPhi*i2

            for j in range(0, self.nstack, 1) :
                j1 = j
                j2 = j+1

                t1 = dTheta * j1
                t2 = dTheta * j2


                xRMaxP1T1 = pRMax * _np.sin(t1) * _np.cos(p1)
                yRMaxP1T1 = pRMax * _np.sin(t1) * _np.sin(p1)
                zRMaxP1T1 = pRMax * _np.cos(t1)

                xRMaxP2T1 = pRMax * _np.sin(t1) * _np.cos(p2)
                yRMaxP2T1 = pRMax * _np.sin(t1) * _np.sin(p2)
                zRMaxP2T1 = pRMax * _np.cos(t1)

                xRMaxP1T2 = pRMax * _np.sin(t2) * _np.cos(p1)
                yRMaxP1T2 = pRMax * _np.sin(t2) * _np.sin(p1)
                zRMaxP1T2 = pRMax * _np.cos(t2)

                xRMaxP2T2 = pRMax * _np.sin(t2) * _np.cos(p2)
                yRMaxP2T2 = pRMax * _np.sin(t2) * _np.sin(p2)
                zRMaxP2T2 = pRMax * _np.cos(t2)

                if t1 == 0 :                 # if north pole (triangles)
                    vCurv = []
                    vCurv.append(_Vertex([xRMaxP1T1, yRMaxP1T1, zRMaxP1T1], None))
                    vCurv.append(_Vertex([xRMaxP1T2, yRMaxP1T2, zRMaxP1T2], None))
                    vCurv.append(_Vertex([xRMaxP2T2, yRMaxP2T2, zRMaxP2T2], None))
                    polygons.append(_Polygon(vCurv))
                elif t2 == _np.pi :   # if south pole (triangleS)
                    vCurv = []
                    vCurv.append(_Vertex([xRMaxP1T1, yRMaxP1T1, zRMaxP1T1], None))
                    vCurv.append(_Vertex([xRMaxP2T2, yRMaxP2T2, zRMaxP2T2], None))
                    vCurv.append(_Vertex([xRMaxP2T1, yRMaxP2T1, zRMaxP2T1], None))
                    polygons.append(_Polygon(vCurv))
                else :                      # normal curved quad
                    vCurv = []
                    vCurv.append(_Vertex([xRMaxP1T1, yRMaxP1T1, zRMaxP1T1], None))
                    vCurv.append(_Vertex([xRMaxP1T2, yRMaxP1T2, zRMaxP1T2], None))
                    vCurv.append(_Vertex([xRMaxP2T2, yRMaxP2T2, zRMaxP2T2], None))
                    vCurv.append(_Vertex([xRMaxP2T1, yRMaxP2T1, zRMaxP2T1], None))
                    polygons.append(_Polygon(vCurv))

        mesh = _CSG.fromPolygons(polygons)
        return mesh