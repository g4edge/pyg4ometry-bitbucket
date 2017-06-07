# Generated from FlukaParser.g4 by ANTLR 4.6
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by FlukaParser.

class FlukaParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FlukaParser#model.
    def visitModel(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#command.
    def visitCommand(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#SimpleMaterial.
    def visitSimpleMaterial(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#CompoundMaterial.
    def visitCompoundMaterial(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#material.
    def visitMaterial(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#compound.
    def visitCompound(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#geoBegin.
    def visitGeoBegin(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#otherKeywords.
    def visitOtherKeywords(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#geocards.
    def visitGeocards(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#GeometryDirective.
    def visitGeometryDirective(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#BodyDefSpaceDelim.
    def visitBodyDefSpaceDelim(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#BodyDefPunctDelim.
    def visitBodyDefPunctDelim(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#simpleRegion.
    def visitSimpleRegion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#complexRegion.
    def visitComplexRegion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#multipleUnion.
    def visitMultipleUnion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#singleUnion.
    def visitSingleUnion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#zone.
    def visitZone(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#singleUnary.
    def visitSingleUnary(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#unaryAndBoolean.
    def visitUnaryAndBoolean(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#unaryAndSubZone.
    def visitUnaryAndSubZone(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#oneSubZone.
    def visitOneSubZone(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#subZone.
    def visitSubZone(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#unaryExpression.
    def visitUnaryExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#geoDirective.
    def visitGeoDirective(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#expansion.
    def visitExpansion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#translat.
    def visitTranslat(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#transform.
    def visitTransform(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FlukaParser#lattice.
    def visitLattice(self, ctx):
        return self.visitChildren(ctx)


