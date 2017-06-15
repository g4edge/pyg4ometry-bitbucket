import pyfluka
from IPython import embed
import cPickle
from collections import Counter
a = pyfluka.model.Model("lhc-tunnel/ir1-just-geo.inp")

with open("lhc-tunnel/ir1-just-geo.inp_diag.pickle") as f:
    o = cPickle.load(f)

working_region_solids = []
not_working_region_solids = []
for region in o['good_regions']:
    for solid in a.regions[region].atomic_solids():
        solid_type = type(a.bodies[solid]).__name__
        working_region_solids.append(solid_type)

for region in o['bad_regions']:
    for solid in a.regions[region].atomic_solids():
        solid_type = type(a.bodies[solid]).__name__
        not_working_region_solids.append(solid_type)
good_count = Counter(working_region_solids)
bad_count = Counter(not_working_region_solids)


def proportion_not_working(solid_type):
    working = float(good_count[solid_type])/len(working_region_solids)
    not_working = float(bad_count[solid_type])/len(not_working_region_solids)
    ratio = not_working/working
    print "notworking2working %s: %s" % (solid_type, ratio)


for solid_type in set(working_region_solids + not_working_region_solids):
    proportion_not_working(solid_type)
