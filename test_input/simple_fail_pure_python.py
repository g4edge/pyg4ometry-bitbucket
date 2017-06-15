import pygdml
from math import pi
import numpy as np


cylinder_scale = 1e10
box_scale = 1e4

w = pygdml.solid.Box("world", 1e6, 1e6, 1e6)
wv = pygdml.Volume([0,0,0], [0,0,0], w, "world-volume",
                              None, 1, False, "G4_Galatic")

cylinder = pygdml.solid.Tubs("cylinder",
                        0.0,
                        7250.0,
                        cylinder_scale * 0.5,
                        0.0,
                        2*pi)

box_1 = pygdml.Box("box_1", 0.5 * box_scale, 0.5 * box_scale, 0.5 * box_scale)
box_2 = pygdml.Box("box_2", 0.5 * box_scale, 0.5 * box_scale, 0.5 * box_scale)
cylinder = pygdml.Tubs("cylinder", 0.0, 7250., 0.5 * cylinder_scale, 0.0, 2*pi)

box_1_y = -1100.
box_2_y = -3850.
box_1_centre_y = box_1_y - 0.5 * box_scale
box_2_centre_y = box_2_y - 0.5 * box_scale
offset = box_2_centre_y - box_1_centre_y
print offset
box_1_minus_box_2 = pygdml.Subtraction("box_1_minus_box_2", box_1, box_2,
                                   [[0,0,0], [0, offset, 0]])

box_1_minus_box_2_translation = [0, box_1_y - 0.5 * box_scale, 0]
box_1_minus_box_2_rotation = [0, 0, 0]
cylinder_translation = np.array([-4100, 50, 0])
cylinder_rotation = np.array([0, 0, 0.5 * pi])

sub_trans = box_1_minus_box_2_translation - cylinder_translation
sub_rot   = box_1_minus_box_2_rotation - cylinder_rotation

cylinder_intersect_sheet = pygdml.Intersection("cylinder_intersect_sheet",
                                          cylinder, box_1_minus_box_2,
                                          [sub_rot,sub_trans])


out_volume = pygdml.Volume([0,0,0], [0., 0., 0.0],
                           cylinder_intersect_sheet,
                           "cylinder_intersect_sheet_vol", wv, 1,
                           False, "asdasd")


# out_volume = pygdml.Volume([0,0,0], [0., 0., 0.0],
#                            box_1_minus_box_2, "box_1_minus_box_2_vol", wv, 1,
#                            False, "asdasd")

# just_cylinder_volume = pygdml.Volume([0,0,0], [0., 100., 0.0],
#                            cylinder, "cylinder_vol", wv, 1,
#                            False, "asdasd")



m = wv.pycsgmesh()
v = pygdml.VtkViewer()
v.addSource(m)
# wv.setClip()
# embed()
v.view()
