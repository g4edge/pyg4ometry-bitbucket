from collections import namedtuple
import logging as _logging
import math as _math
import numpy as _np
from numpy import pi as _pi

import pygdml as _pygdml

INFINITE_SIZE = 1e8 # mm
_bodies_logger = _logging.getLogger(__name__)

_centre = namedtuple("centre", ['x','y','z'])
_rotation = namedtuple("rotation", ['x','y','z'])

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

    def _rotations_from_directions(self,
                                   x_direction,
                                   y_direction,
                                   z_direction):

        norm  = _np.linalg.norm([x_direction, y_direction, z_direction])
        x_rotation = _math.acos(x_direction/norm)
        y_rotation = _math.acos(y_direction/norm)
        z_rotation = _math.acos(z_direction/norm)

        return _rotation(x_rotation, y_rotation, z_rotation)

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
        Parallelepiped (cuboid).  Returns named tuple. with members x,y and z.
        '''

        centre_x = (self.parameters.x_max + self.parameters.x_min)*0.5
        centre_y = (self.parameters.y_max + self.parameters.y_min)*0.5
        centre_z = (self.parameters.z_max + self.parameters.z_min)*0.5

        centre = _centre(centre_x, centre_y, centre_z)

        return centre

    def get_rotation(self):
        return _rotation(0,0,0)

    def _extent(self):
        return max(self.parameters)

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


class BOX(_BodyBase):

    def __init__(self, name, parameters, expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(BOX, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        pass

    def get_rotation(self):
        pass

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        pass


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
        centre = _centre(self.parameters.v_x,
                         self.parameters.v_y,
                         self.parameters.v_z)
        return centre

    def get_rotation(self):
        return _rotation(0,0,0)

    def _get_scale(self):
        return (max(self.parameters.v_x,
                    self.parameters.v_y,
                    self.parameters.v_z)
                + self.parameters.radius)
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
        return None

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.
        '''
        centre_x = self.parameters.v_x + self.parameters.h_x * 0.5
        centre_y = self.parameters.v_y + self.parameters.h_y * 0.5
        centre_z = self.parameters.v_z + self.parameters.h_z * 0.5

        return _centre(centre_x, centre_y, centre_z)

    def get_rotation(self):
        # Choose the cylinder face pointing in the +z direction to
        # have the coordinates (v_x, v_y, v_z), and point in the
        # direction -(h_x, h_y, h_z)
        initial_vector = _np.array([0,0,1])
        # Negate the vector as I want it facing outwards.
        plane_vector = -_np.array([self.parameters.h_x,
                                   self.parameters.h_y,
                                   self.parameters.h_z])
        rotation = _get_rotation_matrix_between_vectors(initial_vector,
                                                        plane_vector)
        angles = _get_angles_from_matrix(rotation)
        return _rotation(*angles)

    def _get_scale(self):
        length = _np.linalg.norm([self.parameters.h_x,
                                  self.parameters.h_y,
                                  self.parameters.h_z])
        return max(self.parameters.v_x,
                   self.parameters.v_y,
                   self.parameters.v_z,
                   length)

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

        return _centre(centre_x, centre_y, centre_z)

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
        start_to_end_face = _get_rotation_matrix_between_vectors(start_face,
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
        middle_to_end_major = _get_rotation_matrix_between_vectors(middle_major,
                                                                   end_major)

        resulting_matrix = middle_to_end_major.dot(start_to_end_face)

        angles = _get_angles_from_matrix(resulting_matrix)
        return _rotation(*angles)

    # def get_rotation(self):
    #     # vector starts out at [0,-
    #     start_vector = [1,1,1]
    #     end_vector =

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

        # Useful derived parameters for later:
        self._length = _np.linalg.norm([self.parameters.major_to_minor_x,
                                        self.parameters.major_to_minor_y,
                                        self.parameters.major_to_minor_z])

        self._major_to_minor_vector = _np.array([self.parameters.major_to_minor_x,
                                                 self.parameters.major_to_minor_y,
                                                 self.parameters.major_to_minor_z])

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
        major_centre_vector = _np.array([self.parameters.centre_major_x,
                                         self.parameters.centre_major_y,
                                         self.parameters.centre_major_z])
        centre = major_centre_vector + 0.5 * self._major_to_minor_vector
        return _centre(*centre)

    def get_rotation(self):
        # At the start, the major face is pointing at -z.
        start_vector = _np.array([0,0,-1])
        # We want the major face pointing in the opposite direction to
        # major_to_minor_vector.
        end_vector = -self._major_to_minor_vector

        # Get the matrix that will give us this rotation
        start_to_end_matrix = _get_rotation_matrix_between_vectors(start_vector,
                                                                   end_vector)
        # Get the euler angles from this matrix.
        start_to_end_angles = _get_angles_from_matrix(start_to_end_matrix)
        return _rotation(*start_to_end_angles)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        # Choose to put the major face at -z.  The above
        # get_rotation method relies on this choice.
        return _pygdml.solid.Cons(self.name,
                                 0.0,
                                 self.parameters.major_radius,
                                 0.0,
                                 self.parameters.minor_radius,
                                 0.5 * self._length,
                                 0.0,
                                 2*_pi)


class ELL(_BodyBase):

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(ELL, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        pass

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        pass


class WED(_BodyBase):

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(WED, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        pass

    def get_rotation(self):
        pass

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        pass


class RAW(_BodyBase):

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(RAW, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        pass

    def get_rotation(self):
        pass

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        pass


class ARB(_BodyBase):

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(ARB, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        pass

    def get_rotation(self):
        pass

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        pass


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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_z'])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = 0.0
        centre_y = 0.0
        centre_z = self.parameters.v_z - (self.scale * 0.5)
        return _centre(centre_x, centre_y, centre_z)

    def get_rotation(self):
        return _rotation(0,0,0)

    def _get_scale(self):
        return self.parameters.v_z

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_y'])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = 0.0
        centre_y = self.parameters.v_y - (self.scale * 0.5)
        centre_z = 0.0
        return _centre(centre_x, centre_y, centre_z)

    def get_rotation(self):
        return _rotation(0,0,0)

    def _get_scale(self):
        return self.parameters.v_y

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_x'])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = self.parameters.v_x - (self.scale * 0.5)
        centre_y = 0.0
        centre_z = 0.0
        return _centre(centre_x, centre_y, centre_z)

    def get_rotation(self):
        return _rotation(0,0,0)

    def _get_scale(self):
        return self.parameters.v_x

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["x_direction",
                                                         "y_direction",
                                                         "z_direction",
                                                         "x_position",
                                                         "y_position",
                                                         "z_position"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        # The centre of the object will not, of course, be a point on
        # the surface of the "plane" (Box).  The centre required for
        # the face to lie on the provided point then needs to be
        # found.
        direction_norm = _np.linalg.norm([self.parameters.x_direction,
                                          self.parameters.y_direction,
                                          self.parameters.z_direction])

        # This is the value that we can multiply the direction vector
        # by to get it pointing towards the desired centre of the box.
        scaling_factor = -0.5 * self.scale / direction_norm

        centre_x = (scaling_factor
                    * self.parameters.x_direction
                    + self.parameters.x_position)
        centre_y = (scaling_factor
                    * self.parameters.y_direction
                    + self.parameters.y_position)
        centre_z = (scaling_factor
                    * self.parameters.z_direction
                    + self.parameters.z_position)

        return _centre(centre_x, centre_y, centre_z)

    def get_rotation(self):
        # Choose the face pointing in the direction of the positive
        # z-axis to make the face of the plane.
        initial_vector = _np.array([0,0,1])
        plane_vector = _np.array([self.parameters.x_direction,
                                  self.parameters.y_direction,
                                  self.parameters.z_direction])

        # Get the rotation matrix that maps initial_vector to plane_vector
        rotation = _get_rotation_matrix_between_vectors(initial_vector,
                                                        plane_vector)

        angles = _get_angles_from_matrix(rotation)
        return _rotation(*angles)

    def _get_scale(self):
        return self.scale
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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_y",
                                                         "centre_z",
                                                         "radius"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return _centre(0.0, self.parameters.centre_y, self.parameters.centre_z)

    def get_rotation(self):
        return _rotation(0.0, 0.5 * _pi, 0.0)

    def _get_scale(self):
        return self.scale

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_x",
                                                         "centre_z",
                                                         "radius"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return _centre(self.parameters.centre_x, 0.0, self.parameters.centre_z)

    def get_rotation(self):
        return _rotation(0.5 * _pi, 0.0, 0.0)

    def _get_scale(self):
        return self.scale
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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_x",
                                                         "centre_y",
                                                         "radius"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return _centre(self.parameters.centre_x,
                       self.parameters.centre_y,
                       0.0)

    def get_rotation(self):
        return _rotation(0.0, 0.0, 0.0)

    def _get_scale(self):
        return self.scale

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_y",
                                                         "centre_z",
                                                         "semi_axis_y",
                                                         "semi_axis_z"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return _centre(0.0, self.parameters.centre_y, self.parameters.centre_z)

    def get_rotation(self):
        return _rotation(0.0, 0.5 * _pi, 0.0)

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_z",
                                                         "centre_x",
                                                         "semi_axis_z",
                                                         "semi_axis_x"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return _centre(self.parameters.centre_x, 0.0, self.parameters.centre_z)

    def get_rotation(self):
        return _rotation(0.5 * _pi, 0.0, 0.0)

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
        self.scale = INFINITE_SIZE

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ["centre_x",
                                                         "centre_y",
                                                         "semi_axis_x",
                                                         "semi_axis_y"])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        return _centre(self.parameters.centre_x,
                       self.parameters.centre_y,
                       0.0)

    def get_rotation(self):
        return _rotation(0.0, 0.0, 0.0)

    def _extent(self):
        return max(self.parameters)

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        return _pygdml.solid.EllipticalTube(self.name,
                                           self.parameters.semi_axis_y,
                                           self.parameters.semi_axis_x,
                                           0.5 * self.scale)


class QUA(_BodyBase):

    def __init__(self, name,
                 parameters,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):
        super(QUA, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)
        self._set_parameters(parameters)

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    @_BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        pass

    def get_rotation(self):
        pass

    @_BodyBase._parameters_in_mm
    @_gdml_logger
    def get_as_gdml_solid(self):
        pass


class Translation(object):
    def __init__(self, delta_x, delta_y, delta_z):
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_z = delta_z


class Transformation(object):
    pass


class Expansion(object):
    def __init__(self, scaling_factor):
        self.scaling_factor = scaling_factor

def _rotations_between_vectors(vector_1, vector_2):
    matrix = _get_rotation_matrix_between_vectors(vector_1, vector_2)
    return _get_angles_from_matrix(matrix)

def _get_rotation_matrix_between_vectors(vector_1, vector_2):
    """
    Returns the rotation matrix that rotates vector_1 to parallel to
    vector_2.

    Useful for ensuring a given face points in a certain
    direction.

    Parameters
    ----------
    vector_1 : Array-like 3-vector.

    """
    # Normalise input vectors (rot matrix won't be orthogonal otherwise)
    vector_1 = vector_1 / _np.linalg.norm(vector_1)
    vector_2 = vector_2 / _np.linalg.norm(vector_2)

    cross_product = _np.cross(vector_1, vector_2)
    cosine = float(_np.dot(vector_1, vector_2))
    sine = _np.linalg.norm(cross_product)

    identity = _np.identity(3)

    # Check for trivial cases that Rodrigues' can't handle
    if cosine == 1.0: # then they are already parallel
        return identity
    elif cosine == -1.0: # then they are anti-parallel
        return -identity

    # Construct the skew-symmetric cross product matrix.
    first_row = [0, -cross_product[2], -cross_product[1]]
    second_row = [cross_product[2], 0, -cross_product[0]]
    third_row = [-cross_product[1], cross_product[0], 0]
    cross_matrix = _np.matrix([first_row, second_row, third_row])

    # Rodrigues' rotation formula.
    rotation_matrix = (identity + cross_matrix
                       + (cross_matrix
                          * cross_matrix
                          * (1 - cosine)
                          / (sine**2)))

    return rotation_matrix

def _get_angles_from_matrix(matrix):
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
        y_rotation = _pi / 2.
        z_rotation = 0.0
    elif R_31 == 1:
        x_rotation =  _np.arctan2(-R_12,
                                  -R_13)
        y_rotation = -_pi / 2
        z_rotation = 0.0
    return [x_rotation, y_rotation, z_rotation]


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
    "XYP": "Infinite Half-space",
    "XZP": "Infinite Half-space",
    "YCC": "Infinite Circular Cylinder parallel to the y-axis",
    "YEC": "Infinite Elliptical Cylinder parallel to the y-axis",
    "YZP": "Infinite Half-space",
    "ZCC": "Infinite Circular Cylinder parallel to the z-axis",
    "ZEC": "Infinite Elliptical Cylinder parallel to the z-axis"
}
