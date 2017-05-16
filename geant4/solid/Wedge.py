from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Polygon as _Polygon
import numpy as _np

class Wedge(_SolidBase) :

    def __init__(self, name, pRMax = 1000, pSPhi=0, pDPhi=1.5, halfzlength=10000):
        self.name  = name
        self.pRMax = pRMax
        self.pSPhi = pSPhi
        self.pDPhi = pDPhi
        self.pDz   = halfzlength

        self.nslice = 16

        self.mesh = None 

    def __repr__(self):
        return 'Wedge : '+self.name+' '+str(self.pRMax)+' '+str(self.pSPhi)+' '+str(self.pDPhi)+' '+str(self.pDz) 

    def pycsgmesh(self):

        if self.mesh : 
            return self.mesh

        d = self.pDz

        phi = _np.linspace(self.pSPhi, self.pDPhi, self.nslice)
        x  = self.pRMax*_np.cos(phi)
        y  = self.pRMax*_np.sin(phi)

        polygons = []

        vZero1 = _Vertex(_Vector(0,0,-d),None)
        vZero2 = _Vertex(_Vector(0,0, d),None)

        p1     = [ _Vertex(_Vector(x[i],y[i],-d),None)  for i in range(0,len(x))]
        p2     = [ _Vertex(_Vector(x[i],y[i], d),None)  for i in range(0,len(x))]


        for i in range(0,len(x)) :
            if i != len(x)-1 :
                # top triangle
                polygons.append(_Polygon([vZero2,p2[i],p2[i+1]]))
                # bottom triangle
                polygons.append(_Polygon([vZero1,p1[i],p1[i+1]]))
                # end square
                polygons.append(_Polygon([p1[i],p1[i+1],p2[i+1],p2[i]]))

        # first end face
        polygons.append(_Polygon([vZero1,p1[0],p2[0], vZero2]))

        # last end face
        polygons.append(_Polygon([vZero1,vZero2,p2[-1],p1[-1]]))

        self.mesh = _CSG.fromPolygons(polygons)

        return self.mesh

    def gdml(self) :
        pass

