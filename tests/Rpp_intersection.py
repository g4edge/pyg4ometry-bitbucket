import pygdml
from IPython import embed

box = pygdml.Box("abox", 10, 10, 10)
sphere = pygdml.Orb("asph", 10)

w = pygdml.solid.Box("world", 10000, 10000, 10000)
wv = pygdml.Volume([0,0,0], [0,0,0], w, "world-volume", None, 1,
                   False, "cu")

# intersection = pygdml.Intersection("oint", box, sphere, [[0,0,0], [10.0,0,0]])

boxvol = pygdml.Volume([0,0,0], [0,0,-20], box, "box-volume", wv, 1, False, "cu")
# sphvol = pygdml.Volume([0,0,0], [0,0,0], sphere, "sph-volume", wv,
# 1, False, "cu")
# intvol = pygdml.Volume([0,0,0], [0,0,0], intersection, "int-volume", wv, 1, False, "cu")

m = wv.pycsgmesh()
v = pygdml.VtkViewer()
v.addSource(m)
wv.setClip()
# embed()
v.view()
