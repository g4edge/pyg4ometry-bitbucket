import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import ARB, Region, Zone, FlukaRegistry, Three, Transform


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    vertices = [[0, 0, 0],
                [20, 0, 0],
                [10, 20, 0],
                [0, 20, 0],
                [0, 0, 20],
                [20, 0, 20],
                [10, 20, 20],
                [0, 20, 20]]
    facenumbers = [4321, 5678, 2376, 1584, 3487, 1265]

    arb = ARB("ARB_BODY", vertices, facenumbers, flukaregistry=freg)

    trans = Transform(expansion=0.5,
                      translation=[5, 5, 5])

    arbInner = ARB("ARB_BODY2", vertices, facenumbers, transform=trans)

    z1 = Zone()
    z1.addIntersection(arb)
    z1.addSubtraction(arbInner)

    z2 = Zone()
    z2.addIntersection(arbInner)

    region = Region("ARB_REG", material="COPPER")
    region2 = Region("ARB_REG2", material="COPPER")

    region.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region)
    freg.addRegion(region2)

    greg = convert.fluka2Geant4(freg)
    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer": v}

if __name__ == '__main__':
    Test(True, True)
