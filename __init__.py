from Reader import Reader
from CSG import *
from .model import Model
import geometry
import Parser
import materials
import vector

__all__ = ['Reader','CSG']


"""
NAME
pyfluka - Among among other things, this can be used to store a Fluka model
to be stored as a python object.  In addition to basic introspection
features, it also supports the conversion of the regions to GDML
volumes.

Fluka uses a right-handed coordinate system.

"""

from .model import Model
from .geometry import (PLA, RCC, RPP, SPH, TRC, XCC, XEC,
                       XYP, XZP, YCC, YEC, YZP, ZCC, ZEC,
                       Region, Zone)

__all__ = ['Model',
           "PLA", "RCC", "RPP", "SPH", "TRC", "XCC", "XEC",
           "XYP", "XZP", "YCC", "YEC", "YZP", "ZCC", "ZEC",
           "Region", "Zone"]
