import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import RPP, Region, Zone, FlukaRegistry, Transform


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    expansion = 2

    rpp = RPP("RPP_BODY", 0, 10, 0, 10, 0, 10, flukaregistry=freg,
              expansion=expansion)
    z = Zone()
    z.addIntersection(rpp)
    region = Region("RPP_REG", material="COPPER")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer": v}

if __name__ == '__main__':
    Test(True, True)
