from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
import numpy as _np


class Polycone(_SolidBase) :
    def __init__(self, name, pSPhi, pDPhi, pZpl, pRMin, pRMax, nslice=16) :
        """
        Constructs a solid of rotation using an arbitrary 2D surface. 

        Inputs:
          name:   string, name of the volume
          pSPhi:  float, starting rotation angle in radians
          pDPhi:  float, total rotation angle in radius
          pZPlns: list, z-positions of planes used 
          pRInr : list, inner radii of surface at each z-plane
          pROut : list, outer radii of surface at each z-plane 
        """
        self.type    = 'polycone'
        self.name    = name
        self.pSPhi   = pSPhi
        self.pDPhi   = pDPhi
        self.pZpl    = pZpl
        self.pRMin   = pRMin
        self.pRMax   = pRMax
        self.nslice  = nslice
        self.mesh = None
        _registry.addSolid(self)


    def pycsgmesh(self) :
        if self.mesh :
            return self.mesh

        self.basicmesh()
        self.csgmesh()

        return self.mesh

    def basicmesh(self) :
        
        polygons = []

        dPhi  = 2*_np.pi/self.nslice
        stacks  = len(self.pZpl)
        slices  = self.nslice

        def appendVertex(vertices, theta, z, r, norm=[]):
            c = _Vector([0,0,0])
            x = r*_np.cos(theta)
            y = r*_np.sin(theta)
            
            d = _Vector(
                x,
                y,
                z)
            
            if not norm:
                n = d
            else:
                n = _Vector(norm)
            vertices.append(_Vertex(c.plus(d), None))
            
        rinout    = [self.pRMin, self.pRMax]
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
                    k0 = i0 if R == self.pRMax else i2  #needed to ensure the surface normals on the inner and outer surface are obeyed
                    k1 = i2 if R == self.pRMax else i0
                    vertices = []
                    appendVertex(vertices, k0 * dPhi + self.pSPhi, self.pZpl[j0], r0)
                    appendVertex(vertices, k1 * dPhi + self.pSPhi, self.pZpl[j0], r0)
                    appendVertex(vertices, k1 * dPhi + self.pSPhi, self.pZpl[j2], r2)
                    appendVertex(vertices, k0 * dPhi + self.pSPhi, self.pZpl[j2], r2)
                    
                    polygons.append(_Polygon(vertices))

        for i0 in range(slices):
            i1 = i0 + 0.5
            i2 = i0 + 1
            vertices_t = []
            vertices_b = []
            
            appendVertex(vertices_t, i2 * dPhi + self.pSPhi, self.pZpl[-1], self.pRMin[-1]+offs)
            appendVertex(vertices_t, i0 * dPhi + self.pSPhi, self.pZpl[-1], self.pRMin[-1]+offs)
            appendVertex(vertices_t, i0 * dPhi + self.pSPhi, self.pZpl[-1], self.pRMax[-1]+offs)
            appendVertex(vertices_t, i2 * dPhi + self.pSPhi, self.pZpl[-1], self.pRMax[-1]+offs)        
            polygons.append(_Polygon(vertices_t))

            appendVertex(vertices_b, i0 * dPhi + self.pSPhi, self.pZpl[0], self.pRMin[0]+offs)
            appendVertex(vertices_b, i2 * dPhi + self.pSPhi, self.pZpl[0], self.pRMin[0]+offs)
            appendVertex(vertices_b, i2 * dPhi + self.pSPhi, self.pZpl[0], self.pRMax[0]+offs)
            appendVertex(vertices_b, i0 * dPhi + self.pSPhi, self.pZpl[0], self.pRMax[0]+offs)        
            polygons.append(_Polygon(vertices_b))

        self.mesh     = _CSG.fromPolygons(polygons)

    def csgmesh(self):
        wrmax    = 3*max([abs(r) for r in self.pRMax]) #ensure intersection wedge is much bigger than solid
        wzlength = 3*max([abs(z) for z in self.pZpl])
        
        if self.pDPhi != 2*_np.pi:
            pWedge = Wedge("wedge_temp",wrmax, self.pSPhi, self.pDPhi+self.pSPhi, wzlength).pycsgmesh()
            self.mesh = pWedge.intersect(self.mesh)

        return self.mesh
        

    def gdml(self, gw, prepend):
        #oe = gw.doc.createElement('polycone')
        #oe.setAttribute('name', prepend + '_' + self.name)
        print "Solid Polyhedra not written out: not supported in writer yet!"
