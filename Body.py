from collections import namedtuple
import math as _math
import pygdml as pygdml

from IPython import embed

class BodyBase(object):
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
        self._centre = namedtuple("centre", ['x','y','z'])
        self._rotation = namedtuple("rotation", ['x_rotation',
                                                 'y_rotation',
                                                 'z_rotation'])

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
            # Call function
            output = func(self)
            # Put the coordinates back to cm.
            parameters_in_cm = [i * 1/mm for i in self.parameters]
            self.parameters = parameters_type(*parameters_in_cm)
            return output

        return wrapped

    @staticmethod
    def _rotations_from_directions(x_direction,
                                 y_direction,
                                 z_direction):

        norm  = _norm(x_direction, y_direction, z_direction)
        x_rotation = _math.acos(x_direction/norm)
        y_rotation = _math.acos(y_direction/norm)
        z_rotation = _math.acos(z_direction/norm)

        return self._rotation(x_rotation, y_rotation, z_rotation)


class RPP(BodyBase):
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

    @BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Return the coordinates of the centre of the Rectangular
        Parallelepiped (cuboid).  Returns named tuple. with members x,y and z.
        '''

        centre_x = (self.parameters.x_max + self.parameters.x_min)*0.5
        centre_y = (self.parameters.y_max + self.parameters.y_min)*0.5
        centre_z = (self.parameters.z_max + self.parameters.z_min)*0.5

        centre = self._centre(centre_x, centre_y, centre_z)

        return centre

    def get_rotation(self):
        x_direction = self.parameters.x_max - self.parameters_x_min
        y_direction = self.parameters.y_may - self.parameters_y_min
        z_direction = self.parameters.z_maz - self.parameters_z_min

        return _rotations_from_directions(x_direction, y_direction, z_direction)

    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        '''
        Construct a pygdml Box from this body definition
        '''
        x_length = self.parameters.x_max - self.parameters.x_min
        y_length = self.parameters.y_max - self.parameters.y_min
        z_length = self.parameters.z_max - self.parameters.z_min

        return pygdml.Box(self.name, x_length, y_length, z_length)


class BOX(BodyBase):

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

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class SPH(BodyBase):

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

    @BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.
        '''
        centre = self._centre(self.parameters.v_x,
                              self.parameters.v_y,
                              self.parameters.v_z)
        return centre

    def get_rotation(self):
        return _rotation(0,0,0)

    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        '''
        Construct a pgydml orb (full, solid sphere) solid.
        '''
        return pygdml.solid.Orb(self.name, self.parameters.radius)


class RCC(BodyBase):
    '''
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

        self.length = _norm(self.parameters.h_x,
                            self.parameters.h_y,
                            self.parameters.h_z)

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

    @BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere in
        MILLIMETRES, as this is used for GDML.
        '''

        centre_x = self.parameters.v_x + self.parameters.h_x * self.length*0.5
        centre_y = self.parameters.v_y + self.parameters.h_y * self.length*0.5
        centre_z = self.parameters.v_z + self.parameters.h_z * self.length*0.5

        return self._centre(centre_x, centre_y, centre_z)

    def get_rotation(self):
        x_direction = self.parameters.h_x
        y_direction = self.parameters.h_y
        z_direction = self.parameters.h_z

        return _rotations_from_directions(x_direction, y_direction, z_direction)

    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        return pygdml.solid.Tubs(self.name, 0.0,
                                 self.parameters.radius,
                                 self.length*0.5,
                                 0.0,
                                 2*_math.pi)


class REC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class TRC(BodyBase):
    '''
    - V_(x,y,z) (centre of the centre of the major face),
    - Hx, Hy, Hz (components of a vector corresponding to the TRC
    height, directed from the major to the minor base), R(1) (radius
    of the major base), R(2) (radius of the minor base)
    '''
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

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_x',
                                                         'v_y',
                                                         'v_z',
                                                         'h_x',
                                                         'h_y',
                                                         'h_z',
                                                         'radius_major',
                                                         'radius_minor'])
        self.parameters = self._ParametersType(*parameters)
        return None

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class ELL(BodyBase):

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

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class WED(BodyBase):

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

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class RAW(BodyBase):

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

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class ARB(BodyBase):

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

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class XYP(BodyBase):
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

    @BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = 0.0
        centre_y = 0.0
        centre_z = self.parameters.v_z + (self.scale * 0.5)

        return self._centre(centre_x, centre_y, centre_z)

    @BodyBase._parameters_in_mm
    def get_rotation(self):
        return self._rotation(0,0,0)

    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        return pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class XZP(BodyBase):
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
        self.scale = 1e9

    def _set_parameters(self, parameters):
        self._ParametersType = namedtuple("Parameters", ['v_y'])
        self.parameters = self._ParametersType(*parameters)

    @BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = 0.0
        centre_y = self.parameters.v_y + (self.scale * 0.5)
        centre_z = 0.0

    @BodyBase._parameters_in_mm
    def get_rotation(self):
        return self._rotation(0,0,0)

    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        return pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class YZP(BodyBase):
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

    @BodyBase._parameters_in_mm
    def get_coordinates_of_centre(self):
        centre_x = self.parameters.v_x + (self.scale * 0.5)
        centre_y = 0.0
        centre_z = 0.0

    @BodyBase._parameters_in_mm
    def get_rotation(self):
        return self._rotation(0,0,0)

    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        return pygdml.solid.Box(self.name,
                                0.5 * self.scale,
                                0.5 * self.scale,
                                0.5 * self.scale)


class PLA(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class XCC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class YCC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class ZCC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class XEC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class YEC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class ZEC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class QUA(BodyBase):

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

    def get_coordinates_of_centre(self):
        pass

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

def _norm(x1, x2, x3):
    return _math.sqrt(x1**2 + x2**2 + x3**2)

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
