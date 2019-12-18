import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import PLA, Region, Zone, FlukaRegistry
import pyg4ometry.fluka.body

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    pyg4ometry.fluka.body.INFINITY = 30

    pla1 = PLA("PLA1_BODY",
               [1, 1, 1],
               [20, 20.0, 20],
               translation=[-20, -20, -20],
               flukaregistry=freg)

    z1 = Zone()

    z1.addIntersection(pla1)

    region = Region("REG_INF")
    region.addZone(z1)

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