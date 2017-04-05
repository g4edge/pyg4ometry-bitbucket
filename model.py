from collections import namedtuple
import antlr4 as _antlr4
import pygdml as _pygdml
from Parser.FlukaParserVisitor import FlukaParserVisitor
from Parser.FlukaParserListener import FlukaParserListener
from Parser.Parse import Parse
import bodies


class Model(object):

    def __init__(self, filename):
        self.bodies = {}
        self.materials = {}
        self.translations = {}
        self.expansions = {}
        self.transformations = {}
        self.regions = {}
        self.filename = filename

        # get the antlr4 tree.
        tree = Parse(filename)

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
                                + bodies.code_meanings[body]).ljust(60,'.')
            print body_description + str(count)

        return None

    def _get_listener_assignments(self, assignment_listener):
        self.bodies = assignment_listener.bodies
        self.materials = assignment_listener.materials
        self.translations = assignment_listener.translations
        self.expansions = assignment_listener.expansions
        self.transformations = assignment_listener.transformations

        return None


class _FlukaAssignmentListener(FlukaParserListener):

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
        body_parameters = self._get_floats(ctx)
        # embed()
        body_constructor = getattr(bodies, body_type)

        body = body_constructor(body_name,
                                body_parameters,
                                self._transform_stack,
                                self._translat_stack,
                                self._expansion_stack)

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


class _FlukaRegionVisitor(FlukaParserVisitor):

    def __init__(self, bodies, materials):
        self.bodies = bodies
        self.materials = materials
        w = _pygdml.solid.Box("world", 10000, 10000, 10000)
        self.world_volume = _pygdml.Volume(
            [0,0,0], [0,0,0], w, "world-volume",
            None, 1, False, "G4_Galactic")

        self.regions = {}

    def visitRegion(self, ctx):
        # region_solid = self.visit(self.expr())
        region_solid = self.visitChildren(ctx)

        region_centre_x = region_solid.centre.x
        region_centre_y = region_solid.centre.y
        region_centre_z = region_solid.centre.z
        region_centre = [region_centre_x,
                         region_centre_y,
                         region_centre_z]

        region_rotation_x = region_solid.rotation.x
        region_rotation_y = region_solid.rotation.y
        region_rotation_z = region_solid.rotation.z
        region_rotation = [region_rotation_x,
                           region_rotation_y,
                           region_rotation_z]

        region_gdml = region_solid.solid
        region_name = ctx.RegionName().getText()

        if region_solid.operator == '+':
            placement = _pygdml.volume.Volume(region_rotation,
                                              region_centre,
                                              region_gdml,
                                              region_name,
                                              self.world_volume,
                                              1,
                                              False,
                                              "copper")

    def visitUnaryAndBoolean(self, ctx):
        left_solid = self.visit(ctx.unaryExpression())
        right_solid = self.visit(ctx.expr())
        return left_solid.combine(right_solid)

    def visitUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()
        body = self.bodies[body_name]
        gdml_solid = body.get_as_gdml_solid()
        body_centre = body.get_coordinates_of_centre()
        body_rotation  = body.get_rotation()

        if ctx.Plus():
            return _UnaryGDMLSolid(gdml_solid, '+', body_centre, body_rotation)
        else:
            return _UnaryGDMLSolid(gdml_solid, '-', body_centre, body_rotation)

    def visitZoneUnion(self, ctx):
        # Get the zones:
        zones = [self.visit(zone) for zone in ctx.zone()]
        union_of_zones = reduce(lambda first, second:
                                first.union(second), zones)
        return union_of_zones


class _UnaryGDMLSolid(object):
    '''
    A gdml solid with a unary operator from Fluka and a position.
    '''

    def __init__(self, pygdml_solid, operator, centre, rotation):
        self.solid = pygdml_solid
        self.operator = operator
        self.centre = centre
        self.rotation = rotation

    def combine(self, other):
        '''
        Combine two _UnaryGDMLSolids, returning the third resultant.
        Doesn't handle simple union solids, as these are not
        "combinations" between two Fluka unary operations, but instead
        have their own syntax.  This is handled by the "union" method
        '''

        if self.operator == '+' and other.operator == '+':
            return self._combine_plus_plus(other)
        elif self.operator == '-' and other.operator == '-':
            return self._combine_minus_minus(other)
        elif self.operator == '-' and other.operator == '+':
            return self._combine_minus_plus(other)
        elif self.operator == '+' and other.operator == '-':
            return self._combine_plus_minus(other)
        else:
            raise Exception("One or more unknown operator types:",
                            self.operator, other.operator)

    def _combine_minus_plus(self, other):
        return other._combine_plus_minus(self)

    def _combine_plus_minus(self, other):
        output_name = "(%s_\_%s)" % (self.solid.name, other.solid.name)

        other_transformation = self._get_transformation(other)

        output_solid = _pygdml.solid.Subtraction(output_name,
                                                 self.solid,
                                                 other.solid,
                                                 other_transformation)
        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation

        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)

    def _combine_plus_plus(self, other):

        output_name = "(%s_+_%s)" % (self.solid.name,
                                                other.solid.name)
        other_transformation = self._get_transformation(other)
        output_solid = _pygdml.solid.Intersection(output_name,
                                                  self.solid,
                                                  other.solid,
                                                  other_transformation)
        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation

        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)

    def _combine_minus_minus(self, other):
        output_name = "(%s_|_%s)" % (self.solid.name,
                                         other.solid.name)
        other_transformation = self._get_transformation(other)

        output_operator = '-'
        output_centre = self.centre
        output_rotation = self.rotation

        output_solid =  _pygdml.Union(output_name,
                                       self.solid,
                                       other.solid,
                                       other_transformation)
        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)

    def _get_transformation(self, other):
        # other_transformation is the transformation applied to the
        # second volume w.r.t the first, which is situated at (0,0,0)
        # without rotation when peforming the boolean operation.
        offset_x = other.centre.x - self.centre.x
        offset_y = other.centre.y - self.centre.y
        offset_z = other.centre.z - self.centre.z

        offset_x_rotation = other.rotation.x - self.rotation.x
        offset_y_rotation = other.rotation.y - self.rotation.y
        offset_z_rotation = other.rotation.z - self.rotation.z

        other_translation = [offset_x, offset_y, offset_z]
        other_rotation = [offset_x_rotation,
                          offset_y_rotation,
                          offset_z_rotation]

        other_transformation = [other_rotation, other_translation]

        return other_transformation

    def union(self, other):
        output_name = "(%s_union_%s)" % (self.solid.name, other.solid.name)
        other_transformation = self._get_transformation(other)

        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation

        output_solid =  _pygdml.Union(output_name,
                                      self.solid,
                                      other.solid,
                                      other_transformation)

        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)
