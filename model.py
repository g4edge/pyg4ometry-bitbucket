from collections import namedtuple as _namedtuple
from collections import Counter as _Counter
import os.path as _path
import warnings as _warnings
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
        # get the syntax tree.
        self.tree = Parse(filename)
        self.bodies, self._body_freq_map = self._bodies_from_tree()
        self.regions = self._regions_from_tree()
        # Initialiser the world volume:
        self._world_volume = self._gdml_world_volume()

    def _regions_from_tree(self):
        """
        Get the region definitions from the tree.  Called in the
        initialiser and then never called again.

        """
        visitor = _FlukaRegionVisitor(self.bodies)
        visitor.visit(self.tree)
        return visitor.regions

    def _gdml_world_volume(self):
        """
        This method insantiates the world volume.

        """
        world_size = 1e5
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

    def view(self, regions=None, setclip=True):
        """
        View the mesh for this model.

        Parameters
        ----------

        regions: A name or list of names of regions to be
        viewed.  By default, all regions will be viewed.

        setclip: If True, will  clip the bounding box to the extent
        of the geometry.  This is useful for checking placements and
        as an optimisation--the mesh will only be generated once.  By
        default, the bounding box will be clipped.

        """
        world_mesh = self._generate_mesh(regions, setclip=setclip)
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

    def _bodies_from_tree(self):
        """
        return a tuple of bodies, region scale, and a count of bodies
        by type.

        """
        body_listener = _FlukaBodyListener()
        walker = _antlr4.ParseTreeWalker()
        walker.walk(body_listener, self.tree)
        body_freq_map = body_listener.body_freq_map
        bodies = body_listener.bodies
        return bodies, body_freq_map

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

        duration = (_time.time() - start) / 60.0
        print duration, "minutes since test begun."
        output['time'] = duration

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
        except NotImplementedError:
            _warnings.simplefilter('once', UserWarning)
            _warnings.warn(("\nBody type %s not supported.  All bodies"
                            " of this type will be omitted.  If bodies"
                            " of this type are used in regions, the"
                            " conversion will fail.") % body_type,
                           UserWarning)
            self.omitted_bodies.append((body_name, body_type))

    def enterUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()
        # used, then record its name and type.
        if body_name not in self.unique_body_names:
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
    def __init__(self, bodies):
        self.bodies = bodies
        self.regions = dict()

    def visitSimpleRegion(self, ctx):
        # Simple in the sense that it consists of no unions of Zones.
        region_defn = self.visitChildren(ctx)
        # Build a zone from the list of bodies or single body:
        zone = pyfluka.bodies.Zone(region_defn)
        region_name = ctx.RegionName().getText()
        region = pyfluka.bodies.Region(region_name, zone)
        self.regions[region_name] = pyfluka.bodies.Region(region_name, zone)

    def visitComplexRegion(self, ctx):
        # Complex in the sense that it consists of the union of
        # multiple zones.

        # Get the list of tuples of operators and bodies/zones
        region_defn = self.visitChildren(ctx)
        # Construct zones out of these:
        zones = [pyfluka.bodies.Zone(defn) for defn in region_defn]
        region_name = ctx.RegionName().getText()
        region = pyfluka.bodies.Region(region_name, zones)
        self.regions[region_name] = region

    def visitUnaryAndBoolean(self, ctx):
        left_solid = self.visit(ctx.unaryExpression())
        right_solid = self.visit(ctx.expr())

        # If both are tuples (i.e. operator, body/zone pairs):
        if (isinstance(left_solid, tuple)
            and isinstance(right_solid, tuple)):
            return [left_solid, right_solid]
        elif (isinstance(left_solid, tuple)
              and isinstance(right_solid, list)):
            right_solid.append(left_solid)
            return right_solid
        else:
            raise RuntimeError("dunno what's going on here")

    def visitUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()
        body = self.bodies[body_name]
        if ctx.Plus():
            return  ('+', body)
        elif ctx.Minus():
            return ('-', body)

    def visitUnaryAndSubZone(self, ctx):
        sub_zone = self.visit(ctx.subZone())
        expr = self.visit(ctx.expr())
        # If expr is already a list, append to it rather than building
        # up a series of nested lists.  This is to keep it flat, with
        # the only nesting occuring in Zones.
        if isinstance(expr, list):
            return [sub_zone] + expr
        return [sub_zone, expr]

    def visitSingleUnion(self, ctx):
        zone = [(self.visit(ctx.zone()))]
        return zone

    def visitMultipleUnion(self, ctx):
        # Get the zones:
        zones = [self.visit(zone) for zone in ctx.zone()]
        return zones

    def visitSubZone(self, ctx):
        if ctx.Plus():
            operator = '+'
        elif ctx.Minus():
            operator = '-'
        solids = self.visit(ctx.expr())
        zone = pyfluka.bodies.Zone(solids)
        return (operator, zone)

def load_pickle(path):
    with open(path, 'r') as f:
        o = _cPickle.load(f)
    return o
