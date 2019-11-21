import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import SPH, PLA
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # sphere at origin with radius 10
    sph = SPH("SPH_BODY", [0, 0, 0], 10, flukaregistry=freg)
    # point is at [5, 5, 5]
    # facing in the -1, -1, -1 direction
    pla = PLA("PLA_BODY", [-1, -1, -1], [0, 0, 0], flukaregistry=freg)

    z = Zone()
    z2 = Zone()
    z.addIntersection(sph)
    # z2.addIntersection(pla)
    z.addSubtraction(pla)
    region = Region("SPH_REG")
    region.addZone(z)
    # region.addZone(z2)
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
