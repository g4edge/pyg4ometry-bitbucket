import numpy as _np

class ThreeVector(_np.ndarray):
    def __new__(cls, *coordinates):
        if (len(coordinates) == 1  # If coerced from another _np.array
            and isinstance(coordinates[0], _np.ndarray)):
            obj = _np.asarray(coordinates[0]).view(cls)
        elif len(coordinates) == 3: # If supplied as x,y,z
            obj = _np.asarray(coordinates).view(cls)
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
