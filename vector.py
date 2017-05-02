import numpy as _np

class Three(_np.ndarray):
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

    def parallel_to(self, other, tolerance=1e-10):
        """
        Check if instance is parallel to some other vector, v
        """
        if _np.linalg.norm(_np.cross(self, other)) < tolerance:
            return True
        else:
            return False


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
    if not _np.array_equal(
            _np.allclose(rotation_matrix.T.dot(rotation_matrix)), _np.eye(3)):
        raise RuntimeError("Rotation matrix is not orthogonal!")
    return rotation_matrix

def angles_from_matrix(matrix):
    '''
    Returns the Tait-Bryan (Euler) angles, sequence = (x-y-z)
    for a given rotation matrix.

    Source:
    http://www.staff.city.ac.uk/~sbbh653/publications/euler.pdf

    Parameters:
    matrix -- a numpy matrix to extract the angles from.
    '''

    # Get the relevant elements from the matrix.
    R_11 = matrix.item(0)
    R_12 = matrix.item(1)
    R_13 = matrix.item(2)
    R_21 = matrix.item(3)
    R_31 = matrix.item(6)
    R_32 = matrix.item(7)
    R_33 = matrix.item(8)

    if (R_31 != -1 and R_31 != 1):
        y_rotation = -_np.arcsin(R_31)
        cosine_y_rotation = _np.cos(y_rotation)

        x_rotation = _np.arctan2(R_32 / cosine_y_rotation,
                                 R_33 / cosine_y_rotation)
        z_rotation = _np.arctan2(R_21 / cosine_y_rotation,
                                 R_11 / cosine_y_rotation)

    elif R_31 == -1:
        x_rotation = _np.arctan2(R_12,
                                 R_13)
        y_rotation = _np.pi / 2.
        z_rotation = 0.0
    elif R_31 == 1:
        x_rotation =  _np.arctan2(-R_12,
                                  -R_13)
        y_rotation = -_np.pi / 2
        z_rotation = 0.0
    return [x_rotation, y_rotation, z_rotation]

def rotation_between_vectors(vector_1, vector_2):
    matrix = _rot_matrix_between_vectors(vector_1, vector_2)
    return _get_angles_from_matrix(matrix)
