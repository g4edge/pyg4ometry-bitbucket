from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Plane as _Plane
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
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
    
class Layer(object):
    def __init__(self, p1, p2, p3, p4, z):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.z  = z

    def Rotated(self, angle):
        result = Layer(self.p1.Rotated(angle),
                       self.p2.Rotated(angle),
                       self.p3.Rotated(angle),
                       self.p4.Rotated(angle),
                       self.z)
        return result

    def __repr__(self):
        s = 'Layer<'
        s += str(self.p1) + ', '
        s += str(self.p2) + ', '
        s += str(self.p3) + ', '
        s += str(self.p4) + ', '
        s += ' z = ' + str(self.z) + '>'
        return s

class TwistedBox2(_SolidBase) :
    def __init__(self, name, twistedangle, pDx, pDy, pDz, nslice=2, refine=0) :
        """
        Constructs a tube of elliptical cross-section. 

        Inputs:
          name:         string, name of the volume
          twistedangle: float, twist angle
          pDx:          float, half-length in x
          pDy:          float, half-length in y
          pDz:          float, half-length in z
          refine:       int, number of steps to iteratively smoothen the mesh
                             by doubling the number of vertices at every step
        """
        self.type = 'TwistedBox'
        self.name = name
        self.twistedAngle = twistedangle
        self.pDx    = pDx
        self.pDy    = pDy
        self.pDz    = pDz
        self.nslice  = nslice
        self.refine = refine
        _registry.addSolid(self)


    def makeLayers(self, p1, p2, p3, p4, pDz, theta, nslice):
        dz = 2*pDz/nslice
        dtheta = theta/nslice
        z = -pDz

        layers = []
        
        bottom = Layer(p1,p2,p3,p4, z)
        bottom = bottom.Rotated(-theta*0.5) #overwrite
        layers.append(bottom)
        
        for i in range(nslice):
            l = layers[-1].Rotated(dtheta) # returns rotated copy
            z += dz # increment z
            l.z = z # fix z
            layers.append(l)

        return layers

    def makeFaceFromLayer(self, layer):
        pols = []
        l = layer
        for p in [l.p1, l.p2, l.p3, l.p4]:
            pols.append(_Vertex(_Vector(p.x, p.y, l.z), None))
        return _Polygon(pols)

    def makeSide(self, pal, pbl, pau, pbu, zl, zu, nsl):
        """
        p = point
        a = first
        b = second
        u = upper
        l = lower
        """
        pols = []
        for i in range(nsl):
            pll = pal + i     * (pbl - pal) / nsl
            plr = pal + (i+1) * (pbl - pal) / nsl
            pul = pau + i     * (pbu - pau) / nsl
            pur = pau + (i+1) * (pbu - pau) / nsl
        
            pol1 = _Polygon([_Vertex(_Vector(pll.x, pll.y, zl), None),
                             _Vertex(_Vector(pul.x, pul.y, zu), None),
                             _Vertex(_Vector(pur.x, pur.y, zu), None)])
            pols.append(pol1)
            
            pol2 = _Polygon([_Vertex(_Vector(plr.x, plr.y, zl), None),
                             _Vertex(_Vector(pll.x, pll.y, zl), None),
                             _Vertex(_Vector(pur.x, pur.y, zu), None)])
            pols.append(pol2)
        return pols
        
    def pycsgmesh(self):
        p1 = TwoVector(-self.pDx, -self.pDy)#, self.pDz]
        p2 = TwoVector(self.pDx, -self.pDy) # self.pDz]
        p3 = TwoVector(self.pDx, self.pDy) #self.pDz]
        p4 = TwoVector(-self.pDx, self.pDy) # self.pDz]

        m = self.makeLayers(p1, p2, p3, p4, self.pDz, self.twistedAngle, self.nslice)

        return self.meshFromLayers(m, self.nslice)

    def meshFromLayers(self, layers, nsl):
        l = layers #shortcut
        allPolygons = []
        polyTop = []
        polyBottom = []      

        bottom = self.makeFaceFromLayer(l[-1])
        allPolygons.append(bottom)
        
        for zi in range(len(l) - 1):
            ll = l[zi]
            ul = l[zi + 1]
            
            pols = self.makeSide(ll.p1, ll.p2, ul.p1, ul.p2, ll.z, ul.z, nsl)
            allPolygons.extend(pols)

            pols = self.makeSide(ll.p2, ll.p3, ul.p2, ul.p3, ll.z, ul.z, nsl)
            allPolygons.extend(pols)

            pols = self.makeSide(ll.p3, ll.p4, ul.p3, ul.p4, ll.z, ul.z, nsl)
            allPolygons.extend(pols)

            pols = self.makeSide(ll.p4, ll.p1, ul.p4, ul.p1, ll.z, ul.z, nsl)
            allPolygons.extend(pols)
        
        top = self.makeFaceFromLayer(l[0])
        allPolygons.append(top)
        
        self.mesh = _CSG.fromPolygons(allPolygons)
        

        return self.mesh
