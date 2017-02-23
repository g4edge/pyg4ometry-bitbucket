from . import Parser

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
        visitor = Parser.FlukaTreeVisitor()
        visitor.visit(tree)


    # def _GetAssignments(tree):

    def PyGDMLSolidFactory(name):
        pass
