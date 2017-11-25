"""Useful functions and classes to ease the use of pyfluka with BDSIM."""

from __future__ import (absolute_import, print_function, division)
import collections
import warnings
import textwrap

import ROOT

import pygdml.transformation
import pyfluka.vector

if ROOT.gSystem.Load("librebdsimLib") == -1:
    msg = ("Cannot find librebdsimLib root library.  Module \"{}\" will"
           " not be fully functional.").format(__name__)
    warnings.warn(msg)
    del msg

def _get_bdsim_rotation(fluka_direction, bdsim_rotation):
    """Get the rotation for placing the external FLUKA geometry with
    respect to the BDSIM beamline.

    fluka_direction -- a vector in the FLUKA coordinate
    system that will be aligned with the vector corresponding to the
    rotation of (0,0,1) described in `bdsim_rotation`.  This is typically the
    direction the beamline in FLUKA-world points in.
    bdsim_rotation -- AxisAngle instance providing the rotation w.r.t
    the +ve z-axis in BDSIM-world.  A typical source of such a
    rotation is the BDSOutputROOTEventModel tree in the rootevent
    output, where the rotation for each element w.r.t the positive
    z-axis can be found.

    """
    bdsim_rotation_matrix = (
        pygdml.transformation.axisangle2matrix(bdsim_rotation.axis,
                                               bdsim_rotation.angle))
    # The BDSIM rotation is w.r.t the positive z-axis, so we pick that
    # here.  This is because the beamline in BDSIM builds along +ve z.
    fluka_rotation_matrix = pygdml.matrix_from(fluka_direction, [0, 0, 1])
    net_rotation = fluka_rotation_matrix.dot(
        bdsim_rotation_matrix.dot(fluka_rotation_matrix))
    axis_angle = pygdml.transformation.matrix2axisangle(net_rotation)
    axis = axis_angle[0]
    angle = axis_angle[1]
    return AxisAngle(axis, angle)

def _get_bdsim_placement(bdsim_point, fluka_point,
                         fluka_bounding_box_origin,
                         axis, angle):
    """Return the placement that aligns fluka_point with bdsim_point in
    the BDSIM global coordinate system.  Units in mm

    Arguments:
    bdsim_point -- a point in the BDSIM world.
    fluka_point -- a coordinate in the FLUKA coordinate system.
    fluka_bounding_box_origin -- the centre of the bounding box in FLUKA-world.
    axis -- the axis part of the axis-angle rotation for the bounding
    box.  Get this from get_bdsim_rotation.
    angle -- the angle part of the axis-angle rotation for the bounding
    box.  Get this from get_bdsim_rotation.

    """
    # Convert the axis/angle back to a rotation matrix.
    rotation_matrix = pygdml.transformation.axisangle2matrix(axis, angle)
    # converts a point in the fluka coordinate system to its point in
    # the bdsim global coordinate system.
    fluka_point_in_bdsim = fluka_point - fluka_bounding_box_origin
    rotated_point = rotation_matrix.dot(fluka_point_in_bdsim).A1
    offset = bdsim_point - rotated_point
    return offset

def get_placement_string(output_name,
                         gdml_path,
                         bdsim_point,
                         fluka_point,
                         fluka_bounding_box_origin,
                         bdsim_rotation,
                         fluka_direction):
    """
    output_name -- the name of the output geometry placement.
    gdml_path -- the path of the GDML file.
    bdsim_point -- the point in BDSIM-world to coincide with
                         `fluka_point` in BDSIM-world.
    fluka_point -- the point in FLUKA-world to coincide with
                         `bdsim_point` in BDSIM-world
    fluka_bounding_box_origin -- the centre of the bounding box in
                         FLUKA-world.  This coordinate is in the
                         dictionary returned by
                         pyfluka.Model.write_to_gdml.
    bdsim_rotation -- the rotation that fluka_direction will be
                         aligned with.  You will probably want to
                         align your geometry w.r.t a specific
                         component, in which case you will find it easiest
                         this from the BDSOutputROOTEventModel tree of
                         the rootevent output for your beamline.
    fluka_direction -- the vector that will be used to align the
                         geometry parallel to the rotation
                         `bdsim_rotation` in BDSIM-world.

    """
    rotation = _get_bdsim_rotation(fluka_direction, bdsim_rotation)
    placement = _get_bdsim_placement(bdsim_point, fluka_point,
                                     fluka_bounding_box_origin,
                                     rotation.axis, rotation.angle)
    return _build_placement_string(output_name, gdml_path, placement,
                                   rotation.axis, rotation.angle)


def _build_placement_string(name, filepath, offset, axis, angle):
    """All units should be in millimetres."""
    # cast iterables to vectors.
    offset = pyfluka.vector.Three(offset)
    axis = pyfluka.vector.Three(axis)
    out = ("{name}: placement,"
           " x = {offset.x}*mm, y = {offset.y}*mm, z = {offset.z}*mm,"
           " geometryFile=\"gdml:{filepath}\", axisAngle=1,"
           " axisX = {axis.x}, axisY = {axis.y}, axisZ = {axis.z},"
           " angle = {angle};")
    out = '\n'.join(textwrap.wrap(out))
    return out.format(name=name, filepath=filepath,
                      offset=offset, axis=axis, angle=angle)

# These must be hardcoded, I think, as C++ has no reflection.
# These are per component variables.
_COMPONENT_VARS = frozenset({"componentName",
                             "placementName",
                             "componentType",
                             "length",
                             "staPos",
                             "midPos",
                             "endPos",
                             "staRot",
                             "midRot",
                             "endRot",
                             "staRefPos",
                             "midRefPos",
                             "endRefPos",
                             "staRefRot",
                             "midRefRot",
                             "endRefRot",
                             "staS",
                             "midS",
                             "endS",
                             "beamPipeType",
                             "beamPipeAper1",
                             "beamPipeAper2",
                             "beamPipeAper3",
                             "beamPipeAper4"})

# These are variables which are not per component.
_MISC_VARIABLES = frozenset({"samplerNamesUnique"})

AxisAngle = collections.namedtuple("AxisAngle", ["axis", "angle"])

class Component(collections.namedtuple("Component",
                                       _COMPONENT_VARS | {"index"})):
    """Simple class for representing a component read out of the
    BDSOutputROOTEventModel tree from BDSIM rootevent output.

    """
    # Default repr would be too big so redefine to something
    # human-readable and useful:
    def __repr__(self):
        return "<{}: {}, S={}m ...>".format(self.componentName,
                                            self.componentType,
                                            self.staS)

class Lattice(list):
    """Simple class used for inspecting BDSIM rootevent models."""
    def __init__(self, path):
        # Load the ROOT model
        data_loader = ROOT.DataLoader(path)
        model = data_loader.GetModel()
        model_tree = data_loader.GetModelTree()
        model_tree.GetEntry(0)
        model = model.model

        # Add the miscellaneous variables.
        for variable in _MISC_VARIABLES:
            sequence = list(getattr(model, variable))
            setattr(self, variable, sequence)

        # Give the model a copy of the component variables for convenience.
        self.component_variables = _COMPONENT_VARS

        # Add the per component variables.
        for index, _ in enumerate(model.componentName):
            component_vars = {variable:
                              _try_coercion(getattr(model, variable)[index])
                              for variable in _COMPONENT_VARS}
            self.append(Component(index=index, **component_vars))
        self.length = self[-1].endS

    def get_component_column(self, variable):
        """Returns a list of all the component's attribute according
        to the variable provided."""
        return [getattr(component, variable) for component in self]

    def __repr__(self):
        return "<Lattice: {} components; length = {}m>".format(len(self),
                                                               self.length)


def _coerce_tvector3(tvector):
    return pyfluka.vector.Three(tvector.X(), tvector.Y(), tvector.Z())

def _coerce_trotation(trotation):
    angle = ROOT.Double()
    axis = ROOT.TVector3()
    trotation.AngleAxis(angle, axis)
    axis = _coerce_tvector3(axis)
    angle = float(angle)
    return AxisAngle(axis, angle)

def _try_coercion(var):
    try:
        return _coerce_trotation(var)
    except AttributeError:
        pass
    try:
        return _coerce_tvector3(var)
    except AttributeError:
        return var

_G4_EXCEPTION_START = (
    "-------- WWWW ------- G4Exception-START -------- WWWW -------\n")
_G4_EXCEPTION_END = (
    "-------- WWWW -------- G4Exception-END --------- WWWW -------\n")

class G4ExceptionMessage(object):
    """Given an exception message (list of lines) from G4Exception-START to
    G4-Exception-END."""


    def __init__(self, msg):
        self.exception = ""
        self.issuer = ""
        self.message = ""

        self._set_exception(msg)
        self._set_issuer(msg)
        self._set_message(msg)

    def _set_exception(self, msg):
        for line in msg:
            if line.startswith("*** G4Exception"):
                self.exception = line.split(": ")[1].strip()

        G4ExceptionMessage._only_one(msg, "*** G4Exception")

    def _set_issuer(self, msg):
        for line in msg:
            if "issued by :" in line:
                self.issuer = line.split(": ")[1].strip()
        G4ExceptionMessage._only_one(msg, "issued by :")

    def _set_message(self, msg):
        start_index = next((i
                            for i, line in enumerate(msg)
                            if "issued by :" in line)) + 1
        message = []
        for line in msg[start_index:]:
            if line == _G4_EXCEPTION_END:
                break
            message.append(line)
        else:
            raise ValueError("No G4Exception-END line found!")
        self.message = message

    @staticmethod
    def _only_one(msg, substring):
        n = len([1 for line in msg if substring in line])
        if n != 1:
            raise ValueError("Too many occurences of {}".format(substring))


def process_geometry_test(file_in, file_out=None):
    # Skip until we get to the geometry test
    seen_geom_test_run_count = 0
    with open(file_in) as f:
        for i, line in enumerate(f):
            if line.startswith("/geometry/test/run"):
                start_overlaps_line_no = i
                break

    # Read in the geometry test exceptions and append
    # G4ExceptionMessage instances to all_exceptions
    with open(file_in) as f:
        all_exceptions = []
        this_exception = []
        in_exception = False
        for line in f.readlines()[i:]:
            # Look for an exception message
            if line != _G4_EXCEPTION_START and in_exception is False:
                continue
            in_exception = True
            this_exception.append(line)
            if line == _G4_EXCEPTION_END and in_exception is True:
                all_exceptions.append(G4ExceptionMessage(this_exception))
                in_exception = False
                this_exception = []

    # Split into a dictionary of lists of instances based on issuer
    issuers = _splitter(all_exceptions, "issuer")

    return [_process_overlap_g4message(message)
            for message in issuers["G4PVPlacement::CheckOverlaps()"]]


def _splitter(iterable, attribute):
    out = dict()
    for item in iterable:
        value = getattr(item, attribute)
        if value not in out:
            out[value] = []
        out[value].append(item)

    return out

def _process_overlap_g4message(msg):
    if msg.issuer != "G4PVPlacement::CheckOverlaps()":
        raise ValueError("This exception message is not for an overlap!")
    first_vol = msg.message[1].split()[-1]
    amount = float(msg.message[3].split()[-2])
    unit = msg.message[3].split()[-1]

    if "mother volume" in msg.message[0]:
        second_vol = "mother"
        point = list(eval(msg.message[3].split()[4][:-1]))
        with_mother = True
    else:
        second_vol = msg.message[2].split()[1]
        point = list(eval(msg.message[3].split()[2][:-1]))
        with_mother = False

    OverlapInfo = collections.namedtuple(
        "OverlapInfo", ["first", "second", "point",
                        "amount", "unit", "with_mother"])
    return OverlapInfo(first_vol, second_vol, point, amount, unit, with_mother)
