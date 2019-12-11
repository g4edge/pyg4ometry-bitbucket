import pyg4ometry.convert as convert
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import XCC, YZP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()
    # I pick 20 because that's the length of the axes added below, so
    # verifying the resulting body is of the correct length and radius
    # is trivial.
    xcc1 = XCC("XCC_BODY1", 0, 0, 20, flukaregistry=freg)
    xcc2 = XCC("XCC_BODY2", 0, 0, 10, flukaregistry=freg)

    yzp1 = YZP("YZP1_BODY", 20, flukaregistry=freg)
    yzp2 = YZP("YZP2_BODY", 0, flukaregistry=freg)

    yzp3 = YZP("YZP3_BODY", 15, flukaregistry=freg)
    yzp4 = YZP("YZP4_BODY", 5, flukaregistry=freg)

    z1 = Zone()
    z1.addIntersection(xcc1)
    z1.addIntersection(yzp1)
    z1.addSubtraction(yzp2)

    z2 = Zone()
    z2.addIntersection(xcc2)
    z2.addIntersection(yzp3)
    z2.addSubtraction(yzp4)

    z1.addSubtraction(z2)

    region1 = Region("REG_INF1")
    region2 = Region("REG_INF2")
    region1.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)

    greg = convert.fluka2Geant4(freg, True, False)

    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    # Test extents??
    # clip wv?
    # test writing back to fluka?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wlv)
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
