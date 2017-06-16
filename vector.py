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

    def __eq__(self, other):
        return (self.x == other.x
                and self.y == other.y
                and self.z == other.z)

    def __ne__(self, other):
        return not self == other


def point_on_line_closest_to_point(point, point_on_line, direction):
    """
    Line is defined in terms of two vectors:  a point on the line and
    the direction of the line.

    point is the point with which the distance to the line is to be
    minimised.

    """
    # Algorithm pinched from:

    # Get another point on the line:
    p0 = point
    p1 = point_on_line
    a = direction

    # In the name of rapidity, implementation pinched from:
    # https://math.stackexchange.com/questions/13176/how-to-find-a-point-on-a-line-closest-to-another-given-point
    t = ((- a.x * (p1.x - p0.x) - a.y * (p1.y - p0.y) - a.z * (p1.z - p0.z))
         / (a.x * a.x + a.y * a.y + a.z * a.z))
    pt = p1 + t * a

    return pt
