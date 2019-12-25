import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import XZP, Region, Zone, FlukaRegistry
import pyg4ometry.fluka.body

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    pyg4ometry.fluka.body.INFINITY = 30

    xzp = XZP("XZP_BODY", 20.0, flukaregistry=freg)

    z = Zone()
    z.addIntersection(xzp)

    region = Region("REG_INF", material="COPPER")
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
