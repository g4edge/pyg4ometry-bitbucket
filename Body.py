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
                          "its maxes\n. It is ignored in Fluka but "
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

        self.length = _math.sqrt(self.parameters.h_x**2
                                 + self.parameters.h_y**2
                                 + self.parameters.h_z**2)

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


    @BodyBase._parameters_in_mm
    def get_as_gdml_solid(self):
        return pygdml.solid.Tubs(self.name, 0.0,
                                 self.parameters.radius,
                                 self.length,
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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class XZP(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


class YZP(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


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
    pass


class Transformation(object):
    pass


class Expansion(object):
    pass


code_meanings = {
    "RPP": "Rectangular Parallelepiped",
    "BOX": "General Rectangular Parallelepiped",
    "SPH": "Sphere",
    "RCC": "Right Circular Cylinder",
    "REC": "Right Ellitpical Cylinder",
    "TRC": "Truncated Right Angle Cone",
    "ELL": "Elippsoid of Revolution",
    "WED": "Right Angle Wedge",
    "RAW": "Right Angle Wedge",
    "ARB": "Abitrary Convex Polyhedron",
    "XYP": "Infinite Half-space",
    "XZP": "Infinite Half-space",
    "YZP": "Infinite Half-space",
    "PLA": "Generic Infinite Half-space",
    "XCC": "Infinite Circular Cylinder parallel to the x-axis",
    "YCC": "Infinite Circular Cylinder parallel to the y-axis",
    "ZCC": "Infinite Circular Cylinder parallel to the z-axis",
    "XEC": "Infinite Elliptical Cylinder parallel to the x-axis",
    "YEC": "Infinite Elliptical Cylinder parallel to the y-axis",
    "ZEC": "Infinite Elliptical Cylinder parallel to the z-axis",
    "QUA": "Generic Quadric"
}
