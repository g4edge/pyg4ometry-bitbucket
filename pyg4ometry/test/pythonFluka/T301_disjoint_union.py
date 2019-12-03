import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    rpp1 = RPP("RPP_BODY1", 0, 5, 0, 5, 0, 5, flukaregistry=freg)
    rpp2 = RPP("RPP_BODY2", 10, 15, 10, 15, 10, 15, flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(rpp1)
    z2.addIntersection(rpp2)

    region = Region("RPP_REG")
    region.addZone(z1)
    region.addZone(z2)

    cz = region.get_connected_zones()

    freg.addRegion(region)

    greg = freg.toG4Registry()

    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
