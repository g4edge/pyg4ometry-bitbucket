import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import XCC, YZP, Region, Zone, FlukaRegistry
from pyg4ometry.fluka.body import INFINITY

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    # I pick 20 because that's the length of the axes added below, so
    # verifying the resulting body is of the correct length and radius
    # is trivial.
    xcc = XCC("XCC_BODY", 0, 0, 20, flukaregistry=freg)

    yzp_hi = YZP("YZP1_BODY", 20, flukaregistry=freg)
    yzp_lo = YZP("YZP2_BODY", 0, flukaregistry=freg)

    z = Zone()

    z.addIntersection(xcc)
    z.addIntersection(yzp_hi)
    z.addSubtraction(yzp_lo)


    region = Region("REG_INF")
    region.addZone(z)

    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg,
                                with_length_safety=True,
                                split_disjoint_unions=False,
                                minimise_solids=True)
    print "Infinite cylinder length =", greg.solidDict["XCC_BODY_s"].pDz
    assert greg.solidDict["XCC_BODY_s"].pDz < INFINITY

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}

if __name__ == '__main__':
    Test(True, True)
