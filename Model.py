from . import Parser
import antlr4 as _antlr4
import pygdml as pygdml

class Model(object):

    def __init__(self, input):
        self.bodies = {}
        self.materials = {}
        self.translations = {}
        self.expansions = {}
        self.transformations = {}
        self.filename = input

        # get the antlr4 tree.
        tree = Parser.Parse(input)
        assignment_listener = _FlukaAssignmentListener()
        walker = _antlr4.ParseTreeWalker()
        walker.walk(assignment_listener, tree)

        self._get_listener_assignments(assignment_listener)
        self.report_body_count()

    def report_body_count(self):
        '''
        Prints the different types of bodies that appear in the model
        and their frequencies, in order.
        '''
        body_types = [body.body_type for body in
                      self.bodies.itervalues()]
        unique_body_types = set(body_types)

        body_count = [body_types.count(body_type)
                      for body_type in unique_body_types]
        body_and_count = zip(unique_body_types, body_count)
        body_and_count.sort(key = lambda i: i[1], reverse=True)

        for body, count in body_and_count:
            body_description = (body
                                + " - "
                                + _Fluka_body_code_meanings[body]).ljust(60,'.')
            print body_description + str(count)

        return None

    def _get_listener_assignments(self, assignment_listener):
        self.bodies = assignment_listener.bodies
        self.materials = assignment_listener.materials
        self.translations = assignment_listener.translations
        self.expansions = assignment_listener.expansions
        self.transformations = assignment_listener.transformations

        return None

    def _VisitTree(self, tree):
        visitor = Parser.FlukaAssignmentVisitor()
        visitor.visit(tree)

class _FlukaAssignmentListener(Parser.FlukaParserListener):

    def __init__(self):

        self.bodies = {}
        self.materials = {}

        self.translations = {}
        self.expansions = {}
        self.transformations = {}

        self._transform_stack = []
        self._translat_stack = []
        self._expansion_stack = []

    def enterBodyDefSpaceDelim(self, ctx):
        if ctx.ID():
            body_name = ctx.ID().getText()
        else:
            body_name = int(ctx.Integer().getText())

        body_type = ctx.BodyCode().getText()
        # ctx.Float() returns a list of Float contexts associated with this body
        # Get their text, and convert it to floats.
        body_data = self._get_floats(ctx)

        body = Body(body_name, body_type, body_data,
                    self._transform_stack,
                    self._translat_stack,
                    self._expansion_stack)

        self.bodies[body_name] = body

    def enterTranslat(self, ctx):
        # embed()
        # ctx.Float() returns an array of 3 terminal nodes.
        # These correspond to the 3-vector that forms the translation.
        translation = self._get_floats(ctx)
        self._translat_stack.append(translation)

    def exitTranslat(self, ctx):
        self._translat_stack.pop()
        return None

    def enterExpansion(self, ctx):
        self._expansion_stack.append(ctx.Float().getText())

    def exitExpansion(self, ctx):
        self._expansion_stack.pop()
        return None

    @staticmethod
    def _get_floats(ctx):
        '''
        Gets the Float tokens associated with the rule and returns
        them as an array of python floats.
        '''
        float_strings = [i.getText() for i in ctx.Float()]
        floats = map(float, float_strings)
        return floats

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


_Fluka_body_code_meanings = {
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
