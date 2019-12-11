import pyg4ometry.convert as convert
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    rpp1 = RPP("RPP_BODY1", 0, 10, 0, 10, 0, 10, flukaregistry=freg)
    rpp2 = RPP("RPP_BODY2", 2, 8, 2, 8, 2, 8, flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(rpp1)
    z1.addSubtraction(rpp2)

    z2.addIntersection(rpp2)

    region1 = Region("RPP_REG1")
    region2 = Region("RPP_REG2")

    region1.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)

    greg = convert.fluka2Geant4(freg, with_length_safety=True)


    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wlv)
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
