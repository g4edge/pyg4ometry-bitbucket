import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import RPP, RCC, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    rpp = RPP("RPP_BODY", -10, 10, -10, 0, -10, 10, flukaregistry=freg)
    rcc = RCC("RCC_BODY", [0, -10, 0], [0.0, 10, 0.0], 10, flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(rpp)
    z2.addIntersection(rcc)

    region = Region("REG", material="COPPER")
    region.addZone(z1)
    region.addZone(z2)

    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg, splitDisjointUnions=True)

    assert len(greg.logicalVolumeList) == 2

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        # should appear as different colours if  split properly
        v.setRandomColours()
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer": v}

if __name__ == '__main__':
    Test(True, True)
