from SolidBase import SolidBase as _SolidBase
from Wedge import Wedge as _Wedge
from ...pycsg.core import CSG as _CSG
from ...pycsg.geom import Vector as _Vector
from ...pycsg.geom import Vertex as _Vertex
from ...pycsg.geom import Polygon as _Polygon

import logging as _log
import numpy as _np

class Orb(_SolidBase):
    def __init__(self, name, pRMax, registry=None):

        """
        Constructs a solid sphere.

        Inputs:
           name:     string, name of the volume
           pRMax:    float, outer radius
        """
        self.type = 'Orb'
        self.name = name
        self.pRMax = pRMax

        self.dependents = []

        if registry:
            registry.addSolid(self)

    def __repr__(self):
        return "Orb : {} {}".format(self.name, self.pRMax)

    def pycsgmesh(self):
        _log.info("orb.antlr>")
        pRMax = float(self.pRMax)

        _log.info("orb.pycsgmesh>")
        mesh = _CSG.sphere(center=[0,0,0], radius=pRMax)
        return mesh
