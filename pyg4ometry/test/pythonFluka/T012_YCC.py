import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import YCC, XZP
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()
    # I pick 20 because that's the length of the axes added below, so
    # verifying the resulting body is of the correct length and radius
    # is trivial.
    ycc = YCC("YCC_BODY", 0, 0, 20, flukaregistry=freg)

    xzp_hi = XZP("XZP1_BODY", 20, flukaregistry=freg)
    xzp_lo = XZP("XZP2_BODY", 0, flukaregistry=freg)



    z = Zone()

    z.addIntersection(ycc)
    z.addIntersection(xzp_hi)
    z.addSubtraction(xzp_lo)


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
