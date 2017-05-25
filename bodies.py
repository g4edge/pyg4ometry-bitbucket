from collections import namedtuple
import logging as _logging
import math as _math
import numpy as _np
from numpy import pi as _pi

import pygdml as _pygdml
from pygdml import transformation as _trf
import vector


def _gdml_logger(f):
    # Logging the construction of the gdml solids.
    def wrapped(self):
        # Parameters for the gdml solids that are used here in bodies.
        gdml_parameters = {"Box": ["pX", "pY", "pZ"],
                           "Orb": ["pRMax"],
                           "Tubs": ["pRMin", "pRMax", "pDz", "pSPhi", "pDPhi"],
                           "Cons": ["pRmin1", "pRmax1", "pRmin2",
                                    "pRmax2", "pDz", "pSPhi", "pDPhi"],
                           "EllipticalTube": ["pDx", "pDy", "pDz"]}
        solid = f(self)
        solid_type = type(solid).__name__
        parameters =  [getattr(solid, parameter)
                   for parameter in gdml_parameters[solid_type]]
        logger = _logging.getLogger("pyfluka.bodies.%s" % type(self).__name__)
        logger.debug("solid: type=%s; name=%s; rest=%s",
                     solid_type,
                     solid.name,
                     parameters)
        return solid
    return wrapped


class _BodyBase(object):
    '''
    A class representing a body as defined in Fluka.
    get_body_as_gdml_solid() returns the body as a pygdml.solid
    '''

    def __init__(self,
                 name,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):

        self.name = name
        self._expansion_stack = expansion_stack
        self._translation_stack = translation_stack
        self._transformation_stack = transformation_stack
        # Named tuple constructor for later use.

    def set_transformation_definitions(self, something):
        pass

    @staticmethod
    def _parameters_in_mm(func):
        '''
        Chances parameter units to millimetres local only to the
        function "func".
        Tuples are supposed to be immutable, but this saves a
        dependency.
        '''
        def wrapped(self):
            mm = 10.0
            fields = self.parameters._fields
            parameters_in_mm = [i * mm for i in self.parameters]
            # Redefine the named tuple so the returned object is the same shape
            parameters_type = namedtuple("Parameters", fields)
            self.parameters = parameters_type(*parameters_in_mm)
            if hasattr(self, "scale"):
                self.scale *= mm
            # Call function
            output = func(self)
            # Put the coordinates back to cm.
            parameters_in_cm = [i * 1/mm for i in self.parameters]
            self.parameters = parameters_type(*parameters_in_cm)
            if hasattr(self, "scale"):
                self.scale /= mm
            return output

        return wrapped


class _InfiniteSolid(object):
    # Infinite bodies are factories for themselves, allowing
    # for dynamic infinite scale for a common underlying body.
    # This is useful because an infinite body maybe used multiple
    # times, but in one usecase may need to be much bigger than in
    # another.  This essentially allows for multiple bodies from a
    # single Fluka definition.
    def __call__(self, scale):
        out = self
        out.scale = scale
        return out

class RPP(_BodyBase):
    '''
    An RPP is a rectangular parallelpiped (a cuboid).
    '''
    def __init__(self, name, parameters, expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(RPP, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)

        self._set_parameters(parameters)

        if (self.parameters.x_min > self.parameters.x_max or
            self.parameters.y_min > self.parameters.y_max or
            self.parameters.z_min > self.parameters.z_max):
            raise Warning("This RPP \"" + name + "\" has mins larger than "
                          "its maxes.\n It is ignored in Fluka but "
                          "won't be ignored here!")


    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['x_min',
                                                         'x_max',
                                                         'y_min',
                                                         'y_max',
                                                         'z_min',
                                                         'z_max'])
        self.parameters = self._ParametersType(*parameters)
        return None

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Return the coordinates of the centre of the Rectangular
        Parallelepiped (cuboid).
        '''

        centre_x = 0.5 * (self.parameters.x_max + self.parameters.x_min)
        centre_y = 0.5 * (self.parameters.y_max + self.parameters.y_min)
        centre_z = 0.5 * (self.parameters.z_max + self.parameters.z_min)

        centre = vector.Three(centre_x, centre_y, centre_z)

        return centre

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0,0,0)

    def extent(self):
        return max([self.parameters.x_max - self.parameters.x_min,
                    self.parameters.y_max - self.parameters.y_min,
                    self.parameters.z_max - self.parameters.z_min])


    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        '''
        Construct a pygdml Box from this body definition
        '''
        x_length = abs(self.parameters.x_max - self.parameters.x_min)
        y_length = abs(self.parameters.y_max - self.parameters.y_min)
        z_length = abs(self.parameters.z_max - self.parameters.z_min)

        return _pygdml.solid.Box(self.name,
                                 0.5 * x_length,
                                 0.5 * y_length,
                                 0.5 * z_length)


class SPH(_BodyBase):
    def __init__(self, name, parameters, expansion_stack,
                 translation_stack,
                 transformation_stack):

        super(SPH, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)

        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        # A named tuple for representing the geometry parameters associated with
        # the object.
        self._ParametersType = namedtuple("Parameters", ['v_x',
                                                         'v_y',
                                                         'v_z',
                                                         'radius'])
        self.parameters = self._ParametersType(*parameters)
        return None

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.
        '''
        centre = vector.Three(self.parameters.v_x,
                              self.parameters.v_y,
                              self.parameters.v_z)
        return centre

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0,0,0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        '''
        Construct a pgydml orb (full, solid sphere) solid.
        '''
        return _pygdml.solid.Orb(self.name, self.parameters.radius)


class RCC(_BodyBase):
    '''
    Right-angled Circular Cylinder

    Parameters:
    v_(x,y,z) = coordinates of the centre of one of the circular planes
    faces
    h_(x,y,z) = components of vector pointing in the direction of the
    other plane face, with magnitude equal to the cylinder length.
    radius    = cylinder radius
    '''

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(RCC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_x',
                                                         'v_y',
                                                         'v_z',
                                                         'h_x',
                                                         'h_y',
                                                         'h_z',
                                                         'radius'])
        self.parameters = self._ParametersType(*parameters)
        self.face_centre = vector.Three(self.parameters.v_x,
                                        self.parameters.v_y,
                                        self.parameters.v_z)
        self.direction = vector.Three(self.parameters.h_x,
                                      self.parameters.h_y,
                                      self.parameters.h_z)

        return None

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.
        '''

        return self.face_centre + 0.5 * self.direction

    def get_rotation_matrix(self):
        initial = [0, 0, 1]
        final = -self.direction
        return _trf.matrix_from(initial, final)

    def get_rotation(self):
        # Choose the cylinder face pointing in the +z direction to
        # become the face with coordinates (v_x, v_y, v_z), and point in the
        # direction -(h_x, h_y, h_z).
        initial_vector = vector.Three([0.0, 0.0, 1.0])
        # Negate the vector as I want it facing outwards to match the above.
        final_vector = -vector.Three(self.parameters.h_x,
                                     self.parameters.h_y,
                                     self.parameters.h_z)
        angles = vector.tb_angles_from(initial_vector, final_vector)
        # Assert that the matrix does indeed take map the initial
        # vector to the final vector.
        assert (_trf.tbxyz2matrix(angles).dot(initial_vector)
                .view(vector.Three).reshape(3).parallel_to(final_vector))
        return vector.Three(*angles)

    def extent(self):
        centre_max = max(abs(vector.Three(self.parameters.v_x,
                                          self.parameters.v_y,
                                          self.parameters.v_z)))
        length = _np.linalg.norm([self.parameters.h_x,
                                  self.parameters.h_y,
                                  self.parameters.h_z])
        return centre_max + length

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        length = _np.linalg.norm([self.parameters.h_x,
                                  self.parameters.h_y,
                                  self.parameters.h_z])

        return _pygdml.solid.Tubs(self.name, 0.0,
                                 self.parameters.radius,
                                 length * 0.5,
                                 0.0,
                                 2*_pi)


class REC(_BodyBase):
    """
    NOT IMPLEMENTED

    Class representing the Right Elliptical Cylinder of Fluka.

    Parameters:
    face_centre_x : x-coordinate of the centre of one of the faces.
    face_centre_y : y-coordinate of the centre of one of the faces.
    face_centre_z : z-coordinate of the centre of one of the faces.

    to_other_face_x : x-component of the vector pointing from
                      face_centre to the other face.
    to_other_face_y : y-component of the vector pointing from
                      face_centre to the other face.
    to_other_face_z : z-component of the vector pointing from
                      face_centre to the other face.
    The length of the vector to_other_face is the length of the
    elliptical cylinder.

    semi_minor_x : x-component of the semi-minor axis.
    semi_minor_y : y-component of the semi-minor axis.
    semi_minor_z : z-component of the semi-minor axis.
    The length of the vector semi_minor is the length of the
    semi-minor axis.

    semi_major_x : x-component of the semi-major axis.
    semi_major_y : y-component of the semi-major axis.
    semi_major_z : z-component of the semi-major axis.
    The length of the vector semi_major is the length of the
    semi-major axis.
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(REC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        raise BodyNotImplementedError(self)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["face_centre_x",
                                                         "face_centre_y",
                                                         "face_centre_z",
                                                         "to_other_face_x",
                                                         "to_other_face_y",
                                                         "to_other_face_z",
                                                         "semi_minor_x",
                                                         "semi_minor_y",
                                                         "semi_minor_z",
                                                         "semi_major_x",
                                                         "semi_major_y",
                                                         "semi_major_z"])
        self.parameters = self._ParametersType(*parameters)


    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = (self.parameters.face_centre_x
                    + self.parameters.to_other_face_x * 0.5)
        centre_y = (self.parameters.face_centre_y
                    + self.parameters.to_other_face_y * 0.5)
        centre_z = (self.parameters.face_centre_z
                    + self.parameters.to_other_face_z * 0.5)

        return vector.Three(centre_x, centre_y, centre_z)

    def get_rotation_matrix(self):
        pass

    def get_rotation(self):
        # Perform 2 rotations:
        # First to get the faces pointing in the correct direction.
        # Second to get the major axis pointing in the correct direction.
        # The minor axis will then also be pointing in the correct direction.

        # The unrotated EllipticalTube initially lies parallel to the
        # z-axis.
        # Choose the face pointing in the -z direction to become
        # face_centre.  This will point in the direction
        # anti-parallel to_other_face.
        start_face = _np.array([0, 0, +1])
        # Negate the vector as I want it facing outwards.
        end_face = _np.array([self.parameters.to_other_face_x,
                              self.parameters.to_other_face_y,
                              self.parameters.to_other_face_z])
        # The matrix rotating the starting face to parallel to the desired.
        start_to_end_face = vector.rot_matrix_between_vectors(start_face,
                                                              end_face)
        # The major-axis starts in the positive y direction.
        start_major = _np.array([0, 1, 0])
        # The major-axis after being rotated by the above matrix.
        middle_major = start_to_end_face.dot(start_major)
        # The output of "dot" is a matrix, so convert back to an array.
        middle_major = _np.squeeze(_np.asarray(middle_major))
        # The desired final vector points in the semi_major direction
        end_major = _np.array([self.parameters.semi_major_x,
                               self.parameters.semi_major_y,
                               self.parameters.semi_major_z])
        middle_to_end_major = vector.rot_matrix_between_vectors(middle_major,
                                                                end_major)

        resulting_matrix = middle_to_end_major.dot(start_to_end_face)

        angles = _trf.matrix2tbxyz(resulting_matrix)
        return vector.Three(*angles)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        # EllipticalTube is defined in terms of half-lengths in x, y,
        # and z.  Choose semi_major to start in the positive y direction.
        semi_minor = _np.linalg.norm([self.parameters.semi_minor_x,
                                      self.parameters.semi_minor_y,
                                      self.parameters.semi_minor_z])

        semi_major = _np.linalg.norm([self.parameters.semi_major_x,
                                      self.parameters.semi_major_y,
                                      self.parameters.semi_major_z])

        length = _np.linalg.norm([self.parameters.to_other_face_x,
                                  self.parameters.to_other_face_y,
                                  self.parameters.to_other_face_z])

        return _pygdml.solid.EllipticalTube(self.name,
                                            semi_minor,
                                            semi_major,
                                            length * 0.5)


class TRC(_BodyBase):
    """
    Truncated Right-angled Cone.

    Parameters
    ----------

    centre_major_x : x-coordinate of the centre of the larger face.
    centre_major_y : y-coordinate of the centre of the larger face.
    centre_major_z : z-coordinate of the centre of the larger face.

    major_to_minor_x : x_coordinator of the vector pointing from the major
                       to minor face.
    major_to_minor_y : y_coordinator of the vector pointing from the major
                       to minor face.
    major_to_minor_z : z_coordinator of the vector pointing from the major
                       to minor face.
    The length of the major_to_minor vector is the length of the resulting
    cone.

    major_radius : radius of the larger face.
    minor_radius : radius of the smaller face.
    """

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(TRC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)
        self.major_centre = vector.Three([self.parameters.centre_major_x,
                                          self.parameters.centre_major_y,
                                          self.parameters.centre_major_z])
        self.major_to_minor = vector.Three([self.parameters.major_to_minor_x,
                                            self.parameters.major_to_minor_y,
                                            self.parameters.major_to_minor_z])
        self.length = self.major_to_minor.length

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['centre_major_x',
                                                         'centre_major_y',
                                                         'centre_major_z',
                                                         'major_to_minor_x',
                                                         'major_to_minor_y',
                                                         'major_to_minor_z',
                                                         'major_radius',
                                                         'minor_radius'])
        self.parameters = self._ParametersType(*parameters)
        return None

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return self.major_centre + 0.5 * self.major_to_minor

    def get_rotation_matrix(self):
        # We choose in the as_gdml_solid method to place the major at
        # -z, and the major at +z, hence this choice of initial and
        # final vectors:
        initial = [0, 0, 1]
        final = self.major_to_minor
        return matrix_from(initial, final)

    def get_rotation(self):
        # At the start, the major face is pointing at +z toward the
        # minor face
        initial_vector = vector.Three([0,0,1])
        # Major to minor is pointing in the direction from -z to +z
        final_vector = self.major_to_minor

        angles = vector.tb_angles_from(initial_vector, final_vector)
        # Assert that the matrix does indeed take map the initial
        # vector to the final vector.
        assert (_trf.tbxyz2matrix(angles).dot(initial_vector)
                .view(vector.Three).reshape(3).parallel_to(final_vector))
        return vector.Three(*angles)

    def extent(self):
        length = _np.linalg.norm([self.parameters.major_to_minor_x,
                                  self.parameters.major_to_minor_y,
                                  self.parameters.major_to_minor_z])

        return max(abs(self.parameters.centre_major_x) + length,
                   abs(self.parameters.centre_major_y) + length,
                   abs(self.parameters.centre_major_z) + length,
                   self.parameters.minor_radius,
                   self.parameters.major_radius)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        # The first face of pygdml.Cons is located at -z, and the
        # second at +z.  Here choose to put the major face at -z.
        return _pygdml.solid.Cons(self.name,
                                  0.0,
                                  self.parameters.major_radius,
                                  0.0,
                                  self.parameters.minor_radius,
                                  0.5 * self.length,
                                  0.0,
                                  2*_pi)


class XYP(_BodyBase, _InfiniteSolid):
    '''
    Infinite plane perpendicular to the z-axis.
    '''
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(XYP, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_z'])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = 0.0
        centre_y = 0.0
        centre_z = self.parameters.v_z - (self.scale * 0.5)
        return vector.Three(centre_x, centre_y, centre_z)

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0,0,0)

    def extent(self):
        return abs(self.parameters.v_z)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class XZP(_BodyBase, _InfiniteSolid):
    '''
    Infinite plane perpendicular to the y-axis.
    '''
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(XZP, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_y'])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = 0.0
        centre_y = self.parameters.v_y - (self.scale * 0.5)
        centre_z = 0.0
        return vector.Three(centre_x, centre_y, centre_z)

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0,0,0)

    def extent(self):
        return abs(self.parameters.v_y)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class YZP(_BodyBase, _InfiniteSolid):
    '''
    Infinite plane perpendicular to the x-axis.
    '''
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(YZP, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_x'])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = self.parameters.v_x - (self.scale * 0.5)
        centre_y = 0.0
        centre_z = 0.0
        return vector.Three(centre_x, centre_y, centre_z)

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0,0,0)

    def extent(self):
        return abs(self.parameters.v_x)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class PLA(_BodyBase, _InfiniteSolid):
    """
    Generic infinite half-space.

    Parameters:
    x_direction (Hx) :: x-component of a vector of arbitrary length
                        perpendicular to the plane.  Pointing outside
                        of the space.
    y_direction (Hy) :: y-component of a vector of arbitrary length
                        perpendicular to the plane.  Pointing outside
                        of the space.
    z_direction (Hz) :: z-component of a vector of arbitrary length
                        perpendicular to the plane.  Pointing outside
                        of the space.
    x_position  (Vx) :: x-component of a point anywhere on the plane.
    y_position  (Vy) :: y-component of a point anywhere on the plane.
    z_position  (Vz) :: z-component of a point anywhere on the plane.
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(PLA, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["x_direction",
                                                         "y_direction",
                                                         "z_direction",
                                                         "x_position",
                                                         "y_position",
                                                         "z_position"])
        self.parameters = self._ParametersType(*parameters)
        self.perpendicular = vector.Three([self.parameters.x_direction,
                                           self.parameters.y_direction,
                                           self.parameters.z_direction])
        self.surface_point = vector.Three([self.parameters.x_position,
                                           self.parameters.y_position,
                                           self.parameters.z_position])

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        # This is the centre of the underlying gdml solid (i.e. won't
        # be on the surface, but set backwards by half length scale's amount.
        centre = (self.surface_point
                  - (0.5 * self.scale * self.perpendicular.unit))
        return centre

    def get_rotation_matrix(self):
        # Choose the face pointing in the direction of the positive
        # z-axis to make the face of the plane.
        initial = [0,0,1]
        final = self.perpendicular
        return _trf.matrix_from(initial, final)

    def get_rotation(self):
        # Choose the face pointing in the direction of the positive
        # z-axis to make the face of the plane.
        initial_vector = vector.Three([0,0,1])
        final_vector = self.perpendicular
        angles = vector.tb_angles_from(initial_vector, final_vector)
        return vector.Three(*angles)

    def extent(self):
        return max(abs(self.parameters.x_position),
                   abs(self.parameters.y_position),
                   abs(self.parameters.z_position))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class XCC(_BodyBase, _InfiniteSolid):
    """
    Infinite circular cylinder parallel to x-axis

    parameters:

    centre_y    -- y-coordinate of the centre of the cylinder
    centre_z    -- z-coordinate of the centre of the cylinder
    radius -- radius of the cylinder
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(XCC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_y",
                                                         "centre_z",
                                                         "radius"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return vector.Three(0.0, self.parameters.centre_y, self.parameters.centre_z)

    def get_rotation_matrix(self):
        # Rotate pi/2 about the y-axis.
        return _np.matrix([[ 0,  0, -1],
                           [ 0,  1,  0],
                           [ 1,  0,  0]])

    def get_rotation(self):
        return vector.Three(0.0, 0.5 * _pi, 0.0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Tubs(self.name, 0.0,
                                 self.parameters.radius,
                                 self.scale * 0.5,
                                 0.0,
                                 2*_pi)


class YCC(_BodyBase, _InfiniteSolid):
    """
    Infinite circular cylinder parallel to y-axis

    parameters:

    centre_x    -- x-coordinate of the centre of the cylinder
    centre_z    -- z-coordinate of the centre of the cylinder
    radius -- radius of the cylinder
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(YCC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_z",
                                                         "centre_x",
                                                         "radius"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return vector.Three(self.parameters.centre_x, 0.0, self.parameters.centre_z)

    def get_rotation_matrix(self):
        # Rotate by pi/2 about the x-axis.
        return _np.matrix([[ 1,  0,  0],
                           [ 0,  0,  1],
                           [ 0, -1,  0]])

    def get_rotation(self):
        return vector.Three(0.5 * _pi, 0.0, 0.0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Tubs(self.name,
                                 0.0,
                                 self.parameters.radius,
                                 self.scale * 0.5,
                                 0.0,
                                 2*_pi)


class ZCC(_BodyBase, _InfiniteSolid):
    """
    Infinite circular cylinder parallel to z-axis

    parameters:

    centre_x    -- x-coordinate of the centre of the cylinder
    centre_y    -- y-coordinate of the centre of the cylinder
    radius -- radius of the cylinder
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(ZCC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_x",
                                                         "centre_y",
                                                         "radius"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return vector.Three(self.parameters.centre_x,
                            self.parameters.centre_y,
                            0.0)

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0.0, 0.0, 0.0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.Tubs(self.name,
                                  0.0,
                                  self.parameters.radius,
                                  self.scale * 0.5,
                                  0.0,
                                  2*_pi)


class XEC(_BodyBase, _InfiniteSolid):
    """
    An infinite elliptical cylinder parallel to the x-axis.

    Parameters:

    centre_y (Ay) - y-coordinate of the centre of the ellipse face.
    centre_z (Az) - z-coordinate of the centre of the ellipse face.
    semi_axis_y (Ly) - semi-axis in the y-direction of the ellipse
    face.
    semi_axis_z (Lz) - semi-axis in the z-direction of the ellipse face.
    """

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(XEC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_y",
                                                         "centre_z",
                                                         "semi_axis_y",
                                                         "semi_axis_z"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return vector.Three(0.0, self.parameters.centre_y, self.parameters.centre_z)

    def get_rotation_matrix(self):
        # Rotate pi/2 about the y-axis.
        return _np.matrix([[ 0,  0, -1],
                           [ 0,  1,  0],
                           [ 1,  0,  0]])

    def get_rotation(self):
        return vector.Three(0.0, 0.5 * _pi, 0.0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                           self.parameters.semi_axis_z,
                                           self.parameters.semi_axis_y,
                                           0.5 * self.scale)


class YEC(_BodyBase, _InfiniteSolid):
    """
    An infinite elliptical cylinder parallel to the y-axis.

    Parameters:

    centre_z (Az) - z-coordinate of the centre of the ellipse face.
    centre_x (Ax) - x-coordinate of the centre of the ellipse face.
    semi_axis_z (Lz) - semi-axis in the z-direction of the ellipse face.
    semi_axis_x (Lx) - semi-axis in the x-direction of the ellipse face.
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(YEC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_z",
                                                         "centre_x",
                                                         "semi_axis_z",
                                                         "semi_axis_x"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return vector.Three(self.parameters.centre_x, 0.0, self.parameters.centre_z)

    def get_rotation_matrix(self):
        # Rotate by pi/2 about the x-axis.
        return _np.matrix([[ 1,  0,  0],
                           [ 0,  0,  1],
                           [ 0, -1,  0]])

    def get_rotation(self):
        return vector.Three(0.5 * _pi, 0.0, 0.0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                           self.parameters.semi_axis_x,
                                           self.parameters.semi_axis_z,
                                           0.5 * self.scale)


class ZEC(_BodyBase, _InfiniteSolid):
    """
    An infinite elliptical cylinder parallel to the z-axis.

    Parameters:

    centre_x (Ax) - x-coordinate of the centre of the ellipse face.
    centre_y (Ay) - y-coordinate of the centre of the ellipse face.
    semi_axis_x (Lx) - semi-axis in the x-direction of the ellipse face.
    semi_axis_y (Ly) - semi-axis in the y-direction of the ellipse face.
    """
    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(ZEC, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_x",
                                                         "centre_y",
                                                         "semi_axis_x",
                                                         "semi_axis_y"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return vector.Three(self.parameters.centre_x,
                            self.parameters.centre_y,
                            0.0)

    def get_rotation_matrix(self):
        return _np.matrix(_np.identity(3))

    def get_rotation(self):
        return vector.Three(0.0, 0.0, 0.0)

    def extent(self):
        return max(map(abs, self.parameters))

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                           self.parameters.semi_axis_x,
                                           self.parameters.semi_axis_y,
                                           0.5 * self.scale)


class BOX(_BodyBase):
    pass


class QUA(_BodyBase):
    pass

class ELL(_BodyBase):
    pass


class WED(_BodyBase):
    pass


class RAW(_BodyBase):
    pass


class ARB(_BodyBase):
    pass


class Region(object):
    """
    Class used for interfacing a Fluka region with a GDML volume.
    This class has the underlying pygdml volume payload, alongside its
    placement and rotation in the world volume, and a material.

    """
    # Encapsulating a region in this way allows individual regions to
    # be picked and
    def __init__(self, name, gdml_solid,
                 material="G4_Galactic",
                 position=[0, 0, 0],
                 rotation=[0, 0, 0]):
        self.name = name
        self.gdml_solid = gdml_solid
        self.material = material
        self.position = position
        self.rotation = rotation

    def view(self):
        """
        View this single region.  If a null mesh is encountered, try
        the view_debug method to see the problematic boolean operation.

        """
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                     "world-volume", None,
                                     1, False, "G4_NITROUS_OXIDE")

        self.add_to_volume(world_volume)
        world_volume.setClip()
        mesh = world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(mesh)
        viewer.view()

    def view_debug(self, first=None, second=None):
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                     "world-volume", None,
                                     1, False, "G4_NITROUS_OXIDE")
        self.add_to_volume(world_volume)
        try:
            world_volume.setClip()
            mesh = world_volume.pycsgmesh()
            print "Mesh was successful."
        except _pygdml.solid.NullMeshError as error:
            print error.message
            print "Debug:  Viewing consituent solids."
            self._view_null_mesh(error, first, second)

    def add_to_volume(self, volume):
        """
        Basically for adding to a world volume.

        """
        _pygdml.volume.Volume(_trf.reverse(self.rotation),
                              self.position,
                              self.gdml_solid,
                              self.name,
                              volume,
                              1,
                              False,
                              self.material)

    def _view_null_mesh(self, error, first, second):
        solid1 = error.solid.obj1
        solid2 = error.solid.obj2
        tra2 = error.solid.tra2

        world_box = _pygdml.solid.Box("world", 10000, 10000, 10000)
        world_volume = _pygdml.Volume([0, 0, 0], [0, 0, 0], world_box,
                                      "world-volume", None,
                                      1, False, "G4_NITROUS_OXIDE")
        if (first is None and second is None
            or first is True and second is True):
            volume1 = _pygdml.Volume([0, 0, 0], [0, 0, 0], solid1,
                                     solid1.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
            volume2 = _pygdml.Volume(_trf.reverse(tra2[0]), tra2[1], solid2,
                                     solid2.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
        elif first is True and second is not True:
            volume1 = _pygdml.Volume([0, 0, 0], [0, 0, 0], solid1,
                                     solid1.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
        elif second is True and first is not True:
            volume2 = _pygdml.Volume(_trf.reverse(tra2[0]), tra2[1], solid2,
                                     solid2.name, world_volume,
                                     1, False, "G4_NITROUS_OXIDE")
        elif first is False and second is False:
            raise RuntimeError("Must select at least one"
                               " of the two solids to view")
        world_volume.setClip()
        mesh = world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(mesh)
        viewer.view()

    def atomic_solids(self):
        """
        return a dictionary of the atomic solids (i.e. no boolean solids)
        making up this region.

        """
        solids = dict()
        def dump_iter(solid):
            if isinstance(solid, (_pygdml.solid.Intersection,
                                  _pygdml.solid.Subtraction,
                                  _pygdml.solid.Union)):
                dump_iter(solid.obj1)
                dump_iter(solid.obj2)
            else:
                solids[solid.name] = solid
        dump_iter(self.gdml_solid)
        return solids


class BodyNotImplementedError(Exception):
    def __init__(self, body):
        body_name = body.name
        body_type = type(body).__name__
        self.message = ("Body \"{}\" cannot be constructed.  Body type "
                        "\"{}\" is not supported!").format(body_name,
                                                           body_type)
        super(Exception, self).__init__(self.message)
        logger = _logging.getLogger("pyfluka.bodies.%s" % type(self).__name__)
        logger.exception("Body not instantiated: %s; type=%s", body_name, body_type)

code_meanings = {
    "ARB": "Abitrary Convex Polyhedron",
    "BOX": "General Rectangular Parallelepiped",
    "ELL": "Elippsoid of Revolution",
    "PLA": "Generic Infinite Half-space",
    "QUA": "Generic Quadric",
    "RAW": "Right Angle Wedge",
    "RCC": "Right Circular Cylinder",
    "REC": "Right Ellitpical Cylinder",
    "RPP": "Rectangular Parallelepiped",
    "SPH": "Sphere",
    "TRC": "Truncated Right Angle Cone",
    "WED": "Right Angle Wedge",
    "XCC": "Infinite Circular Cylinder parallel to the x-axis",
    "XEC": "Infinite Elliptical Cylinder parallel to the x-axis",
    "XYP": "Infinite Half-space perpendicular to the z-axis",
    "XZP": "Infinite Half-space perpendicular to the y-axis",
    "YCC": "Infinite Circular Cylinder parallel to the y-axis",
    "YEC": "Infinite Elliptical Cylinder parallel to the y-axis",
    "YZP": "Infinite Half-space perpendicular to the x-axis",
    "ZCC": "Infinite Circular Cylinder parallel to the z-axis",
    "ZEC": "Infinite Elliptical Cylinder parallel to the z-axis"
}
