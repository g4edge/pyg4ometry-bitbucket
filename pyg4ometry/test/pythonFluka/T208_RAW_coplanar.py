import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RAW
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka.Vector import Three
import numpy as np

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    # What I expect to see in the visualiser is a cube formed by the
    # union of two wedeges. with sides equal to 20cm.  The mesh shows
    # the two wedges.

    raw1 = RAW("RAW1_BODY",
              [0, 0, 0], # vertex position
              [20, 0, 0], # one transverse side.
              [0, 0, 20], # length vector.
              [0, 20, 0], # the other transverse side.
              flukaregistry=freg)

    raw2 = RAW("RAW2_BODY",
               [5, 5, 5], # vertex position
               [5, 0, 0], # one transverse side.
               [0, 0, 5], # length vector.
               [0, 5, 0], # the other transverse side.
               flukaregistry=freg)

    z1 = Zone()
    z1.addIntersection(raw1)
    z1.addSubtraction(raw2)

    z2 = Zone()
    z2.addIntersection(raw2)

    region1 = Region("RAW_REG1")
    region1.addZone(z1)

    region2 = Region("RAW_REG2")
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)

    greg = freg.toG4Registry(with_length_safety=False,
                             split_disjoint_unions=False)

    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(wlv)
        v.setRandomColours()
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
