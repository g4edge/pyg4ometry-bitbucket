import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import TRC
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # big face (r=5) is at the origin, smaller face (r=2) is at [5, 5, 5].
    trc = TRC("TRC_BODY", [0, 0, 0], [5, 5, 5], 5, 2, flukaregistry=freg)
    # big face (r=5) is at the [4, 4, 4]    , smaller face (r=2) is at
    # [9, 9, 9].
    trc2 = TRC("TRC2_BODY", [4, 4, 4], [5, 5, 5], 5, 2, flukaregistry=freg)

    z = Zone()
    z2 = Zone()
    z.addIntersection(trc)
    z2.addIntersection(trc2)

    region = Region("TRC_REG")
    region.addZone(z)
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