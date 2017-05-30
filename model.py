from collections import namedtuple as _namedtuple
from collections import Counter as _Counter
import logging as _logging
import os.path as _path
import warnings as _warnings
from uuid import uuid4 as _uuid4
import time as _time
import cPickle as _cPickle

import antlr4 as _antlr4
import pygdml as _pygdml
from pygdml import transformation as _trf

import pyfluka.bodies
import pyfluka.materials as materials
from pyfluka.vector import Three
from pyfluka.Parser.FlukaParserVisitor import FlukaParserVisitor
from pyfluka.Parser.FlukaParserListener import FlukaParserListener
from pyfluka.Parser.Parse import Parse

_logger = _logging.getLogger(__name__)
class Model(object):
    """
    Class for loading Fluka model geometry, viewing its mesh, and
    writing to GDML.

    Parameters
    ---------

    filename:  path to Fluka input file

    """

    def __init__(self, filename):
        self._filename = filename
        _logger.info("creating pyfluka model from file %s",
                     _path.basename(filename))
        _logging.basicConfig(level=_logging.DEBUG,
                             format='%(name)-20s %(levelname)-8s %(message)s',
                             datefmt='%m-%d %H:%M',
                             filename=_path.basename(
                                 (_path.splitext(self._filename)[0])
                                 + ".log"),
                             filemode='w')

        # get the syntax tree.
        self.tree = Parse(filename)
        self.materials = self._materials_from_tree()
        (self.bodies,
         self._region_scale_map,
         self._body_freq_map) = self._bodies_from_tree()
        self.regions = self._regions_from_tree()
        # Initialiser the world volume:
        self._world_volume = self._gdml_world_volume()

    def _regions_from_tree(self):
        """
        Get the region definitions from the tree.  Called in the
        initialiser and then never called again.

        """
        visitor = _FlukaRegionVisitor(self.bodies,
                                      self.materials,
                                      self._region_scale_map)
        visitor.visit(self.tree)
        return visitor.regions

    def _gdml_world_volume(self):
        """
        This method insantiates the world volume.

        """
        world_size = max(self._region_scale_map.values()) * 5.0
        _logger.debug("worldvolume: name=world; dimensions=%s", world_size)
        world_box = _pygdml.solid.Box("world", world_size, world_size, world_size)
        return _pygdml.Volume([0, 0, 0], [0, 0, 0], world_box, "world-volume",
                              None, 1, False, "G4_Galactic")

    def write_to_gdml(self, region_names=None, out_path=None, make_gmad=False):
        """
        Convert the region to GDML.  Default output file name is
        "./" + basename + ".gdml".

        Parameters
        ---------

        region_names: A name or list of names of regions to be
        converted to GDML.  By default, all regions will be converted.

        out_path: Output path for file to be written to.  By default
        will make a name based on the model filename.

        make_gmad: Generate a skeleton GMAD file pre-filled with
        references to corresponding the GDML file.

        """
        self._generate_mesh(region_names)
        if out_path is None:
            out_path = ("./"
                        + _path.basename(_path.splitext(self._filename)[0])
                        + ".gdml")
        elif _path.splitext(out_path)[1] != "gdml":
            out_path = _path.splitext(out_path)[0] + ".gdml"

        out = _pygdml.Gdml()
        out.add(self._world_volume)
        out.write(out_path)

        if make_gmad is True:
            self._write_test_gmad(out_path)

    def view(self, region_names=None, setclip=True):
        """
        View the mesh for this model.

        Parameters
        ----------

        region_names: A name or list of names of regions to be
        viewed.  By default, all regions will be viewed.

        setclip: If True, will  clip the bounding box to the extent
        of the geometry.  This is useful for checking placements and
        as an optimisation--the mesh will only be generated once.  By
        default, the bounding box will be clipped.

        """
        world_mesh = self._generate_mesh(region_names, setclip=setclip)
        viewer = _pygdml.VtkViewer()
        viewer.addSource(world_mesh)
        viewer.view()

    def _generate_mesh(self, region_names, setclip=True):
        """
        This function has the side effect of recreating the world
        volume if the region_names requested are different to the ones
        already assigned to it and returns the relevant mesh.

        """
        self._compose_world_volume(region_names)
        start = _time.time()
        try:
            if setclip:
                self._world_volume.setClip()
            world_mesh = self._world_volume.pycsgmesh()
        except _pygdml.solid.NullMeshError as error:
            self._null_mesh_handler(error)
        end = _time.time()
        print "Time spent meshing world:", (end - start)/60.0, "minutes."
        return world_mesh

    def _compose_world_volume(self, region_names):
        """
        Add the region or regions in region_names to the world volume,
        only if not already added.

        """
        if region_names is None:
            region_names = self.regions.keys()
        # Coerce a string to a single-element list.
        elif isinstance(region_names, basestring):
            region_names = [region_names]
        # if the world volume consists of different regions to the
        # ones requested, then redo it with the requested volumes.
        if (set(region_names) != set([volume.name
                                      for volume
                                      in self._world_volume.daughterVolumes])):
            self._world_volume = self._gdml_world_volume()
            for region_name in list(region_names):
                self.regions[region_name].add_to_volume(self._world_volume)

    def report_body_count(self):
        """
        Prints the frequency of bodies in order and by type that are used
        in region definitions.  Bodies which are defined but not used
        are not included in this count.
        """
        body_and_count = self._body_freq_map.items()
        body_and_count.sort(key=lambda i: i[1], reverse=True)
        # Print result, with alignment.
        print "Bodies used in region definitions:"
        for body, count in body_and_count:
            body_description = (
                body
                + " - "
                + pyfluka.bodies.code_meanings[body]).ljust(60, '.')
            print body_description + str(count)

    def _materials_from_tree(self):
        # This gets the materials and maps them to their region (volumes)
        material_listener = _FlukaMaterialGetter()
        walker = _antlr4.ParseTreeWalker()
        walker.walk(material_listener, self.tree)
        return material_listener.region_material_map

    def _bodies_from_tree(self):
        """
        return a tuple of bodies, region scale, and a count of bodies
        by type.

        """
        body_listener = _FlukaBodyListener()
        walker = _antlr4.ParseTreeWalker()
        walker.walk(body_listener, self.tree)
        body_freq_map = body_listener.body_freq_map
        region_max_scale_map = body_listener.region_max_scale_map
        bodies = body_listener.bodies
        return bodies, region_max_scale_map, body_freq_map

    def _write_test_gmad(self, gdml_path):
        gmad_path = _path.splitext(gdml_path)[0] + ".gmad"
        with open(gmad_path, 'w') as gmad:
            # Extent of the bounding box in the transverse directions:
            bounding_x = self._world_volume.currentVolume.pX / 1000.
            bounding_y = self._world_volume.currentVolume.pY / 1000.
            diameter = 2 * max(bounding_x, bounding_y)
            length = 2 * self._world_volume.currentVolume.pZ / 1000.

            gmad.write("test_component: element, l={}*m, geometry=\"gdml:{}\","
                       " outerDiameter={}*m;\n".format(length,
                                                       gdml_path,
                                                       diameter))
            gmad.write('\n')
            gmad.write("component : line = (test_component);\n")
            gmad.write('\n')
            gmad.write("beam,  particle=\"e-\",\n"
                       "energy=1.5 * GeV,\n"
                       "X0=0.1*um;\n")
            gmad.write('\n')
            gmad.write("use, period=component;\n")

    def test_regions(self, pickle=None, regions=None):
        """
        Method for individually meshing each region and returning
        dictionary of lists of good regions, bad regions, bad
        intersections, and bad subtractions.

        If a string is supplied for pickle, then the resulting dictionary will
        be written to file.

        """
        if regions is None:
            regions = self.regions
        elif isinstance(regions, basestring):
            regions = [regions]
        # good regions, bad regions, bad subtractions, bad intersections
        output = {key:[] for key in ["good", "bad", "subs", "ints"]}
        output["scale"] = self._region_scale_map
        number_of_regions = len(regions)
        start = _time.time()
        for index, region_name in enumerate(regions):
            print "... Testing Region: %s" % region_name
            try:
                self._generate_mesh(region_name)
                output["good"].append(region_name)
            except _pygdml.solid.NullMeshError as error:
                output["bad"].append(region_name)
                if isinstance(error.solid, _pygdml.solid.Subtraction):
                    output["subs"].append(region_name)
                elif isinstance(error.solid, _pygdml.solid.Intersection):
                    output["ints"].append(region_name)
            print "Tested {0}/{1}.".format(index + 1, number_of_regions)
            print ("Succeded: {}.  Failed: {} ({:.2%}).".format(
                len(output["good"]),
                len(output["bad"]),
                (len(output["good"])
                 / (len(output["good"])
                    + float(len(output["bad"]))))))

        end = _time.time()
        print (end - start)/60.0, "minutes elipsed since test begun."

        if pickle:
            with open("./{}_diag.pickle".format(
                    self._filename + pickle), 'w') as f:
                _cPickle.dump(output, f)
        return output

    def view_debug(self, region=None, do_all=False):
        """
        If region name is specified then view that in debug mode, else
        attempt to mesh each region in turn and view the first null
        mesh in debug mode, and then exits.  If do_all is not False
        then will not exit after the first null mesh, and will instead
        try to view all regions in turn.

        """
        if region is not None:
            self.regions[region].view_debug()
            return

        for region in self.regions.itervalues():
            try:
                region.gdml_solid.pycsgmesh()
            except _pygdml.solid.NullMeshError:
                print "Failed mesh @ region: {}.".format(region.name)
                print "Viewing region in debug mode ..."
                region.view_debug()
                if do_all is False:
                    break

    def _null_mesh_handler(self, error):
        solid = error.solid
        solid_type = type(error.solid).__name__
        _logger.exception("nullmesh: type=%s, name=%s; solid1=%s;"
                          " solid2=%s; trans=%s", solid_type, solid.name,
                          solid.obj1.name, solid.obj2.name, solid.tra2)
        raise error

    def view_bodies(self, bodies):
        if isinstance(bodies, basestring):
            bodies = [bodies]
        world_volume = self._gdml_world_volume()
        for body in bodies:
            print body
            self.bodies[body].add_to_volume(world_volume)
        world_mesh = world_volume.pycsgmesh()
        viewer = _pygdml.VtkViewer()
        viewer.addSource(world_mesh)
        viewer.view()



class _FlukaMaterialGetter(FlukaParserListener):
    # This class gets the materials as pygdml.materials instances.
    # Or perhaps as pyfluka.materials Material instances (???)

    def __init__(self):
        self.materials = materials.fluka_g4_material_map
        self.region_material_map = dict()

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
            if type(ctx) is _antlr4.tree.Tree.TerminalNodeImpl:
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
    """
    This class is for getting simple, declarative  information about
    the geometry model.  In no particular order:

    - Body definitions, including surrounding geometry directives
    - Region "scale" for use in defining infinite cylinders and planes.
    - Stats like names and frequencies for body types and regions.

    """
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
        # These two are transient attributes which record the current
        # region name and the corresponding max_scale.
        self.region_name = ctx.RegionName().getText()
        self.max_scale = 0.0

    def exitRegion(self, ctx):
        # As we exit the region, record the max_scale for this region.
        self.region_max_scale_map[self.region_name] = self.max_scale

    def enterBodyDefSpaceDelim(self, ctx):
        # This is where we get the body definitions and instantiate
        # them with the relevant pyfuka.bodies classes.
        body_name = ctx.ID().getText()
        body_type = ctx.BodyCode().getText()
        body_parameters = self._get_floats(ctx)
        body_constructor = getattr(pyfluka.bodies, body_type)
        # Try and construct the body, if it's not implemented then add
        # it to the list of omitted bodies.
        try:
            body = body_constructor(body_name,
                                    body_parameters,
                                    self._transform_stack,
                                    self._translat_stack,
                                    self._expansion_stack)
            self.bodies[body_name] = body
        except TypeError:
            _warnings.simplefilter('once', UserWarning)
            _warnings.warn(("\nBody type %s not supported.  All bodies"
                            " of this type will be omitted.  If bodies"
                            " of this type are used in regions, the"
                            " conversion will fail.") % body_type,
                           UserWarning)
            self.omitted_bodies.append((body_name, body_type))

    def enterUnaryExpression(self, ctx):
        # Here we assign max_scale the current body's extent if it's
        # larger than the previous max_scale.
        body_name = ctx.ID().getText()
        try:
            self.max_scale = max(self.max_scale,
                                 abs(self.bodies[body_name].extent()))
        except KeyError:
            raise KeyError(("Undefined body \"{}\""
                            " in region: \"{}\"!".format(body_name,
                                                         self.region_name)))

        # For logging purposes.  If body hasn't yet been recorded as
        # used, then record its name and type.
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
        floats = map(lambda x: 10 * x, floats)
        return floats

    def exitGeocards(self, ctx):
        # When we've finished walking the geometry, count the bodies.
        self.body_freq_map = _Counter(self.used_bodies_by_type)
        del self.used_bodies_by_type



class _FlukaRegionVisitor(FlukaParserVisitor):
    def __init__(self, bodies, materials, _region_scale_map):
        self.bodies = bodies
        self.regions = dict()
        self.materials = materials
        self._region_scale_map = _region_scale_map

    def visitRegion(self, ctx):
        self.region_name = ctx.RegionName().getText()
        region_solid = self.visitChildren(ctx)
        region_centre = [region_solid.centre.x,
                         region_solid.centre.y,
                         region_solid.centre.z]

        region_rotation = region_solid.rotation
        region_gdml = region_solid.solid
        region_name = ctx.RegionName().getText()

        # This allows us to plot subtractions without something to
        # subtract from.  Useful for looking at all the solids.
        if region_solid.operator == '+' or region_solid.operator == '-':
            _logger.debug("volume: name=%s; position=%s; rotation=%s; solid=%s",
                          region_name, region_centre,
                          _trf.matrix2tbxyz(region_rotation), region_gdml.name)
            self.regions[region_name] = bodies.Region(region_name,
                                                      region_gdml,
                                                      position=region_centre,
                                                      rotation=region_rotation)

    def visitUnaryAndBoolean(self, ctx):
        left_solid = self.visit(ctx.unaryExpression())
        right_solid = self.visit(ctx.expr())
        return left_solid.combine(right_solid)

    def visitUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()

        body = self.bodies[body_name]
        body_type = type(body).__name__

        # If an infinite body:
            scale = self._region_scale_map[self.region_name] * 10.
        if isinstance(body, pyfluka.bodies._InfiniteSolid):
            # Infinite bodies are factories for themselves, allowing
            # for dynamic infinite scale for a common underlying body.
            body = body(scale)
            _logger.debug("infinite solid:  type=%s; scale=%s",
                          body_type, scale)

        gdml_solid = body.gdml_solid()
        body_centre = body.centre()
        body_rotation = body.get_rotation_matrix()

        if ctx.Plus():
            return _UnarySolid(gdml_solid, '+', body_centre, body_rotation)
        else:
            return _UnarySolid(gdml_solid, '-', body_centre, body_rotation)

    def visitUnaryAndSubZone(self, ctx):
        first = self.visit(ctx.subZone())
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
        return _UnarySolid(solid.solid,
                               operator,
                               solid.centre,
                               solid.rotation)



class _UnarySolid(object):
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
        Combine two _UnarySolids, returning the third resultant.
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
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_solid = _pygdml.solid.Subtraction(output_name,
                                                 self.solid,
                                                 other.solid,
                                                 relative_transformation)
        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation
        _logger.debug("boolean: type=Subtraction; name=%s; "
                      "solid1=%s; solid2=%s; trans=%s",
                      output_name, self.solid.name,
                      other.solid.name, [relative_angles, relative_translation])

        return _UnarySolid(output_solid,
                           output_operator,
                           output_centre,
                           output_rotation)

    def _combine_plus_plus(self, other):
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_solid = _pygdml.solid.Intersection(output_name,
                                                  self.solid,
                                                  other.solid,
                                                  relative_transformation)
        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation
        _logger.debug("boolean: type=Intersection; name=%s; "
                      "solid1=%s; solid2=%s; trans=%s",
                      output_name, self.solid.name,
                      other.solid.name, [relative_angles, relative_translation])

        return _UnarySolid(output_solid,
                           output_operator,
                           output_centre,
                           output_rotation)

    def _combine_minus_minus(self, other):
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_operator = '-'
        output_centre = self.centre
        output_rotation = self.rotation
        output_solid = _pygdml.Union(output_name,
                                     self.solid,
                                     other.solid,
                                     relative_transformation)
        _logger.debug("boolean: type=Union; name=%s; "
                      "solid1=%s; solid2=%s; trans=%s",
                      output_name, self.solid.name,
                      other.solid.name, [relative_angles, relative_translation])

        return _UnarySolid(output_solid,
                           output_operator,
                           output_centre,
                           output_rotation)

    def union(self, other):
        """
        Method for doing the union of this UnarySolid with
        another.  rotations and translations are propagates
        appropriately to the daughter solid.

        """
        output_name = self._generate_name(other)

        relative_translation = self._get_relative_translation(other)
        relative_angles = self._get_relative_rotation(other)
        relative_transformation = [relative_angles, relative_translation]

        output_operator = '+'
        output_centre = self.centre
        output_rotation = self.rotation

        output_solid = _pygdml.Union(output_name,
                                     self.solid,
                                     other.solid,
                                     relative_transformation)
        _logger.debug("boolean: type=Union; name=%s; "
                      "solid1=%s; solid2=%s; trans=%s",
                      output_name, self.solid.name,
                      other.solid.name, [relative_angles, relative_translation])

        return _UnarySolid(output_solid,
                           output_operator,
                           output_centre,
                           output_rotation)

    def _get_relative_rot_matrix(self, other):
        return self.rotation.T.dot(other.rotation)

    def _get_relative_translation(self, other):
        # In a boolean rotation, the first solid is centred on zero,
        # so to get the correct offset, subtract from the second the
        # first, and then rotate this offset with the rotation matrix.
        offset_vector =  Three(other.centre.x - self.centre.x,
                               other.centre.y - self.centre.y,
                               other.centre.z - self.centre.z)
        mat = self.rotation.T
        offset_vector = mat.dot(offset_vector).view(Three)
        try:
            x = offset_vector[0][0]
            y = offset_vector[0][1]
            z = offset_vector[0][2]
        except IndexError:
            x = offset_vector.x
            y = offset_vector.y
            z = offset_vector.z
        return Three(x,y,z)

    def _get_relative_rotation(self, other):
        # The first solid is unrotated in a boolean operation, so it
        # is in effect rotated by its inverse.  We apply this same
        # rotation to the second solid to get the correct relative
        # rotation.
        return _trf.matrix2tbxyz(self._get_relative_rot_matrix(other))

    def _generate_name(self, other):
        name = str(_uuid4())
        name = name.replace("-","")
        return "a" + name

def load_pickle(path):
    with open(path, 'r') as f:
        o = _cPickle.load(f)
    return o
