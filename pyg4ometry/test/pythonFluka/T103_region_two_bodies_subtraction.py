import pyg4ometry.convert as convert
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP

from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    rpp1 = RPP("RPP_BODY1", 0, 10, 0, 10, 0, 10, flukaregistry=freg)
    rpp2 = RPP("RPP_BODY2", 5, 15, 0, 10, 0, 10, flukaregistry=freg)

    z = Zone()
    z.addIntersection(rpp1)
    z.addSubtraction(rpp2)
    region = Region("RPP_REG")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

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
