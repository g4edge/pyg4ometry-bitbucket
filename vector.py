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


def rot_matrix_between_vectors(vector_1, vector_2):
    """
    Returns the rotation matrix that rotates vector_1 to parallel to
    vector_2.

    Useful for ensuring a given face points in a certain
    direction.

    Parameters
    ----------
    vector_1 : Array-like 3-vector.

    """
    # Trivial cases that the algorithm otherwise can't handle:
    if vector_1.parallel_to(vector_2):
        return eye(3)
    elif -vector_1.parallel_to(vector_2):
        return -eye(3)
    # Get the axis to rotate around and the angle to rotate by:
    axis = (_np.cross(vector_1,
                      vector_2)
            / _np.linalg.norm(_np.cross(vector_1,
                                        vector_2)))
    angle = _np.arccos(_np.dot(vector_1,
                               vector_2)
                       / (_np.linalg.norm(vector_1)
                          * _np.linalg.norm(vector_2)))

    # Construct the skew-symmetric cross product matrix.
    cross_matrix = _np.matrix([[0,       -axis[2],  axis[1]],
                               [axis[2],       0,  -axis[0]],
                               [-axis[1], axis[0],        0]])
    # Rodrigues' rotation formula.
    rotation_matrix = (_np.eye(3)
                       + (_np.sin(angle)
                          * cross_matrix)
                       + ((1 - _np.cos(angle))
                          * cross_matrix
                          * cross_matrix))
    if not vector_2.parallel_to(
            rotation_matrix.dot(vector_1).view(Three).reshape(3)):
        raise RuntimeError("Rotation matrix doesn't map vector onto other!")
    if not _np.allclose(rotation_matrix.T.dot(rotation_matrix), _np.eye(3)):
        raise RuntimeError("Rotation matrix is not orthogonal!")
    return rotation_matrix

def rotation_between_vectors(vector_1, vector_2):
    matrix = _rot_matrix_between_vectors(vector_1, vector_2)
    return _get_angles_from_matrix(matrix)

def tb_angles_from(vector_1, vector_2):
    """
    Return the Tait-Bryan angles [x, y, z] (order: x -> y -> z)
    """

    matrix = rot_matrix_between_vectors(vector_1, vector_2)
    angles = _trf.matrix2tbxyz(matrix)
    resultant = _trf.tbxyz2matrix(angles).dot(vector_1).view(Three).reshape(3)
    assert resultant.parallel_to(vector_2)
    return angles
