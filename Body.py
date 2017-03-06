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
        self.expansion_stack = expansion_stack
        self.translation_stack = translation_stack
        self.transformation_stack = transformation_stack

    def set_transformation_definitions(self, something):
        pass

    def _get_data_in_mm(self):
        '''
        pygdml is in units of millimetres.  Fluka is in units of
        centimetres.  Helper function for this purpose.
        '''
        cm = 10.0
        return [i * cm for i in self.data]

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
        Indices = xyz of data.
        '''

        Fluka_body_xyz_indices = {
            "RPP": None,
            "BOX": None,
            "SPH": [0,1,2],
            "RCC": None,
            "REC": None,
            "TRC": None,
            "ELL": None,
            "WED": None,
            "RAW": None,
            "ARB": None,
            "XYP": None,
            "XZP": None,
            "YZP": None,
            "PLA": None,
            "XCC": None,
            "YCC": None,
            "ZCC": None,
            "XEC": None,
            "YEC": None,
            "ZEC": None,
            "QUA": None
        }

        x_index = Fluka_body_xyz_indices[self.name][0]
        y_index = Fluka_body_xyz_indices[self.name][1]
        z_index = Fluka_body_xyz_indices[self.name][2]

        centre = namedtuple("centre", ['x','y','z'])
        centre = centre(self.data[x_index],
                        self.data[y_index],
                        self.data[z_index])

        return centre

class RPP(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass


class BOX(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class SPH(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):

        super(SPH, self).__init__(name,
                                  expansion_stack,
                                  translation_stack,
                                  transformation_stack)

        self._set_body_specific_parameters(data)

    def _set_body_specific_parameters(self, data):
        # A named tuple for representing the geometry data associated with
        # the object.
        self._DataType = namedtuple("Data", ['v_x',
                                             'v_y',
                                             'v_z',
                                             'radius'])
        self.data = self._DataType(*data)
        return None

    def get_coordinates_of_centre(self):
        '''
        Returns the coordinates of the centre of the sphere.
        '''
        centre = namedtuple("centre", ['x','y','z'])
        centre = centre(self.data.v_x,
                        self.data.v_y,
                        self.data.v_z)
        return centre

    def get_as_gdml_solid(self):
        '''
        Construct a pgydml orb (full, solid sphere) solid.
        '''
        # A function-local data for use with mm (rather than fluka cm)
        data_in_mm = self._DataType(*self._get_data_in_mm())

        return pygdml.solid.Orb(self.name, data_in_mm.radius)


class RCC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class REC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class TRC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class ELL(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class WED(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class RAW(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class ARB(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class XYP(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class XZP(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class YZP(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class PLA(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class XCC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class YCC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class ZCC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class XEC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class YEC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class ZEC(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
        pass

class QUA(BodyBase):

    def __init__(self, name, data, expansion_stack,
                 translation_stack,
                 transformation_stack):
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
