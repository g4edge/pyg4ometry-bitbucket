import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import RPP, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    rpp1 = RPP("RPP_BODY1", 0, 20, 0, 20, 0, 20, flukaregistry=freg)
    rpp2 = RPP("RPP_BODY2", 5, 15, 5, 15, 5, 15, flukaregistry=freg)
    rpp3 = RPP("RPP_BODY3", 7.5, 12.5, 7.5, 12.5, 7.5, 12., flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()

    z1.addIntersection(rpp1)
    z1.addSubtraction(rpp2)
    z2.addIntersection(rpp3)

    region = Region("RPP_REG", material="COPPER")
    region.addZone(z1)
    region.addZone(z2)

    cz = region.get_connected_zones()
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    assert len(greg.logicalVolumeList) == 3

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
