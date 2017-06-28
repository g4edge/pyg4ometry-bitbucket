""" Collection of classes for extracting information from a Fluka model. """

from __future__ import division, print_function
import collections
import os.path
import time
import cPickle
import warnings

import antlr4
import pygdml

import pyfluka.geometry
import pyfluka.vector
from pyfluka.Parser.FlukaParserVisitor import FlukaParserVisitor
from pyfluka.Parser.FlukaParserListener import FlukaParserListener
from pyfluka.Parser.Parse import Parse

class Model(object):
    """
    Class for loading Fluka model geometry, viewing its mesh, and
    writing to GDML.

    Parameters
    ----------

    filename:  path to Fluka input file

    """

    def __init__(self, filename):
        self._filename = filename
        # get the syntax tree.
        tree = Parse(filename)
        self.bodies, self._body_freq_map = Model._bodies_from_tree(tree)
        self.regions = self._regions_from_tree(tree)
        # Initialiser the world volume:
        self._world_volume = Model._gdml_world_volume()

    def _regions_from_tree(self, tree):
        """Get the region definitions from the tree.  Called in the
        initialiser and then never called again.

        """
        visitor = FlukaRegionVisitor(self.bodies)
        visitor.visit(tree)
        return visitor.regions

    @staticmethod
    def _gdml_world_volume():
        """ This method insantiates the world volume. """
        world_size = 1e5
        world_box = pygdml.solid.Box("world", world_size, world_size, world_size)
        return pygdml.Volume([0, 0, 0], [0, 0, 0], world_box, "world-volume",
                             None, 1, False, "G4_Galactic")

    def write_to_gdml(self, regions=None, out_path=None,
                      make_gmad=True, optimise=True):
        """Convert the region to GDML.

        Parameters
        ----------

        - regions: A name or list of names of regions to be
        converted to GDML.  By default, all regions will be converted.

        - out_path: Output path for file to be written to.  By default
        output file name is "./" + basename + ".gdml".

        - make_gmad: Generate a skeleton GMAD file pre-filled with
        references to corresponding the GDML file.

        - optimise: Optimise the output GDML by trimming large body
          definitions.  By default the geometry will be optimised.

        """
        self._generate_mesh(regions, setclip=True, optimise=optimise)
        if out_path is None:
            out_path = ("./"
                        + os.path.basename(os.path.splitext(self._filename)[0])
                        + ".gdml")
        elif os.path.splitext(out_path)[1] != "gdml":
            out_path = os.path.splitext(out_path)[0] + ".gdml"

        out = pygdml.Gdml()
        out.add(self._world_volume)
        out.write(out_path)

        if make_gmad is True:
            self._write_test_gmad(out_path)

    def view(self, regions=None, setclip=True, optimise=False):
        """View the mesh for this model.

        Parameters
        ----------

        - regions: A name or list of names of regions to be viewed.
        By default, all regions will be viewed.

        - setclip: If True, will clip the bounding box to the extent
        of the geometry.  Setting it to False is useful for checking
        placements and as an optimisation--the mesh will only be
        generated once.  By default, the bounding box will be clipped.

        """
        world_mesh = self._generate_mesh(regions,
                                         setclip=setclip,
                                         optimise=optimise)
        viewer = pygdml.VtkViewer()
        viewer.addSource(world_mesh)
        viewer.view()

    def _generate_mesh(self, region_names, setclip, optimise):
        """This function has the side effect of recreating the world volume if
        the region_names requested are different to the ones already
        assigned to it and returns the relevant mesh.

        """
        self._compose_world_volume(region_names, optimise=optimise)
        if setclip:
            self._world_volume.setClip()
        world_mesh = self._world_volume.pycsgmesh()
        return world_mesh

    def _compose_world_volume(self, regions, optimise):
        """Add the region or regions in region_names to the world volume, only
        if not already added.

        If regions is None:  do all regions
        If regions is a string:  do just that one region
        If regions is a list of strings:  do those
        If regions is a dict of region names with zone numbers:  Do
        those regions but only the zones in the list.

        """
        self._world_volume = Model._gdml_world_volume()
        if regions is None:
            regions = self.regions.keys()
        # Coerce a string to a single-element list.
        elif isinstance(regions, basestring):
            regions = [regions]
        elif isinstance(regions, dict):
            for region_name, zone_nos in regions.iteritems():
                # print "Adding region {}, zones {}".format(region_name, zone_nos
                self.regions[region_name].add_to_volume(self._world_volume,
                                                        optimise=optimise,
                                                        zones=zone_nos)
            return None

        for region_name in regions:
            print("Adding region: \"{}\"  ...".format(region_name))
            self.regions[region_name].add_to_volume(self._world_volume,
                                                    optimise=optimise)

    def report_body_count(self):
        """Prints a count of all unique bodies by type which are used in
        region defintions.

        """
        body_and_count = self._body_freq_map.items()
        body_and_count.sort(key=lambda i: i[1], reverse=True)
        # Print result, with alignment.
        print("Bodies used in region definitions:")

        body_code_definitions = {
            "ARB": "Abitrary Convex Polyhedron",
            "BOX": "General Rectangular Parallelepiped",
            "ELL": "Elippsoid of Revolution",
            "PLA": "Generic Infinite Half-space",
            "QUA": "Generic Quadric",
            "RAW": "Right Angle Wedge",
            "RCC": "Right Circular Cylinder",
            "REC": "Right Ellitpical Cylinder",
            "RPP": "Rectangular Parallelepiped",
            "SPH": "Sphere",
            "TRC": "Truncated Right Angle Cone",
            "WED": "Right Angle Wedge",
            "XCC": "Infinite Circular Cylinder parallel to the x-axis",
            "XEC": "Infinite Elliptical Cylinder parallel to the x-axis",
            "XYP": "Infinite Half-space perpendicular to the z-axis",
            "XZP": "Infinite Half-space perpendicular to the y-axis",
            "YCC": "Infinite Circular Cylinder parallel to the y-axis",
            "YEC": "Infinite Elliptical Cylinder parallel to the y-axis",
            "YZP": "Infinite Half-space perpendicular to the x-axis",
            "ZCC": "Infinite Circular Cylinder parallel to the z-axis",
            "ZEC": "Infinite Elliptical Cylinder parallel to the z-axis"
        }

        for body, count in body_and_count:
            body_description = (
                body
                + " - "
                + body_code_definitions[body]).ljust(60, '.')
            print(body_description + str(count))

    @staticmethod
    def _bodies_from_tree(tree):
        """Return a tuple of bodies, region scale, and a count of bodies by
        type.

        """
        body_listener = FlukaBodyListener()
        walker = antlr4.ParseTreeWalker()
        walker.walk(body_listener, tree)
        body_freq_map = body_listener.body_freq_map
        bodies = body_listener.bodies
        return bodies, body_freq_map

    def _write_test_gmad(self, gdml_path):
        """Write a simple gmad file corresponding corresponding to the input
        file's geometry with the correct GDML component length.

        """
        gmad_path = os.path.splitext(gdml_path)[0] + ".gmad"
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

    def test_regions(self, pickle=None, regions=None, optimise=True):
        """Individually mesh each region and return dictionary of lists of
        good regions, bad regions, bad intersections, and bad
        subtractions.

        If a string is supplied for pickle, then the resulting dictionary will
        be written to file.

        """
        if regions is None:
            regions = self.regions
        elif isinstance(regions, basestring):
            regions = {regions: self.regions[regions]}
        # good regions, bad regions, bad subtractions, bad intersections
        output = {key:[] for key in ["good", "bad", "subs", "ints"]}
        number_of_regions = len(regions)
        start = time.time()
        for index, region_name in enumerate(regions):
            print("... Testing Region: %s" % region_name)
            try:
                self._generate_mesh(region_name,
                                    setclip=False,
                                    optimise=optimise)
                output["good"].append(region_name)
            except pygdml.solid.NullMeshError as error:
                output["bad"].append(region_name)
                if isinstance(error.solid, pygdml.solid.Subtraction):
                    output["subs"].append(region_name)
                elif isinstance(error.solid, pygdml.solid.Intersection):
                    output["ints"].append(region_name)
            print("Tested {0}/{1}.".format(index + 1, number_of_regions))
            print("Succeded: {}.  Failed: {} ({:.2%}).".format(
                len(output["good"]),
                len(output["bad"]),
                (len(output["good"])
                 / (len(output["good"]) + len(output["bad"])))))

        duration = (time.time() - start) / 60.0
        print(duration, "minutes since test begun.")
        output['time'] = duration

        if pickle:
            pickle_name = "./{}_diag.pickle".format(self._filename)
            with open(pickle_name, 'w') as pickle_file:
                cPickle.dump(output, pickle_file)
        return output

    def view_debug(self, region=None, do_all=False):
        """If region name is specified then view that in debug mode, else
        attempt to mesh each region in turn and view the first null
        mesh in debug mode, and then exit.  If do_all is not False
        then will not exit after the first null mesh, and will instead
        try to view all regions in turn.

        """
        if region is not None:
            self.regions[region].view_debug()
            return

        for region in self.regions.itervalues():
            try:
                region.gdml_solid.pycsgmesh()
            except pygdml.solid.NullMeshError:
                print("Failed mesh @ region: {}.".format(region.name))
                print("Viewing region in debug mode ...")
                region.view_debug()
                if do_all is False:
                    break

    def survey(self, pickle=False):
        """Perform a survey of this model's geometry.  This consists of
        meshing every region and individual zone and storing their
        extents, lengths, and centres.  As Fluka regions need not be
        contiguous, this can be useful for selecting and omitting
        geometry based on position.

        """
        regions = dict()
        for region_name, region in self.regions.iteritems():
            regions[region_name] = region.extent()
            print("Meshing Region: {} ...".format(region_name))
            if len(region.zones) == 1:
                continue
            for zone_no, zone in region.zones.iteritems():
                print("Meshing Region: {}, Zone: {} ...".format(region_name,
                                                                zone_no))
                regions["{}_{}".format(region_name, zone_no)] = zone.extent()

        if pickle is True:
            pickle_name = "./{}_survey.pickle".format(
                os.path.basename(os.path.splitext(self._filename)[0])
            )
            with open(pickle_name, 'w') as pickle_file:
                cPickle.dump(regions, pickle_file)
        return regions

    def __repr__(self):
        return "<Model: \"{}\">".format(self._filename)


class FlukaBodyListener(FlukaParserListener):
    """
    This class is for getting simple, declarative  information about
    the geometry model.  In no particular order:

    - Body definitions, including surrounding geometry directives
    - Stats like names and frequencies for body types and regions.

    """
    def __init__(self):
        self.bodies = dict()

        self.body_freq_map = dict()
        self.unique_body_names = set()
        self.used_bodies_by_type = list()

        self.transform_stack = []
        self.current_translat = None
        self.current_expansion = None

    def enterBodyDefSpaceDelim(self, ctx):
        # This is where we get the body definitions and instantiate
        # them with the relevant pyfuka.bodies classes.
        body_name = ctx.ID().getText()
        body_type = ctx.BodyCode().getText()
        body_parameters = FlukaBodyListener._get_floats(ctx)
        # Apply any expansions:
        body_parameters = self.apply_expansions(body_parameters)

        # Try and construct the body, if it's not implemented then warn
        try:
            body_constructor = getattr(pyfluka.geometry, body_type)
            body = body_constructor(body_name,
                                    body_parameters,
                                    self.transform_stack,
                                    self.current_translat)
            self.bodies[body_name] = body
        except (AttributeError, NotImplementedError):
            warnings.simplefilter('once', UserWarning)
            warnings.warn(("\nBody type %s not supported.  All bodies"
                           " of this type will be omitted.  If bodies"
                           " of this type are used in regions, the"
                           " conversion will fail.") % body_type,
                          UserWarning)

    def enterUnaryExpression(self, ctx):
        body_name = ctx.ID().getText()
        # used, then record its name and type.
        if body_name not in self.unique_body_names:
            self.unique_body_names.add(body_name)
            body_type = type(self.bodies[body_name]).__name__
            self.used_bodies_by_type.append(body_type)

    def enterTranslat(self, ctx):
        translation = FlukaBodyListener._get_floats(ctx)
        self.current_translat = pyfluka.vector.Three(translation)

    def exitTranslat(self, ctx):
        self.current_translat = None

    def enterExpansion(self, ctx):
        self.current_expansion = float(ctx.Float().getText())

    def exitExpansion(self, ctx):
        self.current_expansion = None

    def apply_expansions(self, parameters):
        """
        Method for applying the current expansion to the parameters.

        """
        factor = self.current_expansion
        if factor is not None:
            return [factor * x for x in parameters]
        else:
            return parameters

    @staticmethod
    def _get_floats(ctx):
        '''
        Gets the Float tokens associated with the rule and returns
        them as an array of python floats.
        '''
        float_strings = [i.getText() for i in ctx.Float()]
        floats = map(float, float_strings)
        # Converting centimetres to millimetres!!!
        floats = [10 * x for x in floats]
        return floats

    def exitGeocards(self, ctx):
        # When we've finished walking the geometry, count the bodies.
        self.body_freq_map = collections.Counter(self.used_bodies_by_type)
        del self.used_bodies_by_type


class FlukaRegionVisitor(FlukaParserVisitor):
    """
    A visitor class for accumulating the region definitions.  The body
    instances are provided at instatiation, and then these are used
    when traversing the tree to build up a dictionary of region name
    and pyfluka.geometry.Region instances.

    """
    def __init__(self, bodies):
        self.bodies = bodies
        self.regions = dict()

    def visitSimpleRegion(self, ctx):
        # Simple in the sense that it consists of no unions of Zones.
        region_defn = self.visitChildren(ctx)
        # Build a zone from the list of bodies or single body:
        zone = pyfluka.geometry.Zone(region_defn)
        region_name = ctx.RegionName().getText()
        self.regions[region_name] = pyfluka.geometry.Region(region_name, zone)

    def visitComplexRegion(self, ctx):
        # Complex in the sense that it consists of the union of
        # multiple zones.

        # Get the list of tuples of operators and bodies/zones
        region_defn = self.visitChildren(ctx)
        # Construct zones out of these:
        zones = [pyfluka.geometry.Zone(defn) for defn in region_defn]
        region_name = ctx.RegionName().getText()
        region = pyfluka.geometry.Region(region_name, zones)
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
        zone = pyfluka.geometry.Zone(solids)
        return (operator, zone)

def load_pickle(path):
    """
    Convenience function for loading pickle files.

    """
    with open(path, 'r') as file_object:
        unpickled = cPickle.load(file_object)
    return unpickled
