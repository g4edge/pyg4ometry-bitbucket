import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import BOX, Region, Zone, FlukaRegistry

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    # box with corner at the origin and sides of length 20 extending
    # along the axes
    box = BOX("BOX_BODY",
              [20, 20, 20],
              [20, 0, 0],
              [0, 20, 0],
              [0, 0, 20],
              translation=[-20, -20, -20],
              flukaregistry=freg)
    z = Zone()
    z.addIntersection(box)
    region = Region("BOX_REG")
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
