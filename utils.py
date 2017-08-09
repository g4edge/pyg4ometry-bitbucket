"""Useful functions."""

import pygdml.transformation

def get_bdsim_placement(bdsim_point, fluka_point,
                        fluka_bounding_box_origin, axis, angle):
    """Return the placement that aligns fluka_point with bdsim_point in
    the BDSIM global coordinate system.

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
    rotated_point = rotation_matrix.dot(fluka_point_in_bdsim)
    offset = bdsim_point - rotated_point
    return offset
