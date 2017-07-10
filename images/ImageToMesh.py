from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Polygon as _Polygon
from astropy.io import fits
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
import pygeometry.vtk as _vtk
import numpy as _np
import sys as _sys

class ImageToMesh():
    def __init__(self):
        self._mesh = None

    def MakeMeshFromFits(self, filename, length=100, xlim=None, ylim=None):
        d = self._LoadData(filename)
        self._MeshFromArray(d, length, xlim, ylim)
        self.Visualise()

    def _LoadData(self, filename):
        h = fits.open(filename)
        r = h[0]
        q = r.data
        
        return q

    def _MeshFromArray(self, array, length=100, xlim=None, ylim=None):

        arrays = array
        if xlim != None:
            arrays = array[xlim[0]:xlim[1]]
        if ylim != None:
            arrays = array[:,ylim[0]:ylim[1]]

        s1 = _np.max(arrays) - _np.min(arrays)
        s2 = 10
        s = s2/s1

        d1 = (arrays - _np.min(arrays)) * s

        f = _np.shape(d1)

        d2 = _np.insert(d1, [0]       , 0, axis=1)
        d3 = _np.insert(d2, [f[1] + 1], 0, axis=1)
        d4 = _np.insert(d3, [0]       , 0, axis=0)
        d5 = _np.insert(d4, [f[0] + 1], 0, axis=0)

        z = length/_np.max(f)

        pols = []

        nrows = _np.shape(d5)[0]
        for j in range(_np.shape(d5)[0]-1):
            progress = (float(j) / nrows ) *100
            _sys.stdout.write("Meshing: %d%%     \r" % (progress) )
            _sys.stdout.flush()
            for i in range(_np.shape(d5)[1]-1):
                k = i * z
                l = j * z
                pol1 = _Polygon([_Vertex(_Vector(k, l, d5[i, j]), None),
                                 _Vertex(_Vector(k+z, l, d5[i+1, j]), None),
                                 _Vertex(_Vector(k, l+z, d5[i, j+1]), None)])
                pols.append(pol1)
                
                pol2 = _Polygon([_Vertex(_Vector(k, l+z, d5[i, j+1]), None),
                                 _Vertex(_Vector(k+z, l, d5[i+1, j]), None),
                                 _Vertex(_Vector(k+z, l+z, d5[i+1, j+1]), None)])
                pols.append(pol2)
                
        #print pols

        pol3 = _Polygon([_Vertex(_Vector(0,0,0), None),
                         _Vertex(_Vector(0, _np.shape(d5)[0], 0), None),
                         _Vertex(_Vector(0,0,-5), None)])

        pol4 = _Polygon([_Vertex(_Vector(0,0,0), None),
                         _Vertex(_Vector(0, _np.shape(d5)[0], 0), None),
                         _Vertex(_Vector(0, _np.shape(d5)[0], -5), None)])

        pol5 = _Polygon([_Vertex(_Vector(_np.shape(d5)[1], 0, 0), None),
                         _Vertex(_Vector(0,0,0), None),
                         _Vertex(_Vector(0,0,-5), None)])

        pol6 = _Polygon([_Vertex(_Vector(0,0,-5), None),
                         _Vertex(_Vector(_np.shape(d5)[1], 0, -5), None),
                         _Vertex(_Vector(_np.shape(d5)[1], 0, 0), None)])

        pol7 = _Polygon([_Vertex(_Vector(0, _np.shape(d5)[0], 0), None),
                         _Vertex(_Vector(_np.shape(d5)[1], _np.shape(d5)[0], 0), None),
                         _Vertex(_Vector(_np.shape(d5)[1], _np.shape(d5)[0], -5), None)])

        pol8 = _Polygon([_Vertex(_Vector(_np.shape(d5)[1], _np.shape(d5)[0], -5), None),
                         _Vertex(_Vector(0, _np.shape(d5)[0], -5), None),
                         _Vertex(_Vector(0, _np.shape(d5)[0], 0), None)])

        pol9 = _Polygon([_Vertex(_Vector(_np.shape(d5)[1], _np.shape(d5)[0], 0), None),
                         _Vertex(_Vector(_np.shape(d5)[1], 0, 0), None),
                         _Vertex(_Vector(_np.shape(d5)[1], 0, -5), None)])

        pol10 = _Polygon([_Vertex(_Vector(_np.shape(d5)[1], 0, -5), None),
                          _Vertex(_Vector(_np.shape(d5)[1], _np.shape(d5)[0], -5), None),
                          _Vertex(_Vector(_np.shape(d5)[1], _np.shape(d5)[0], 0), None)])

        pols.append(pol3)
        pols.append(pol4)
        pols.append(pol5)
        pols.append(pol6)
        pols.append(pol7)
        pols.append(pol8)
        pols.append(pol9)
        pols.append(pol10)        
                         
        
        self._mesh = _CSG.fromPolygons(pols)
        self._mesh.alpha     = 0.5
        self._mesh.wireframe = False
        self._mesh.colour    = [1,1,1]

    def Visualise(self):
        v = _vtk.Viewer()
        v.addPycsgMeshList([self._mesh])
        v.view()

    def WriteMeshToSTL(self, outputFileName):
        if self._mesh == None:
            raise AttributeError("No mesh yet")

        
