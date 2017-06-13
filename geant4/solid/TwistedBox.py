from SolidBase import SolidBase as _SolidBase
from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from pygeometry.pycsg.geom import Polygon as _Polygon
from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.solid.Wedge import Wedge as _Wedge
import numpy as _np

class TwistedBox(_SolidBase) :
    def __init__(self, name, twistedangle, pDx, pDy, pDz, refine=0) :
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
        self.type = 'twistedbox'
        self.name = name
        self.twistedAngle = twistedangle
        self.pDx    = pDx
        self.pDy    = pDy
        self.pDz    = pDz
        self.refine = refine

    def pycsgmesh(self):
        vert_crd_up = [[-self.pDx, -self.pDy, self.pDz],[self.pDx, -self.pDy, self.pDz],[self.pDx, self.pDy, self.pDz],[-self.pDx, self.pDy, self.pDz]]
        vert_crd_dn = [[-self.pDx, -self.pDy, -self.pDz],[-self.pDx, self.pDy, -self.pDz],[self.pDx, self.pDy, -self.pDz],[self.pDx, -self.pDy, -self.pDz]]

        vert_crd_rot = []
        
        for i in range(len(vert_crd_up)):
            x_rot = vert_crd_up[i][0]*_np.cos(self.twistedAngle) - vert_crd_up[i][1]*_np.sin(self.twistedAngle)
            y_rot = vert_crd_up[i][0]*_np.sin(self.twistedAngle) + vert_crd_up[i][1]*_np.cos(self.twistedAngle)
            #x_rot = vert_crd_up[i][0]
            #y_rot = vert_crd_up[i][1]
            vert_crd_rot.append([x_rot, y_rot, vert_crd_up[i][2]])
            
        vert_up = []
        vert_dn = []

        for i in range(len(vert_crd_dn)):
            vert_up.append(_Vertex(_Vector(vert_crd_rot[i][0],vert_crd_rot[i][1],vert_crd_rot[i][2]), None))
            vert_dn.append(_Vertex(_Vector(vert_crd_dn[i][0],vert_crd_dn[i][1],vert_crd_dn[i][2]), None))
        """
        self.mesh = _CSG.fromPolygons([_Polygon([vert_dn[0], vert_dn[1], vert_dn[2], vert_dn[3]], None),
                                       _Polygon([vert_up[0], vert_up[1], vert_up[2], vert_up[3]], None),
                                       _Polygon([vert_dn[0], vert_dn[3], vert_up[1], vert_up[0]], None),
                                       _Polygon([vert_dn[1], vert_up[3], vert_up[2], vert_dn[2]], None),
                                       _Polygon([vert_dn[0], vert_up[0], vert_up[3], vert_dn[1]], None),
                                       _Polygon([vert_dn[3], vert_dn[2], vert_up[2], vert_up[1]], None)])
        #_Polygon([vert_dn[3], vert_dn[2], vert_dn[1], vert_dn[0], vert_dn[3]], None),
        #_Polygon([vert_up[0], vert_up[1], vert_up[2], vert_up[3], vert_up[0]], None),
        for i in range(self.refine):
            self.mesh = self.mesh.refine()
        """
        
        self.mesh = _CSG.fromPolygons([_Polygon([vert_dn[0], vert_dn[1], vert_dn[2]], None),
                                       _Polygon([vert_dn[2], vert_dn[3], vert_dn[0]], None),
                                       
                                       _Polygon([vert_up[0], vert_up[1], vert_up[2]], None),
                                       _Polygon([vert_up[2], vert_up[3], vert_up[0]], None),
                                       
                                       _Polygon([vert_dn[0], vert_dn[3], vert_up[1]], None),
                                       _Polygon([vert_dn[0], vert_up[1], vert_up[0]], None),
                                       
                                       _Polygon([vert_dn[1], vert_up[2], vert_dn[2]], None),
                                       _Polygon([vert_dn[1], vert_up[3], vert_up[2]], None),
                                       
                                       _Polygon([vert_dn[0], vert_up[0], vert_up[3]], None),
                                       _Polygon([vert_up[3], vert_dn[1], vert_dn[0]], None),
                                       
                                       _Polygon([vert_dn[3], vert_dn[2], vert_up[2]], None),
                                       _Polygon([vert_up[2], vert_up[1], vert_dn[3]], None)])

        for i in range(self.refine):
            self.mesh = self.mesh.refine()
            
        return self.mesh

    def gdml(selfs):
        pass
