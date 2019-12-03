import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RCC
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    rcc1 = RCC("RCC1_BODY", [0, 0, 0], [5, 5, 5], 2.5, flukaregistry=freg)
    rcc2 = RCC("RCC2_BODY", [-1, -1, -1], [6, 6, 6], 1.25, flukaregistry=freg)

    z = Zone()

    z.addIntersection(rcc1)
    z.addSubtraction(rcc2)    
    region = Region("RCC_REG")
    region.addZone(z)
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

    


    
