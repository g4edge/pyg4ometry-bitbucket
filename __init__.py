from Reader import Reader
from CSG import *
import Model
import Parser

__all__ = ['Reader','CSG']


"""
NAME
pyfluka - Among among other things, this can be used to store a Fluka model
to be stored as a python object.  In addition to basic introspection
features, it also supports the conversion of the regions to GDML
volumes.

Fluka uses a right-handed coordinate system.

"""
