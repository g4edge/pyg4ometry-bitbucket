import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    rpp = RPP("RPP_BODY", -5, 5, -5, 5, -5, 5, flukaregistry=freg)
    z = Zone()
    z.addIntersection(rpp)
    region = Region("RPP_REG")
    region.addZone(z)
    freg.addRegion(region)

    greg = freg.toG4Registry()

    # from IPython import embed; embed()

    # Test extents??
    # clip wv?
    
    if vis:
        v = vi.VtkViewer()
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}
        


if __name__ == '__main__':
    Test()

    


    