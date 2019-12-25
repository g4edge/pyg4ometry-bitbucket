import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import ELL, Region, Zone, FlukaRegistry, Three


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    # ellipsoid with major axes poining in the y direction, total
    # legnth=20, offset in x.
    focus1 = Three([20, 5, 0])
    focus2 = Three([20, 15, 0])
    length = 20

    ell = ELL("ELL_BODY",
              focus1,
              focus2,
              length,
              flukaregistry=freg)

    z = Zone()
    z.addIntersection(ell)
    region = Region("ELL_REG", material="COPPER")
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
