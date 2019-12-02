import os
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # trivially coplanar:
    rpp1 = RPP("RPP1_BODY", 0, 10, 0, 10, 0, 10, flukaregistry=freg)
    rpp2 = RPP("RPP2_BODY", 10, 20, 0, 10, 0, 10, flukaregistry=freg)    

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(rpp1)
    z2.addIntersection(rpp2)    

    region1 = Region("RPP_REG1")
    region2 = Region("RPP_REG2")    

    region1.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)    

    
    # default is True, but to be explicit:
    greg = freg.toG4Registry(with_length_safety=True) 

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

    


    
