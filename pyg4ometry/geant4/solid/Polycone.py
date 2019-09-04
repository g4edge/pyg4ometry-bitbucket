from SolidBase             import SolidBase     as _SolidBase
from pyg4ometry.pycsg.core import CSG           as _CSG
from pyg4ometry.pycsg.geom import Vector        as _Vector
from pyg4ometry.pycsg.geom import Vertex        as _Vertex
from pyg4ometry.pycsg.geom import Polygon       as _Polygon
from Wedge                 import Wedge         as _Wedge

import logging as _log
import numpy as _np
from copy import deepcopy as _dc


class Polycone(_SolidBase):
    
    """
    Constructs a solid of rotation using an arbitrary 2D surface.
    
    :param name:   of the solid
    :type name:    str
    :param pSPhi:  starting rotation angle in radians
    :type pSPhi:   float, Constant, Quantity, Variable, Expression
    :param pDPhi:  total rotation angle in radius
    :type pDPhi:   float, Constant, Quantity, Variable, Expression
    :param pZPlns: z-positions of planes used
    :type pZPlns:  list of float, Constant, Quantity, Variable, Expression
    :param pRInr:  inner radii of surface at each z-plane
    :type pRInr:   list of float, Constant, Quantity, Variable, Expression 
    :param pROut:  outer radii of surface at each z-plane
    :type pROut:   list of float, Constant, Quantity, Variable, Expression
    :param registry: for storing solid
    :type registry: Registry
    :param lunit: length unit (nm,um,mm,m,km) for solid
    :type lunit: str
    :param aunit: angle unit (rad,deg) for solid
    :type aunit: str    
    :param nslice: number of phi elements for meshing
    :type nslice: int  
    
    Optional registration as this solid is used as a temporary solid
    in Polyhedra and needn't be always registered.
    """


    def __init__(self, name, pSPhi, pDPhi, pZpl, pRMin, pRMax,
                 registry, lunit="mm", aunit="rad", nslice=16,
                 addRegistry=True):

        self.type    = 'Polycone'
        self.name    = name
        self.pSPhi   = pSPhi
        self.pDPhi   = pDPhi
        self.pZpl    = pZpl
        self.pRMin   = pRMin
        self.pRMax   = pRMax
        self.lunit   = lunit
        self.aunit   = aunit
        self.nslice  = nslice

        self.dependents = []

        self.varNames = ["pSPhi", "pDPhi", "pZpl","pRMin","pRMax"]

        if addRegistry:
            registry.addSolid(self)

        self.registry = registry

    def __repr__(self):
        return "Polycone : {} {} {}".format(self.name, self.pSPhi, self.pDPhi)

    def pycsgmesh(self):

        _log.info("polycone.pycsgmesh>")
        basicmesh = self.basicmesh()
        mesh = self.csgmesh(basicmesh)

        return mesh

    def basicmesh(self):
        _log.info("polycone.antlr>")

        import pyg4ometry.gdml.Units as _Units #TODO move circular import 
        luval = _Units.unit(self.lunit)
        auval = _Units.unit(self.aunit) 

        pSPhi = self.evaluateParameter(self.pSPhi)*auval
        pDPhi = self.evaluateParameter(self.pDPhi)*auval

        pZpl = [val*luval for val in self.evaluateParameter(self.pZpl)]
        pRMin = [val*luval for val in self.evaluateParameter(self.pRMin)]
        pRMax = [val*luval for val in self.evaluateParameter(self.pRMax)]

        _log.info("polycone.basicmesh>")
        polygons = []

        dPhi  = 2*_np.pi/self.nslice
        stacks  = len(pZpl)
        slices  = self.nslice

        def appendVertex(vertices, theta, z, r, norm=[]):
            c = _Vector([0,0,0])
            x = r*_np.cos(theta)
            y = r*_np.sin(theta)

            d = _Vector(x,y,z)

            if not norm:
                n = d
            else:
                n = _Vector(norm)
            vertices.append(_Vertex(c.plus(d), None))

        rinout    = [pRMin, pRMax]
        meshinout = []

        offs = 1.e-25 #Small offset to avoid point degenracy when the radius is zero. TODO: make more robust
        for R in rinout:
            for j0 in range(stacks-1):
                j1 = j0 + 0.5
                j2 = j0 + 1
                r0 = R[j0] + offs
                r2 = R[j2] + offs
                for i0 in range(slices):
                    i1 = i0 + 0.5
                    i2 = i0 + 1
                    k0 = i0 if R == pRMax else i2  #needed to ensure the surface normals on the inner and outer surface are obeyed
                    k1 = i2 if R == pRMax else i0

                    if r0 == r2 and pZpl[j0] == pZpl[j2]:
                        continue # don't mesh between degenrate planes

                    vertices = []
                    appendVertex(vertices, k0 * dPhi + pSPhi, pZpl[j0], r0)
                    appendVertex(vertices, k1 * dPhi + pSPhi, pZpl[j0], r0)
                    appendVertex(vertices, k1 * dPhi + pSPhi, pZpl[j2], r2)
                    appendVertex(vertices, k0 * dPhi + pSPhi, pZpl[j2], r2)

                    polygons.append(_Polygon(_dc(vertices)))

        for i0 in range(slices):
            i1 = i0 + 0.5
            i2 = i0 + 1
            vertices_t = []
            vertices_b = []

            if (pRMin[-1] or pRMax[-1]) and pRMin[-1] != pRMax[-1]:
                appendVertex(vertices_t, i2 * dPhi + pSPhi, pZpl[-1], pRMin[-1]+offs)
                appendVertex(vertices_t, i0 * dPhi + pSPhi, pZpl[-1], pRMin[-1]+offs)
                appendVertex(vertices_t, i0 * dPhi + pSPhi, pZpl[-1], pRMax[-1]+offs)
                appendVertex(vertices_t, i2 * dPhi + pSPhi, pZpl[-1], pRMax[-1]+offs)
                polygons.append(_Polygon(_dc(vertices_t)))

            if (pRMin[0] or pRMax[0]) and pRMin[0] != pRMax[0]:
                appendVertex(vertices_b, i0 * dPhi + pSPhi, pZpl[0], pRMin[0]+offs)
                appendVertex(vertices_b, i2 * dPhi + pSPhi, pZpl[0], pRMin[0]+offs)
                appendVertex(vertices_b, i2 * dPhi + pSPhi, pZpl[0], pRMax[0]+offs)
                appendVertex(vertices_b, i0 * dPhi + pSPhi, pZpl[0], pRMax[0]+offs)
                polygons.append(_Polygon(_dc(vertices_b)))

        basicmesh     = _CSG.fromPolygons(polygons)
        return basicmesh

    def csgmesh(self, basicmesh):
        _log.info("polycone.antlr>")
        pSPhi = float(self.pSPhi)
        pDPhi = float(self.pDPhi)
        pZpl = [float(val) for val in self.pZpl]
        pRMax = [float(val) for val in self.pRMax]

        _log.info("polycone.csgmesh>")
        wrmax    = 3*max([abs(r) for r in pRMax]) #ensure intersection wedge is much bigger than solid
        wzlength = 3*max([abs(z) for z in pZpl])

        if pDPhi != 2*_np.pi:
            pWedge = _Wedge("wedge_temp",wrmax, pSPhi, pDPhi+pSPhi, wzlength).pycsgmesh()
            mesh = basicmesh.intersect(pWedge)
        else :
            mesh = basicmesh

        return mesh
