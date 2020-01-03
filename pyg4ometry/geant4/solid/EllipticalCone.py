from SolidBase import SolidBase as _SolidBase
from Wedge import Wedge as _Wedge
from ...pycsg.core import CSG as _CSG
from ...pycsg.geom import Vector as _Vector
from ...pycsg.geom import Vertex as _Vertex
from ...pycsg.geom import Polygon as _Polygon
import logging as _log

import numpy as _np

class EllipticalCone(_SolidBase):
    def __init__(self, name, pxSemiAxis, pySemiAxis, zMax, pzTopCut,
                 registry, lunit="mm",nslice=16, nstack=16, addRegistry=True):
        """
        Constructs a cone with elliptical cross-section.

        Inputs:
          name:       string, name of the volume
          pxSemiAxis: float, semiaxis in x (fraction of zMax)
          pySemiAxis: float, semiaxis in y (fraction of zMax)
          zMax:       float, height of cone
          pzTopCut:   float, z-position of upper
        """

        self.type       = 'EllipticalCone'
        self.name       = name
        self.pxSemiAxis = pxSemiAxis
        self.pySemiAxis = pySemiAxis
        self.zMax       = zMax
        self.pzTopCut   = pzTopCut
        self.lunit      = lunit
        self.nslice     = nslice
        self.nstack     = nslice

        self.dependents = []

        self.varNames = ["pxSemiAxis", "pySemiAxis", "zMax","pzTopCut"]

        if addRegistry:
            registry.addSolid(self)

        self.registry = registry

        #self.checkParameters()

    def __repr__(self):
        return "EllipticalCone : {} {} {} {} {}".format(self.name, self.pxSemiAxis,
                                                        self.pySemiAxis, self.zMax,
                                                        self.pzTopCut)

    def checkParameters(self):
        pzTopCut = self.evaluateParameter(self.pzTopCut)
        zMax = self.evaluateParameter(self.zMax)
        if pzTopCut <= -zMax/2.0 or pzTopCut > zMax/2.0:
            raise ValueError("zMax must be greater than pzTopCut")

    '''
    def pycsgmeshOld(self):

        _log.info("ellipticalcone.antlr>")

        import pyg4ometry.gdml.Units as _Units  # TODO move circular import
        luval = _Units.unit(self.lunit)

        pxSemiAxis = self.evaluateParameter(self.pxSemiAxis) * luval
        pySemiAxis = self.evaluateParameter(self.pySemiAxis) * luval
        zMax = self.evaluateParameter(self.zMax) * luval
        pzTopCut = self.evaluateParameter(self.pzTopCut) * luval

        _log.info("ellipticalcone.pycsgmesh>")
        polygons = []

        sz = -zMax / 2.
        dz = zMax / self.nstack
        dTheta = 2 * _np.pi / self.nslice
        stacks = self.nstack
        slices = self.nslice

        # semix and semiy are fractions of zmax - calculate absolute numbers
        dxabs = pxSemiAxis * zMax
        dyabs = pySemiAxis * zMax

        def appendVertex(vertices, theta, z, dx=dxabs, dy=dyabs, norm=[]):
            c = _Vector([0, 0, 0])
            x = dx * (((zMax - z) / zMax) * _np.cos(theta))  # generate points on an ellipse
            y = dy * (((zMax - z) / zMax) * _np.sin(theta))
            d = _Vector(
                x,
                y,
                z)
            if not norm:
                n = d
            else:
                n = _Vector(norm)
            vertices.append(_Vertex(c.plus(d), n))

        for j0 in range(slices):
            j1 = j0 + 0.5
            j2 = j0 + 1
            for i0 in range(stacks):
                i1 = i0 + 0.5
                i2 = i0 + 1
                verticesN = []
                appendVertex(verticesN, i1 * dTheta, j1 * dz + sz)
                appendVertex(verticesN, i2 * dTheta, j2 * dz + sz)
                appendVertex(verticesN, i0 * dTheta, j2 * dz + sz)
                polygons.append(_Polygon(verticesN))
                verticesS = []
                appendVertex(verticesS, i1 * dTheta, j1 * dz + sz)
                appendVertex(verticesS, i0 * dTheta, j0 * dz + sz)
                appendVertex(verticesS, i2 * dTheta, j0 * dz + sz)
                polygons.append(_Polygon(verticesS))
                verticesW = []
                appendVertex(verticesW, i1 * dTheta, j1 * dz + sz)
                appendVertex(verticesW, i0 * dTheta, j2 * dz + sz)
                appendVertex(verticesW, i0 * dTheta, j0 * dz + sz)
                polygons.append(_Polygon(verticesW))
                verticesE = []
                appendVertex(verticesE, i1 * dTheta, j1 * dz + sz)
                appendVertex(verticesE, i2 * dTheta, j0 * dz + sz)
                appendVertex(verticesE, i2 * dTheta, j2 * dz + sz)
                polygons.append(_Polygon(verticesE))

        for i0 in range(0, slices):
            i1 = i0 + 1

            vertices = []

            appendVertex(vertices, i0 * dTheta, sz, norm=[0, 0, 1])
            appendVertex(vertices, 0, sz, dx=0, dy=0, norm=[0, 0, 1])
            appendVertex(vertices, i1 * dTheta, sz, norm=[0, 0, 1])
            polygons.append(_Polygon(vertices))

            vertices = []
            appendVertex(vertices, i1 * dTheta, stacks * dz + sz, norm=[0, 0, -1])
            appendVertex(vertices, 0, slices * dz + sz, dx=0, dy=0, norm=[0, 0, -1])
            appendVertex(vertices, i0 * dTheta, stacks * dz + sz, norm=[0, 0, -1])
            polygons.append(_Polygon(vertices))

        mesh = _CSG.fromPolygons(polygons)

        return mesh
    '''

    def pycsgmesh(self):
        _log.info("ellipticalcone.antlr>")

        import pyg4ometry.gdml.Units as _Units  # TODO move circular import
        luval = _Units.unit(self.lunit)

        pxSemiAxis = self.evaluateParameter(self.pxSemiAxis) * luval
        pySemiAxis = self.evaluateParameter(self.pySemiAxis) * luval
        zMax = self.evaluateParameter(self.zMax) * luval
        pzTopCut = self.evaluateParameter(self.pzTopCut) * luval

        _log.info("ellipticalcone.pycsgmesh>")
        polygons = []

        # length of complete cone
        L = zMax/pzTopCut

        dTheta = 2 * _np.pi / self.nslice
        slices = self.nslice

        # semix and semiy are fractions of zmax - calculate absolute numbers
        dx = pxSemiAxis * zMax
        dy = pySemiAxis * zMax

        for i0 in range(0,slices):

            i1 = i0
            i2 = i0 + 1

            z1 = zMax/2
            x1 = dx * ((L-z1 - zMax/2)/L) * _np.cos(dTheta*i1)
            y1 = dy * ((L-z1 - zMax/2)/L) * _np.sin(dTheta*i1)

            z2 = -zMax/2
            x2 = dx * ((L-z2 - zMax/2)/L) * _np.cos(dTheta*i1)
            y2 = dy * ((L-z2 - zMax/2)/L) * _np.sin(dTheta*i1)

            z3 = -zMax/2
            x3 = dx * ((L-z3 - zMax/2)/L) * _np.cos(dTheta*i2)
            y3 = dy * ((L-z3 - zMax/2)/L) * _np.sin(dTheta*i2)

            z4 = zMax/2
            x4 = dx * ((L-z4 - zMax/2)/L) * _np.cos(dTheta*i2)
            y4 = dy * ((L-z4 - zMax/2)/L) * _np.sin(dTheta*i2)

            vertices = []

            vertices.append(_Vertex([x1,y1,z1], None))
            vertices.append(_Vertex([x2,y2,z2], None))
            vertices.append(_Vertex([x3,y3,z3], None))
            vertices.append(_Vertex([x4,y4,z4], None))

            polygons.append(_Polygon(vertices))

            # bottom
            verticesb = []

            z1b = -zMax/2
            x1b = dx * ((L - z1b - zMax / 2) / L) * _np.cos(dTheta * i1)
            y1b = dy * ((L - z1b - zMax / 2) / L) * _np.sin(dTheta * i1)

            z2b = -zMax/2
            x2b = 0
            y2b = 0

            z3b = -zMax/2
            x3b = dx * ((L - z3b - zMax / 2) / L) * _np.cos(dTheta * i2)
            y3b = dy * ((L - z3b - zMax / 2) / L) * _np.sin(dTheta * i2)

            verticesb.append(_Vertex([x1b, y1b, z1b], None))
            verticesb.append(_Vertex([x2b, y2b, z2b], None))
            verticesb.append(_Vertex([x3b, y3b, z3b], None))

            polygons.append(_Polygon(verticesb))

            #top
            verticest = []

            z1t = zMax/2
            x1t = dx * ((L - z1t - zMax / 2) / L) * _np.cos(dTheta * i1)
            y1t = dy * ((L - z1t - zMax / 2) / L) * _np.sin(dTheta * i1)

            z2t = zMax/2
            x2t = 0
            y2t = 0

            z3t = zMax/2
            x3t = dx * ((L - z3t - zMax / 2) / L) * _np.cos(dTheta * i2)
            y3t = dy * ((L - z3t - zMax / 2) / L) * _np.sin(dTheta * i2)

            verticest.append(_Vertex([x1t, y1t, z1t], None))
            verticest.append(_Vertex([x2t, y2t, z2t], None))
            verticest.append(_Vertex([x3t, y3t, z3t], None))

            polygons.append(_Polygon(verticest))

        mesh = _CSG.fromPolygons(polygons)

        return mesh
