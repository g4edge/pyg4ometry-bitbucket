from . import Parser
import antlr4 as _antlr4
import pygdml as _pygdml
import Body
from math import pi
from collections import namedtuple

class Model(object):

    def __init__(self, input):
        self.bodies = {}
        self.materials = {}
        self.translations = {}
        self.expansions = {}
        self.transformations = {}
        self.regions = {}
        self.filename = input

        # get the antlr4 tree.
        tree = Parser.Parse(input)

        assignment_listener = _FlukaAssignmentListener()
        walker = _antlr4.ParseTreeWalker()
        walker.walk(assignment_listener, tree)


        self._get_listener_assignments(assignment_listener)
        self.report_body_count()
        self._convert_bodies_to_gdml_solids()

        visitor = _FlukaRegionVisitor(self.bodies, self.materials)
        visitor.visit(tree)
    def convert_model_to_gdml(self):
        pass

    def _convert_bodies_to_gdml_solids(self):
        gdml_solids= dict([(body.name, body.get_as_gdml_solid())
                           for body in self.bodies.itervalues()])
        return None

    def report_body_count(self):
        '''
        Prints the different types of bodies that appear in the model
        and their frequencies, in order.
        '''

        # Get unique body types as list of strings from all the body defs
        body_types = [type(body).__name__ for body in
                      self.bodies.itervalues()]
        unique_body_types = set(body_types)

        # Count how many times each body definition appears and sort.
        body_count = [body_types.count(body_type)
                      for body_type in unique_body_types]
        body_and_count = zip(unique_body_types, body_count)
        body_and_count.sort(key = lambda i: i[1], reverse=True)

        # Print result, with alignment.
        for body, count in body_and_count:
            body_description = (body
                                + " - "
                                + Body.code_meanings[body]).ljust(60,'.')
            print body_description + str(count)

        return None

    def _get_listener_assignments(self, assignment_listener):
        self.bodies = assignment_listener.bodies
        self.materials = assignment_listener.materials
        self.translations = assignment_listener.translations
        self.expansions = assignment_listener.expansions
        self.transformations = assignment_listener.transformations

        return None


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

        body_constructor = getattr(Body, body_type)

        body = body_constructor(body_name,
                                body_data,
                                self._transform_stack,
                                self._translat_stack,
                                self._expansion_stack)

        # body = Body(body_name, body_type, body_data,
        #             self._transform_stack,
        #             self._translat_stack,
        #             self._expansion_stack)

        self.bodies[body_name] = body

    def enterTranslat(self, ctx):
        # ctx.Float() returns an array of 3 terminal nodes.
        # These correspond to the 3-vector that forms the translation.
        translation = self._get_floats(ctx)
        self._translat_stack.append(translation)
        return None

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


class _FlukaRegionVisitor(Parser.FlukaParserVisitor.FlukaParserVisitor):

    def __init__(self, bodies, materials):
        self.bodies = bodies
        self.materials = materials
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        self.world_volume = _pygdml.Volume(
            [0,0,0], [0,0,0], w, "world-volume",
            None, 1, False, "G4_Galatic")

        self.regions = {}

    def visitRegion(self, ctx):

        # region_solid = self.visit(self.booleanexpression())
        region_solid = self.visitChildren(ctx)
        region_centre_x = region_solid.centre.x
        region_centre_y = region_solid.centre.y
        region_centre_z = region_solid.centre.z
        region_centre = [region_centre_x,
                         region_centre_y,
                         region_centre_z]
        region_gdml = region_solid.solid
        region_name = ctx.RegionName().getText()

        if region_solid.operator == '+':
            placement = _pygdml.volume.Volume(
                [0,0,0], region_centre, region_gdml, region_name,
                self.world_volume, 1, False, "copper")

    def visitUnaryAndBoolean(self, ctx):
        left_solid = self.visit(ctx.unaryExpression())
        right_solid = self.visit(ctx.booleanExpression())
        return left_solid.combine(right_solid)

    def visitUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()
        body = self.bodies[body_name]
        gdml_solid = body.get_as_gdml_solid()
        body_centre = body.get_coordinates_of_centre()

        if ctx.Plus():
            return _UnaryGDMLSolid(gdml_solid, '+', body_centre)
        else:
            return _UnaryGDMLSolid(gdml_solid, '-', body_centre)


class _UnaryGDMLSolid(object):
    '''
    A gdml solid with a unary operator from Fluka and a position.
    '''

    def __init__(self, pygdml_solid, operator, centre):
        self.solid = pygdml_solid
        self.operator = operator
        self.centre = centre

    def combine(self, other):
        '''
        Combine two _UnaryGDMLSolids, returning the third resultant.
        '''

        if self.operator == '+' and other.operator == '+':
            return self._combine_plus_plus(other)


    def _combine_plus_minus(self, pygdml_solid):
        name = self.solid.name
        other_name = other.solid.name
        output_name = "(" + name + "_intersection_" + other_name + ")"

        other_transformation = self._get_transformation(other)

        output_solid = _pygdml.solid.Subtraction(output_name,
                                                 self.solid,
                                                 other.solid,
                                                 other_transformation)
        output_operator = '+'
        output_centre = self.centre

        return _UnaryGDMLSolid(resultant_solid,
                               resultant_operator,
                               resultant_centre)


    def _combine_plus_plus(self, pygdml_solid):

        name = self.solid.name
        other_name = other.solid.name
        output_name = "(" + name + "_intersection_" + other_name + ")"

        other_transformation = self._get_transformation(other)

        output_solid = _pygdml.solid.Intersection(output_name,
                                                  self.solid,
                                                  other.solid,
                                                  other_transformation)
        output_operator = '+'
        output_centre = self.centre

        return _UnaryGDMLSolid(resultant_solid,
                               resultant_operator,
                               resultant_centre)

    def _combine_minus_minus(self, other):
        name = self.solid.name
        other_name = other.solid.name
        output_name = "(" + name + "_union_" + other_name + ")"

        other_transformation = self._get_transformation(other)

        output_operator = '-'
        output_centre = self.centre

        output_solid = _pygdml.Union(output_name,
                                     self.solid,
                                     other.solid,
                                     other_transformation)

    def _get_transformation(self, other):
        # other_transformation is the transformation applied to the
        # second volume w.r.t the first, which is situated at (0,0,0),
        # when peforming the boolean operation
        centre =  _get_tuple_in_mm(self.centre)
        other_centre =  _get_tuple_in_mm(other.centre)

        offset_x = other_centre.x - centre.x
        offset_y = other_centre.y - centre.y
        offset_z = other_centre.z - centre.z

        other_translation = [offset_x, offset_y, offset_z]
        other_rotation = [0,0,0]
        other_transformation = [other_rotation, other_translation]

        return other_transformation


def _get_tuple_in_mm(input_tuple):
    '''
    input_tuple:  a namedtuple.
    returns namedtuple of identical shape but with mm instead
    '''
    mm = 10.0
    data = [i * mm for i in input_tuple]
    _DataType = namedtuple("Data", input_tuple._fields)

    return _DataType(*data)
