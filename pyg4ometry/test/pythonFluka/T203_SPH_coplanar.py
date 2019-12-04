import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import SPH
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    sph1 = SPH("SPH_BODY1", [0, 0, 0], 10, flukaregistry=freg)
    sph2 = SPH("SPH_BODY2", [0, 0, 0], 5, flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(sph1)
    z1.addSubtraction(sph2)

    z2.addIntersection(sph2)

    region1 = Region("SPH_REG1")
    region2 = Region("SPH_REG2")

    region1.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)

    greg = freg.toG4Registry(with_length_safety=True)


    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    # Test extents??
    # clip wv?


    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(wlv)
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
