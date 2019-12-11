import pyg4ometry.convert as convert
import os

import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP, RCC
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()
    # I pick 20 because that's the length of the axes added below, so
    # verifying the resulting cube is of the correct length is trivial.
    rpp = RPP("RPP_BODY", 0, 20., 0, 20., 0., 20., flukaregistry=freg)
    rcc = RCC("RCC_BODY", [0., 0., 20.], [0., 20., 0.], 10., flukaregistry=freg)

    # RPP is used in the definitions of both zone1 and zone2.

    z1 = Zone()
    z1.addIntersection(rpp)
    z2 = Zone()
    z2.addIntersection(rcc)
    z2.addSubtraction(rpp)


    region = Region("REG_INF")
    region.addZone(z1)
    region.addZone(z2)

    freg.addRegion(region)
    greg = convert.fluka2Geant4(freg)

    # Test extents??
    # clip wv?
    # test writing back to fluka?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    w = gdml.Writer()
    w.addDetector(greg)
    gdml_name = "REUSE.gdml"
    gmad_name = "REUSE.gmad"
    w.write(os.path.join(os.path.dirname(__file__), gdml_name))
    w.writeGmadTester(gmad_name, gdml_name)
        
    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
