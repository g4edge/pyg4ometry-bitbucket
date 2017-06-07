import numpy as _np

from pygdml import transformation as _trf

class Three(_np.ndarray):
    def __new__(cls, *coordinates):
        # If an array-like of 3:
        if (_np.shape(coordinates) == (1, 3)):
            obj = _np.asarray(coordinates[0], dtype=float).view(cls)
        elif _np.shape(coordinates) == (3,): # If supplied as x, y, z
            obj = _np.asarray(coordinates, dtype=float).view(cls)
        else:
            raise TypeError("Unknown construction: %s" % (coordinates,))
        return obj

    @property
    def x(self):
        return self[0]

    @x.setter
    def y(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[0] = value

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[0] = value

    def parallel_to(self, other, tolerance=1e-10):
        """
        Check if instance is parallel to some other vector, v
        """
        if _np.linalg.norm(_np.cross(self, other)) < tolerance:
            return True
        else:
            return False

    @property
    def unit(self):
        """
        Get this as a unit vector.
        """
        return self/_np.linalg.norm(self)

    @property
    def length(self):
        """
        vector length (l2 norm)

        """
        return _np.linalg.norm(self)
