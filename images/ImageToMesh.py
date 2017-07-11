from pygeometry.pycsg.core import CSG as _CSG
from pygeometry.pycsg.geom import Polygon as _Polygon
from astropy.io import fits
from pygeometry.pycsg.geom import Vector as _Vector
from pygeometry.pycsg.geom import Vertex as _Vertex
from scipy.misc import imresize
import pygeometry.vtk as _vtk
import numpy as _np
import sys as _sys

class ImageToMesh():
    def __init__(self, filename=None):
        self.data  = None # array data
        self._mesh = None # mesh data
        if filename != None:
            self.LoadData(filename)

    def LoadData(self, filename):
        self.data = self._GetFirstImageAsArray(filename)

    def MakeMeshFromFits(self, filename, length=100, height=10, depth=5, xlim=None, ylim=None):
        """
        Load fits file and then call MeshFromArray.  See MeshFromArray for parameter details.
        """
        self.LoadData(filename)
        self.MeshFromArray(self.data, length, height, depth, xlim, ylim)
        self.Visualise()
        
    def _GetFirstImageAsArray(self, filename):
        """
        Returns numpy array from fits file.
        """
        h = fits.open(filename)
        r = h[0]
        q = r.data
        
        return q

    def ScaleData(self, scale):
        self.data *= scale

    def MakeMesh(self, length=100, height=10, depth=5, xlim=None, ylim=None):
        """
        Make mesh based on self.data.
        """
        self.MeshFromArray(self.data)

    def MeshFromArray(self, array, length=100, height=10, depth=5, xlim=None, ylim=None):
        """
        Takes 2D numpy array, and builds a mesh from the array. Forms a 3D solid.
        
        length = in mm of the longest dimension
        height = in mm, height of mesh from array
        depth  = in mm, height of baseplate mesh is placed on
        xlim   = list of two values defining upper and lower limit of array inidices in x dimension
        ylim   = list of two values defining upper and lower limit of array inidices in y dimension
        """
        #slicing array to desired size
        array1 = array
        if xlim != None:
            array1 = array1[xlim[0]:xlim[1],:]
        if ylim != None:
            array1 = array1[:,ylim[0]:ylim[1]]
        
        size = _np.shape(array1)
        imscale = 500./float(_np.max(size))
        arrays = imresize(array1, float(imscale), mode='F')

        #scaling vertical size to 10mm
        s1 = _np.max(arrays) - _np.min(arrays)
        s2 = height
        s = s2/s1
        d1 = (arrays - _np.min(arrays)) * s

        #padding array with 0's to make edges of mesh 0
        f1 = _np.shape(d1)
        d2 = _np.insert(d1, [0]       , 0, axis=1)
        d3 = _np.insert(d2, [f1[1] + 1], 0, axis=1)
        d4 = _np.insert(d3, [0]       , 0, axis=0)
        d5 = _np.insert(d4, [f1[0] + 1], 0, axis=0)

        #scaling horizontal size
        f2 = _np.shape(d5)
        xscl = float(length)/float(_np.max(f2))
        
        pols = []
        nrows = _np.shape(d5)[1]-1 # for feedback

        #Building upper sufface of mesh        
        for j in range(_np.shape(d5)[1]-1):
            progress = (float(j) / nrows ) *100
            _sys.stdout.write("Meshing: %d%%     \r" % (progress) )
            _sys.stdout.flush()
            for i in range(_np.shape(d5)[0]-1):
                
                k = i * xscl
                l = j * xscl
                pol1 = _Polygon([_Vertex(_Vector(k,      l,      d5[i, j]),   None),
                                 _Vertex(_Vector(k+xscl, l,      d5[i+1, j]), None),
                                 _Vertex(_Vector(k,      l+xscl, d5[i, j+1]), None)])
                pols.append(pol1)
                
                pol2 = _Polygon([_Vertex(_Vector(k,      l+xscl, d5[i, j+1]),   None),
                                 _Vertex(_Vector(k+xscl, l,      d5[i+1, j]),   None),
                                 _Vertex(_Vector(k+xscl, l+xscl, d5[i+1, j+1]), None)])
                pols.append(pol2)

        progress = 100
        _sys.stdout.write("Meshing: %d%%     \r" % (progress) + "\n" )
        _sys.stdout.flush()

        #Building the mesh for the surfaces, forming a box

        x = _np.shape(d5)[0] * xscl
        y = _np.shape(d5)[1] * xscl
    
        pol3 = _Polygon([_Vertex(_Vector(0,0,0), None),
                         _Vertex(_Vector(0, y, 0), None),
                         _Vertex(_Vector(0, y, -depth), None),
                         _Vertex(_Vector(0,0,-depth), None)])

        pol4 = _Polygon([_Vertex(_Vector(x, 0, 0), None),
                         _Vertex(_Vector(0,0,0), None),
                         _Vertex(_Vector(0,0,-depth), None),
                         _Vertex(_Vector(x, 0, -depth), None)])

        pol5 = _Polygon([_Vertex(_Vector(0, y, 0), None),
                         _Vertex(_Vector(x, y, 0), None),
                         _Vertex(_Vector(x, y, -depth), None),
                         _Vertex(_Vector(0, y, -depth), None)])

        pol6 = _Polygon([_Vertex(_Vector(x, y, 0), None),
                         _Vertex(_Vector(x, 0, 0), None),
                         _Vertex(_Vector(x, 0, -depth), None),
                         _Vertex(_Vector(x, y, -depth), None)])


        pol7 = _Polygon([_Vertex(_Vector(0,0,-depth), None),
                          _Vertex(_Vector(x, 0, -depth), None),
                          _Vertex(_Vector(x, y, -depth), None),
                          _Vertex(_Vector(0, y, -depth), None)])
        
        pols.append(pol3)
        pols.append(pol4)
        pols.append(pol5)
        pols.append(pol6)
        pols.append(pol7)
        
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

        
