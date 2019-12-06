import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import ZCC, XYP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()
    # I pick 20 because that's the length of the axes added below, so
    # verifying the resulting body is of the correct length and radius
    # is trivial.
    zcc1 = ZCC("ZCC_BODY1", 0, 0, 20, flukaregistry=freg)
    zcc2 = ZCC("ZCC_BODY2", 0, 0, 10, flukaregistry=freg)

    xyp1 = XYP("XYP1_BODY", 20, flukaregistry=freg)
    xyp2 = XYP("XYP2_BODY", 0, flukaregistry=freg)

    xyp3 = XYP("XYP3_BODY", 15, flukaregistry=freg)
    xyp4 = XYP("XYP4_BODY", 5, flukaregistry=freg)

    z1 = Zone()
    z1.addIntersection(zcc1)
    z1.addIntersection(xyp1)
    z1.addSubtraction(xyp2)

    z2 = Zone()
    z2.addIntersection(zcc2)
    z2.addIntersection(xyp3)
    z2.addSubtraction(xyp4)

    z1.addSubtraction(z2)

    region1 = Region("REG_INF1")
    region2 = Region("REG_INF2")
    region1.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)

    greg = freg.toG4Registry(True, False)

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
