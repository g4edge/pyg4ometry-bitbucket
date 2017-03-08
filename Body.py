import pygdml as pygdml
from collections import namedtuple
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

    def _get_parameters_in_mm(self):
        '''
        pygdml is in units of millimetres.  Fluka is in units of
        centimetres.  Helper function for this purpose.
        '''
        cm = 10.0
        return [i * cm for i in self.parameters]

    # def get_body_as_gdml_solid(self):
    #     '''
    #     Get this Fluka body as a pygdml instance.
    #     '''
    #     return getattr(self, "_get_"
    #                    + self.body_type
    #                    + "_as_gdml_solid")()


    def get_coordinates_of_centre(self):
        '''This is a method which gets the coordinates of the centre of the
        body as defined in GDML.  This is necessary as a bookkeeping
        measure as gdml solids have no sense of their position.
        Indices = xyz of parameters.
        '''

        centre_x = (self.parameters.x_max + self.parameters.x_min)*0.5
        centre_y = (self.parameters.y_max + self.parameters.y_min)*0.5
        centre_z = (self.parameters.z_max + self.parameters.z_min)*0.5

        centre = self._centre(centre_x, centre_y, centre_z)

        return centre

class RPP(BodyBase):

    def __init__(self, name, parameters, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass


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

    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere.
        '''
        centre = namedtuple("centre", ['x','y','z'])
        centre = self._centre(self.parameters.v_x,
                              self.parameters.v_y,
                              self.parameters.v_z)
        return centre

    def get_as_gdml_solid(self):
        '''
        Construct a pgydml orb (full, solid sphere) solid.
        '''
        # A function-local parameters for use with mm (rather than fluka cm)
        parameters_in_mm = self._ParametersType(*self._get_parameters_in_mm())

        return pygdml.solid.Orb(self.name, parameters_in_mm.radius)


class RCC(BodyBase):

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
        self._ParametersType = namedtuple("Parameters", [])
        self.parameters = self._ParametersType(*parameters)

    def get_coordinates_of_centre(self):
        pass

    def get_as_gdml_solid(self):
        pass


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
