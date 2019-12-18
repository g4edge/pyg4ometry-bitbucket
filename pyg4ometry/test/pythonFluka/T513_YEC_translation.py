import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import YEC, XZP, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    yec = YEC("YEC_BODY",
              20, 20, 20, 10,
              translation=[-20, -20, -20],
              flukaregistry=freg)

    xzp_hi = XZP("XZP1_BODY", 20, flukaregistry=freg)
    xzp_lo = XZP("XZP2_BODY", 0, flukaregistry=freg)

    z = Zone()

    z.addIntersection(yec)
    z.addIntersection(xzp_hi)
    z.addSubtraction(xzp_lo)


    region = Region("REG_INF")
    region.addZone(z)

    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)