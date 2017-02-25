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
        pass
