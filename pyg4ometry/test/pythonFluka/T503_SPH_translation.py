import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import SPH, Region, Zone, FlukaRegistry

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    sph = SPH("SPH_BODY",
              [20, 20, 20], 20,
              translation=[-20, -20, -20],
              flukaregistry=freg)
    z = Zone()
    z.addIntersection(sph)
    region = Region("SPH_REG")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
