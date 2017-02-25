from . import Parser
import antlr4 as _antlr4
import pygdml as pygdml

class Model(object):
    def __init__(self, input):
        self.bodies = {}
        self.materials = {}
        self.translations = {}



        # get the antlr4 tree.
        tree = Parser.Parse(input)
        print "visiting"
        self._VisitTree(tree)

    def _VisitTree(self, tree):
        visitor = Parser.FlukaAssignmentVisitor()
        visitor.visit(tree)


    # def _GetAssignments(tree):

    def PyGDMLSolidFactory(name):
class Body(object):
    '''
    A class representing a body as defined in Fluka.
    get_body_as_gdml_solid() returns the body as a pygdml.solid
    '''

    def __init__(self,
                 name,
                 body_type,
                 data,
                 expansion_stack,
                 translation_stack,
                 transformation_stack):

        self.name = name
        self.body_type = body_type
        self.data = data
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

    def get_body_as_gdml_solid(self):
        '''
        Get this Fluka body as a pygdml instance.
        '''
        return getattr(self, "_get_" + self.body_type + "_as_gdml_solid")

    def _get_RPP_as_gdml_solid(self):
        pass

    def _get_BOX_as_gdml_solid(self):
        pass

    def _get_SPH_as_gdml_solid(self):
        '''
        Construct a sphere solid.
        '''
        data = self._get_data_in_mm()
        centre_x = data[0]
        centre_z = data[1]
        centre_z = data[2]
        radius   = data[3]

        return pygdml.solid.Sphere(self.name,
                                   0.0,
                                   centre_x
                                   centre_y
                                   centre_z
                                   radius)

    def _get_RCC_as_gdml_solid(self):
        pass

    def _get_REC_as_gdml_solid(self):
        pass

    def _get_TRC_as_gdml_solid(self):
        pass

    def _get_ELL_as_gdml_solid(self):
        pass

    def _get_WED_as_gdml_solid(self):
        pass

    def _get_RAW_as_gdml_solid(self):
        pass

    def _get_ARB_as_gdml_solid(self):
        pass

    def _get_XYP_as_gdml_solid(self):
        pass

    def _get_XZP_as_gdml_solid(self):
        pass

    def _get_YZP_as_gdml_solid(self):
        pass

    def _get_PLA_as_gdml_solid(self):
        pass

    def _get_XCC_as_gdml_solid(self):
        pass

    def _get_YCC_as_gdml_solid(self):
        pass

    def _get_ZCC_as_gdml_solid(self):
        pass

    def _get_XEC_as_gdml_solid(self):
        pass

    def _get_YEC_as_gdml_solid(self):
        pass

    def _get_ZEC_as_gdml_solid(self):
        pass

    def _get_QUA_as_gdml_solid(self):
        pass


