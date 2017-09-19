"""Useful functions and classes to ease the use of pyfluka with BDSIM."""

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

def get_bdsim_placement(bdsim_point, fluka_point,
                        fluka_bounding_box_origin, axis, angle):
    """Return the placement that aligns fluka_point with bdsim_point in
    the BDSIM global coordinate system.  Units in mm

    Arguments:
    bdsim_point -- a point in the BDSIM world.
    fluka_point -- a coordinate in the FLUKA coordinate system.
    fluka_bounding_box_origin -- the centre of the bounding box in FLUKA-world.
    axis -- the axis part of the axis-angle rotation for the bounding box.
    angle -- the angle part of the axis-angle rotation for the bounding box.
    """
    rotation_matrix = pygdml.transformation.axisangle2matrix(axis, angle)
    # converts a point in the fluka coordinate system to its point in
    # the bdsim global coordinate system.
    fluka_point_in_bdsim = fluka_point - fluka_bounding_box_origin
    rotated_point = rotation_matrix.dot(fluka_point_in_bdsim).A1
    offset = bdsim_point - rotated_point
    return offset

def get_placement_string(name, filepath, offset, axis, angle):
    """All units should be in metres..."""
    out = ("{name}: placement,"
           " x = {offset.x}*m, y = {offset.y}*m, z = {offset.z}*m,"
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

class Component(collections.namedtuple("Component",
                                       _COMPONENT_VARS | {"index"})):
    # Default repr would be too big so redefine to something
    # human-readable and useful:
    def __repr__(self):
        return "<{}: {}, S={}m ...>".format(self.componentName,
                                            self.componentType,
                                            self.staS)

class Lattice(object):
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
        self.components = []
        for index, _ in enumerate(model.componentName):
            component_vars = {variable:
                              _try_coercion(getattr(model, variable)[index])
                              for variable in _COMPONENT_VARS}
            self.components.append(Component(index=index, **component_vars))

    def get_component_column(self, variable):
        """Returns a list of all the component's attribute according
        to the variable provided."""
        return [getattr(component, variable) for component in self.components]
