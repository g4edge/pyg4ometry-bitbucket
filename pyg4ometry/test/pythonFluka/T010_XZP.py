import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import YZP
import pyg4ometry.fluka.Body
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()
    pyg4ometry.fluka.Body.INFINITY = 30
    xzp = XZP("XZP_BODY", 20.0, flukaregistry=freg)

    z = Zone()
    z.addIntersection(xzp)

    region = Region("REG_INF")
    region.addZone(z)

    freg.addRegion(region)

    greg = freg.toG4Registry()


    # Test extents??
    # clip wv?
    # test writing back to fluka?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
