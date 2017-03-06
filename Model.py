from . import Parser
import antlr4 as _antlr4
import pygdml as pygdml
from math import pi

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

        visitor = _FlukaRegionVisitor()
        visitor.visit(tree)

        self._get_listener_assignments(assignment_listener)
        self.report_body_count()
        self._convert_bodies_to_gdml_solids()

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

    def __init__(self):
        pass

    def visitBooleanExpression(self, ctx):
        pass


    '''
    '''


        '''
        '''























