from collections import namedtuple as _namedtuple
from collections import Counter as _Counter
import logging as _logging
import os.path as _path
import warnings as _warnings

import antlr4 as _antlr4
import pygdml as _pygdml

import bodies
import materials
from materials import fluka_g4_material_map as default_material_map
from Parser.FlukaParserVisitor import FlukaParserVisitor
from Parser.FlukaParserListener import FlukaParserListener
from Parser.Parse import Parse

_logger = _logging.getLogger(__name__)

class Model(object):
    def __init__(self, filename,
                 material_map=None,
                 **kwargs):

        self._filename = filename
        self.material_map = material_map
        _logging.basicConfig(level=_logging.DEBUG,
                     format='%(name)-20s %(levelname)-8s %(message)s',
                     datefmt='%m-%d %H:%M',
                     filename=_path.basename(
                         _path.splitext(self._filename)[0]) + ".log",
                     filemode='w')
        _logger.info("creating pyfluka model from file %s", filename)

        self.debug = kwargs.get("debug")
        if not material_map:
            material_map = default_material_map

        # get the syntax tree.
        self.tree = Parse(filename)

        self._materials_from_model()
        self._bodies_from_model()
        self.report_body_count()

    def _gdml_world_volume(self):
        # Populate, get, and clip the world volume.
        visitor = _FlukaRegionVisitor(self.bodies,
                                      self._region_material_map,
                                      self._region_max_scale_map,
                                      debug=self.debug)
        visitor.visit(self.tree)
        self._world_volume = visitor.world_volume
        self._world_volume.setClip()

    def write_to_gdml(self, out_path=None, make_gmad=False):
        """
        Convert the region to GDML.  Default output file name is
        "./" + basename + ".gdml".

        """
        if not hasattr(self, "_world_volume"):
            self._gdml_world_volume()
        if out_path == None:
            out_path = ("./"
                        + _path.basename(
                            _path.splitext(self._filename)[0])
                        + ".gdml")
        out = _pygdml.Gdml()
        out.add(self._world_volume)
        out.write(out_path)

        if make_gmad == True:
            self._write_test_gmad(out_path)

    def view_mesh(self):
        if not hasattr(self, "_world_volume"):
            self._gdml_world_volume()
        world_mesh = self._world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(world_mesh)
        viewer.view()

    def report_body_count(self):
        """
        Prints the frequency of bodies in order and by type that are used
        in region definitions.  Bodies which are defined but not used
        are not included in this count.
        """

        body_and_count = self._body_freq_map.items()
        body_and_count.sort(key = lambda i: i[1], reverse=True)
        # Print result, with alignment.
        print "Bodies used in region definitions:"
        for body, count in body_and_count:
            body_description = (body
                                + " - "
                                + bodies.code_meanings[body]).ljust(60,'.')
            print body_description + str(count)

    def _materials_from_model(self):
        # This gets the materials and maps them to their region (volumes)
        material_listener = _FlukaMaterialGetter(self.material_map)
        walker = _antlr4.ParseTreeWalker()
        walker.walk(material_listener, self.tree)
        self._region_material_map = material_listener._region_material_map

    def _bodies_from_model(self):
        body_listener = _FlukaBodyListener()
        walker = _antlr4.ParseTreeWalker()
        walker.walk(body_listener, self.tree)
        self.bodies = body_listener.bodies
        used_bodies_by_type = body_listener.used_bodies_by_type
        self._body_freq_map = _Counter(used_bodies_by_type)
        self._region_max_scale_map = body_listener.region_max_scale_map

    def _write_test_gmad(self, gdml_path):
        gmad_path = _path.splitext(gdml_path)[0] + ".gmad"
        with open(gmad_path, 'w') as gmad:
            gmad.write("test_component: element, l=10.*m, geometry=\"gdml:%s\","
                       " outerDiameter=2.1*m;\n" % gdml_path)
            gmad.write('\n')
            gmad.write("component : line = (test_component);\n")
            gmad.write('\n')
            gmad.write("beam,  particle=\"e-\",\n"
                       "energy=1.5 * GeV,\n"
                       "X0=0.1*um;\n")
            gmad.write('\n')
            gmad.write("use, period=component;\n")



class _FlukaMaterialGetter(FlukaParserListener):
    # This class gets the materials as pygdml.materials instances.
    # Or perhaps as pyfluka.materials Material instances (???)

    def __init__(self, fluka_g4_material_map):
        self.materials = fluka_g4_material_map
        self._region_material_map = dict()

        self._Card = _namedtuple("Card", ["keyword", "one",
                                          "two", "three",
                                          "four", "five",
                                          "six", "sdum"])

    def enterSimpleMaterial(self, ctx):
        material_card = self._cards_from_rule(ctx)

    def enterCompoundMaterial(self, ctx):
        cards = self._cards_from_rule(ctx)

    def _cards_from_rule(self, ctx):
        # Get the tokens in a fixed format.
        # Loop over all the tokens in the context:
        tokens = []
        # tokens = [ctx.getChild(i) for i in range(ctx.getChildCount)]
        def get_tokens_iter(ctx):
            if (type(ctx) is _antlr4.tree.Tree.TerminalNodeImpl):
                    # and type(ctx.getPayload()) is _antlr4.Token):
                    tokens.append(ctx.getPayload())
            else:
                for child in ctx.getChildren():
                    get_tokens_iter(child)
        get_tokens_iter(ctx)
        return self._card_factory(tokens)

    def _card_factory(self, tokens):
        # tokens should be a list of tokens
        # Sort in order:
        tokens.sort(key=lambda token: token.start)
        # Get unique line numbers
        lines = set([token.line for token in tokens])

        # Separate the tokens by their lines, starting from first line.
        tokens_by_line = []
        for line_number in lines:
            # Nest list of tokens by line.
            tokens_in_line = [token for token in tokens
                              if token.line == line_number]
            tokens_by_line.append(tokens_in_line)

        cards = []
        self.is_fixed = True
        if self.is_fixed:
            for line in tokens_by_line:
                # Set variables to None before defining a new card instance.
                (keyword, one, two, three, four, five, six, sdum) = 8 * [None]
                for token in line:
                    if token.column < 10:
                        keyword = token.text
                    elif token.column < 20:
                        one = token.text
                    elif token.column < 30:
                        two = token.text
                    elif token.column < 40:
                        three = token.text
                    elif token.column < 50:
                        four = token.text
                    elif token.column < 60:
                        five = token.text
                    elif token.column < 70:
                        six = token.text
                    elif token.column < 80:
                        sdum = token.text

                cards.append(self._Card(keyword, one,
                                        two, three,
                                        four, five,
                                        six, sdum))



class _FlukaBodyListener(FlukaParserListener):
    def __init__(self):
        self.bodies = dict()

        self.omitted_bodies = list()
        self.region_max_scale_map = dict()
        self.unique_body_names = set()
        self.used_bodies_by_type = list()

        self._transform_stack = []
        self._translat_stack = []
        self._expansion_stack = []

    def enterRegion(self, ctx):
        self.region_name = ctx.RegionName().getText()
        self.max_scale = 0.0

    def exitRegion(self, ctx):
        region_name = ctx.RegionName().getText()
        self.region_max_scale_map[region_name] = self.max_scale

    def enterBodyDefSpaceDelim(self, ctx):
        if ctx.ID():
            body_name = ctx.ID().getText()
        else:
            body_name = int(ctx.Integer().getText())

        body_type = ctx.BodyCode().getText()
        body_parameters = self._get_floats(ctx)
        body_constructor = getattr(bodies, body_type)
        try:
            body = body_constructor(body_name,
                                    body_parameters,
                                    self._transform_stack,
                                    self._translat_stack,
                                    self._expansion_stack)
            self.bodies[body_name] = body
        except bodies.BodyNotImplementedError:
            _warnings.simplefilter('once', UserWarning)
            _warnings.warn(("\nBody type %s not supported.  All bodies"
                            " of this type will be omitted.  If bodies"
                            " of this type are used in regions, the"
                            " conversion will fail.") % body_type,
                           UserWarning)
            self.omitted_bodies.append((body_name, body_type))

    def enterUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()
        try:
            self.max_scale = max(self.max_scale,
                                 abs(self.bodies[body_name].extent()))
        except KeyError:
            raise KeyError(("Undefined body \"{}\""
                            " in region: \"{}\"!".format(body_name,
                                                         self.region_name)))

        # For logging purpose
        if body_name in self.unique_body_names:
            return None
        else:
            self.unique_body_names.add(body_name)
            body_type = type(self.bodies[body_name]).__name__
            self.used_bodies_by_type.append(body_type)

    def enterTranslat(self, ctx):
        # ctx.Float() returns an array of 3 terminal nodes.
        # These correspond to the 3-vector that forms the translation.
        translation = self._get_floats(ctx)
        self._translat_stack.append(translation)

    def exitTranslat(self, ctx):
        self._translat_stack.pop()

    def enterExpansion(self, ctx):
        self._expansion_stack.append(ctx.Float().getText())

    def exitExpansion(self, ctx):
        self._expansion_stack.pop()

    def _get_floats(self, ctx):
        '''
        Gets the Float tokens associated with the rule and returns
        them as an array of python floats.
        '''
        float_strings = [i.getText() for i in ctx.Float()]
        floats = map(float, float_strings)
        return floats



class _FlukaRegionVisitor(FlukaParserVisitor):
    def __init__(self, bodies, materials, region_scale_map, debug=False):
        self.bodies = bodies
        self.materials = materials
        self.region_scale_map = region_scale_map
        self.debug = debug

        self.regions = {}

        world_size = max(self.region_scale_map.values()) * 5.0
        _logger.debug("worldvolume: name=world; dimensions=%s", world_size)
        w = _pygdml.solid.Box("world", world_size, world_size, world_size)
        self.world_volume = _pygdml.Volume(
            [0,0,0], [0,0,0], w, "world-volume",
            None, 1, False, "G4_Galactic")

    def visitRegion(self, ctx):
        self.region_name = ctx.RegionName().getText()
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

        # This allows us to plot subtractions without something to
        # subtract from.  Useful for looking at all the solids.
        if region_solid.operator == '+' or region_solid.operator == '-':
            _logger.debug("volume: name=%s; position=%s; rotation=%s; solid=%s",
                              region_name, region_centre,
                              region_rotation, region_gdml.name)
            placement = _pygdml.volume.Volume(region_rotation,
                                              region_centre,
                                              region_gdml,
                                              region_name,
                                              self.world_volume,
                                              1,
                                              False,
                                              "G4_Galactic")



    def visitUnaryAndBoolean(self, ctx):
        left_solid = self.visit(ctx.unaryExpression())
        right_solid = self.visit(ctx.expr())
        return left_solid.combine(right_solid)

    def visitUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()

        body = self.bodies[body_name]
        body_type = type(body).__name__

        # If an infinite body:
        if isinstance(body, bodies._InfiniteSolid):
            scale = self.region_scale_map[self.region_name] * 10.
            # Infinite bodies are factories for themselves, allowing
            # for dynamic infinite scale for a common underlying body.
            body = body(scale)
            _logger.debug("infinite solid:  type=%s; scale=%s",
                          body_type, scale)

        gdml_solid = body.get_as_gdml_solid()
        body_centre = body.get_coordinates_of_centre()
        body_rotation  = body.get_rotation()

        if ctx.Plus():
            return _UnaryGDMLSolid(gdml_solid, '+', body_centre, body_rotation)
        else:
            return _UnaryGDMLSolid(gdml_solid, '-', body_centre, body_rotation)

    def visitUnaryAndSubZone(self, ctx):
        first= self.visit(ctx.subZone())
        second = self.visit(ctx.expr())
        return first.combine(second)

    def visitMultipleUnion(self, ctx):
        # Get the zones:
        zones = [self.visit(zone) for zone in ctx.zone()]
        union_of_zones = reduce(lambda first, second:
                                first.union(second), zones)
        return union_of_zones

    def visitSubZone(self, ctx):
        if ctx.Plus():
            operator = '+'
        elif ctx.Minus():
            operator = '-'
        solid = self.visit(ctx.expr())
        return _UnaryGDMLSolid(solid.solid,
                               operator,
                               solid.centre,
                               solid.rotation)



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
            raise SyntaxError("One or more unknown operator types: %s, %s"
                              % (self.operator, other.operator))

    def _combine_minus_plus(self, other):
        return other._combine_plus_minus(self)

    def _combine_plus_minus(self, other):
        output_name = "%s_p_%s" % (self.solid.name, other.solid.name)

        other_transformation = self._get_transformation(other)

        output_solid = _pygdml.solid.Subtraction(output_name,
                                                 self.solid,
                                                 other.solid,
                                                 other_transformation)
        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation
        _logger.debug("boolean: type=Subtraction; name=%s; "
                          "solid1=%s; solid2=%s; trans=%s",
                          output_name, self.solid.name,
                          other.solid.name, other_transformation)

        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)

    def _combine_plus_plus(self, other):

        output_name = "%s_i_%s" % (self.solid.name,
                                   other.solid.name)
        other_transformation = self._get_transformation(other)
        output_solid = _pygdml.solid.Intersection(output_name,
                                                  self.solid,
                                                  other.solid,
                                                  other_transformation)
        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation
        _logger.debug("boolean: type=Intersection; name=%s; "
                          "solid1=%s; solid2=%s; trans=%s",
                          output_name, self.solid.name,
                          other.solid.name, other_transformation)

        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)

    def _combine_minus_minus(self, other):
        output_name = "%s_m_%s" % (self.solid.name,
                                         other.solid.name)
        other_transformation = self._get_transformation(other)

        output_operator = '-'
        output_centre = self.centre
        output_rotation = self.rotation
        output_solid =  _pygdml.Union(output_name,
                                       self.solid,
                                       other.solid,
                                       other_transformation)
        _logger.debug("boolean: type=Union; name=%s; "
                          "solid1=%s; solid2=%s; trans=%s",
                          output_name, self.solid.name,
                          other.solid.name, other_transformation)

        return _UnaryGDMLSolid(output_solid,
                               output_operator,
                               output_centre,
                               output_rotation)

    def union(self, other):
        output_name = "%s_u_%s" % (self.solid.name, other.solid.name)
        other_transformation = self._get_transformation(other)

        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation

        output_solid =  _pygdml.Union(output_name,
                                      self.solid,
                                      other.solid,
                                      other_transformation)
        _logger.debug("boolean: type=Union; name=%s; "
                          "solid1=%s; solid2=%s; trans=%s",
                          output_name, self.solid.name,
                          other.solid.name, other_transformation)

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
