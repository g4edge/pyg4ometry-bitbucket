import os
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import BOX
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # trivially coplanar:
    box1 = BOX("BOX1_BODY",
               [0, 0, 0],
               [0, 0, 10],
               [0, 10, 0],
               [10, 0, 0],
               flukaregistry=freg)

    box2 = BOX("BOX2_BODY",
               [10, 0, 0],
               [0, 0, 10],
               [0, 10, 0],
               [10, 0, 0],
               flukaregistry=freg)

    box3 = BOX("BOX3_BODY",
               [-10, 0, 0],
               [0, 0, 10],
               [0, 10, 0],
               [10, 0, 0],
               flukaregistry=freg)


    box4 = BOX("BOX4_BODY",
               [0, 10, 0],
               [0, 0, 10],
               [0, 10, 0],
               [10, 0, 0],
               flukaregistry=freg)

    box5 = BOX("BOX5_BODY",
               [0, -10, 0],
               [0, 0, 10],
               [0, 10, 0],
               [10, 0, 0],
               flukaregistry=freg)
    

    z1 = Zone()
    z2 = Zone()
    z3 = Zone()
    z4 = Zone()
    z5 = Zone()

    z1.addIntersection(box1)
    z2.addIntersection(box2)
    z3.addIntersection(box3)
    z4.addIntersection(box4)
    z5.addIntersection(box5)

    region1 = Region("BOX_REG1")
    region2 = Region("BOX_REG2")
    region3 = Region("BOX_REG3")
    region4 = Region("BOX_REG4")
    region5 = Region("BOX_REG5")

    region1.addZone(z1)
    region2.addZone(z2)
    region3.addZone(z3)
    region4.addZone(z4)
    region5.addZone(z5)

    freg.addRegion(region1)
    freg.addRegion(region2)
    freg.addRegion(region3)
    freg.addRegion(region4)
    freg.addRegion(region5)

    # default is True, but to be explicit:
    greg = freg.toG4Registry(with_length_safety=True,
                             split_disjoint_unions=False)

    wv = greg.getWorldVolume()
    wv.checkOverlaps()

    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wv)
        v.view(interactive=interactive)


    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
