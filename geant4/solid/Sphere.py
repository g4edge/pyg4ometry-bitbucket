from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
import numpy as _np
import sys as _sys
from copy import deepcopy as _dc

class Sphere(_SolidBase) :
    def __init__(self, name, pRmin, pRmax, pSPhi, pDPhi, pSTheta, pDTheta, nslice = 8, nstack = 8) :
    #def __init__(self, name, pRmin, pRmax, pSPhi, pDPhi, pSTheta, pDTheta, nslice=4, nstack=4):
        """
        Constructs a section of a spherical shell. 

        Inputs:
          name:    string, name of the volume
          pRmin:   float, innner radius of the shell
          pRmax:   float, outer radius of the shell
          pSPhi:   float, starting phi angle in radians
          pSTheta: float, starting theta angle in radians
          pDPhi:   float, total phi angle in radians 0 to 2 pi
          pDTheta: float, total theta angle in radians 0 to pi

        Phi & Theta are the usual spherical coodrinates.
        """
        self.type    = 'Sphere'
        self.name    = name
        self.pRmin   = pRmin
        self.pRmax   = pRmax
        self.pSPhi   = pSPhi
        self.pDPhi   = pDPhi
        self.pSTheta = pSTheta
        self.pDTheta = pDTheta
        self.nslice  = nslice
        self.nstack  = nstack
        self.mesh    = None
        _registry.addSolid(self)
        self.checkParameters()

    def checkParameters(self):
        if self.pRmin > self.pRmax:
            raise ValueError("Inner radius must be less than outer radius.")
        if self.pDTheta > _np.pi:
            raise ValueError("pDTheta must be less than pi")
        if self.pDPhi > _np.pi*2:
            raise ValueError("pDPhi must be less than 2 pi")

    def __repr__(self):
        return 'Sphere : '+self.name+' '+str(self.pRmin)+' '+str(self.pRmax)+' '+str(self.pSPhi)+' '+str(self.pDPhi)+' '+str(self.pSTheta)+' '+str(self.pDTheta)+' '+str(self.nslice)+' '+str(self.nstack)
    
    def pycsgmesh(self):
#        if self.mesh :
#            return self.mesh

        self.basicmesh()
        self.csgmesh()

        return self.mesh
        
    def basicmesh(self) :
        polygons = []
        
        def appendVertex(vertices, theta, phi, r):
            if r > 0:
                d = _Vector(
                    _np.cos(phi) * _np.sin(theta),                          
                    _np.sin(phi) * _np.sin(theta),
                    _np.cos(theta))                         
                vertices.append(_Vertex(c.plus(d.times(r)), None))

            else:
                vertices.append(_Vertex(c, None))
                

        c      = _Vector([0,0,0])
        slices = self.nslice
        stacks = self.nstack
        
        dTheta = self.pDTheta / float(slices)
        dPhi = self.pDPhi / float(stacks)
            
        sthe = self.pSTheta
        sphi = self.pSPhi

        botPoleIn = 1 if sphi%_np.pi == 0 else 0
        topPoleIn = 1 if sphi+self.pDPhi >= _np.pi else 0

        r = self.pRmax
        if botPoleIn:                               #if poles are present mesh them with triangles to avoid point degenracy on pole
            j0 = 0
            j1 = j0 + 1
            for i0 in range(0, slices):
                i1 = i0 + 1
                #  +--+
                #  | /
                #  |/
                #  +
                vertices = []
                appendVertex(vertices, i0 * dTheta + sthe, j0 * dPhi + sphi, r)
                appendVertex(vertices, i1 * dTheta + sthe, j1 * dPhi + sphi, r)
                appendVertex(vertices, i0 * dTheta + sthe, j1 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(vertices)))
                
        if topPoleIn:
            j0 = stacks - 1
            j1 = j0 + 1
            for i0 in range(0, slices):
                i1 = i0 + 1
                #  +
                #  |\
                #  | \
                #  +--+
                vertices = []
                appendVertex(vertices, i0 * dTheta + sthe, j0 * dPhi + sphi, r)
                appendVertex(vertices, i1 * dTheta + sthe, j0 * dPhi + sphi, r)
                appendVertex(vertices, i0 * dTheta + sthe, j1 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(vertices)))
            
        for j0 in range(botPoleIn, stacks - topPoleIn):
            j1 = j0 + 0.5
            j2 = j0 + 1
            for i0 in range(0, slices):
                i1 = i0 + 0.5
                i2 = i0 + 1
                #  +---+
                #  |\ /|
                #  | x |
                #  |/ \|
                #  +---+
                verticesN = []
                appendVertex(verticesN, i1 * dTheta + sthe, j1 * dPhi + sphi, r)
                appendVertex(verticesN, i2 * dTheta + sthe, j2 * dPhi + sphi, r)
                appendVertex(verticesN, i0 * dTheta + sthe, j2 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(verticesN)))
                verticesS = []
                appendVertex(verticesS, i1 * dTheta + sthe, j1 * dPhi + sphi, r)
                appendVertex(verticesS, i0 * dTheta + sthe, j0 * dPhi + sphi, r)
                appendVertex(verticesS, i2 * dTheta + sthe, j0 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(verticesS)))
                verticesW = []
                appendVertex(verticesW, i1 * dTheta + sthe, j1 * dPhi + sphi, r)
                appendVertex(verticesW, i0 * dTheta + sthe, j2 * dPhi + sphi, r)
                appendVertex(verticesW, i0 * dTheta + sthe, j0 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(verticesW)))
                verticesE = []
                appendVertex(verticesE, i1 * dTheta + sthe, j1 * dPhi + sphi, r)
                appendVertex(verticesE, i2 * dTheta + sthe, j0 * dPhi + sphi, r)
                appendVertex(verticesE, i2 * dTheta + sthe, j2 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(verticesE)))

        for i0 in range(0, slices):
            i1 = i0 + 1
            vertices = []
            
            if not topPoleIn:
                appendVertex(vertices, i1 * dTheta + sthe, stacks * dPhi+sphi, r)
                appendVertex(vertices, 0.0, 0.0, 0.0)
                appendVertex(vertices, i0 * dTheta + sthe, stacks * dPhi+sphi, r)
                polygons.append(_Polygon(_dc(vertices)))
                
            vertices = []
            
            if not botPoleIn:
                appendVertex(vertices, i0 * dTheta + sthe, sphi, r)
                appendVertex(vertices, 0.0, 0.0, 0.0)
                appendVertex(vertices, i1 * dTheta + sthe, sphi, r)
                polygons.append(_Polygon(_dc(vertices)))


        if self.pDTheta%(2*_np.pi) != 0:
            for j0 in range(0, stacks):
                j1 = j0 + 1
                vertices = []

                appendVertex(vertices, sthe, j1 * dPhi + sphi, r)
                appendVertex(vertices, 0.0, 0.0, 0.0)
                appendVertex(vertices, sthe, j0 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(vertices)))

                vertices = []

                appendVertex(vertices, slices * dTheta + sthe, j0 * dPhi + sphi, r)
                appendVertex(vertices, 0, 0, 0)
                appendVertex(vertices, slices * dTheta + sthe, j1 * dPhi + sphi, r)
                polygons.append(_Polygon(_dc(vertices)))

        
        self.mesh = _CSG.fromPolygons(polygons)

    def csgmesh(self) :
        if self.pRmin:
            mesh_inner   = _CSG.sphere(radius=self.pRmin, slices=self.nslice, stacks=self.nstack)
            self.mesh   = self.mesh.subtract(mesh_inner)        

