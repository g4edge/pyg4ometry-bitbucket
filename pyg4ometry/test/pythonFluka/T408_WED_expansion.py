import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import WED, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    wed = WED("WED_BODY",
              [5, 0, 0], # vertex position
              [5, 0, 0], # one transverse side.
              [0, 0, 10], # length vector.
              [0, 10, 0], # the other transverse side.
              expansion=2.0,
              flukaregistry=freg)

    z = Zone()
    z.addIntersection(wed)

    region = Region("WED_REG", material="COPPER")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer": v}

if __name__ == '__main__':
    Test(True, True)
