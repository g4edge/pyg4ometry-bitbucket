import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import WED
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka.Vector import Three
import numpy as np

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # What I expect to see in the visualiser is a cube formed by the
    # union of two wedeges. with sides equal to 20cm.  The mesh shows
    # the two wedges.

    wed1 = WED("WED1_BODY",
              [20, 20, 20], # vertex position
              [-20, 0, 0], # one transverse side.
              [0, 0, -20], # length vector.
              [0, -20, 0], # the other transverse side.
              freg)

    wed2 = WED("WED2_BODY",
               [0, 0, 0],
               [20, 0, 0], # one transverse side.
               [0, 0, 20], # length vector.
               [0, 20, 0], # the other transverse side.
               freg)

    
    z1 = Zone()
    z1.addIntersection(wed1)

    z2 = Zone()
    z2.addIntersection(wed2)

    region = Region("WED_REG")
    region.addZone(z1)
    region.addZone(z2)
    freg.addRegion(region)

    greg = freg.toG4Registry()


    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
