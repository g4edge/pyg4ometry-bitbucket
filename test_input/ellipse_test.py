import pygdml
from math import pi
# Define world volume:
w = pygdml.solid.Box("world", 10000, 10000, 10000)
world_volume = pygdml.Volume([0,0,0], [0,0,0], w,
                             "world-volume", None, 1, False, "G4_NITROUS_OXIDE")

my_solid = pygdml.solid.EllipticalTube("ellip", 10.0, 20.0, 100.0)

my_solid_placement = [0,0,0]
my_solid_rotation = [0,0,0]
my_solid = pygdml.Volume(my_solid_rotation,
                         my_solid_placement,
                         my_solid,
                         "my_solid_volume",
                         world_volume, 1, False, "G4_NITROUS_OXIDE")


world_volume.setClip()
mesh = world_volume.pycsgmesh()
viewer = pygdml.VtkViewer()
viewer.addSource(mesh)
viewer.view()
