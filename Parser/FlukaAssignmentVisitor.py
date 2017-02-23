from antlr4 import * # change this

from FlukaLexer import FlukaLexer
from FlukaParser import FlukaParser
from FlukaParserVisitor import FlukaParserVisitor

from IPython import embed

class FlukaAssignmentVisitor(FlukaParserVisitor):

    def __init(self):
        self.bodies = {}

    def visitBodyDefSpaceDelim(self, ctx):
        # get the body type (3 letter code):
        body_type = ctx.BodyCode().getText()
        body_ID   = ctx.ID().getText()
        # Get the tokens in constituent data tokens for the rule:
        float_strings = map(lambda node: node.getText(), ctx.Float())
        # Convert them to strings:
        floats = map(float, float_strings)

        # Bodies are keyed with their IDs.  Entry is a tuple, first element is
        # the body type.  The rest are the data members in order.
        self.bodies[body_ID] = tuple(floats.insert(0, body_type))
