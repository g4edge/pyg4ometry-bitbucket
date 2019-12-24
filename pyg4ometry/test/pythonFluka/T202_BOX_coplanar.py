import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import BOX, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    # trivially coplanar:
    box1 = BOX("BOX1_BODY",
               [0, 0, 0],
               [0, 0, 10],
               [0, 10, 0],
               [10, 0, 0],
               flukaregistry=freg)

    box2 = BOX("BOX2_BODY",
               [2, 2, 2],
               [0, 0, 6],
               [0, 6, 0],
               [6, 0, 0],
               flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(box1)
    z1.addSubtraction(box2)
    z2.addIntersection(box2)

    region1 = Region("BOX_REG1", material="COPPER")
    region2 = Region("BOX_REG2", material="COPPER")

    region1.addZone(z1)
    region2.addZone(z2)

    freg.addRegion(region1)
    freg.addRegion(region2)

    # default is True, but to be explicit:
    greg = convert.fluka2Geant4(freg,
                                with_length_safety=True,
                                split_disjoint_unions=False)

    wv = greg.getWorldVolume()
    wv.checkOverlaps()

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wv)
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}

if __name__ == '__main__':
    Test(True, True)
