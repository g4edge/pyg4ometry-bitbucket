import pyg4ometry.convert as convert
import numpy as np
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import ELL

from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka.Vector import Three


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # construct an ellipsoid with the one of the ends of the
    # semi-major axis at the origin, and stretching in the i+j+k direction.
    focus1 = Three([3, 3, 3])
    focus2 = 8*focus1
    linear_eccentricity = 0.5*(focus2 - focus1).length()
    focus1_length = focus1.length()

    length = (linear_eccentricity + focus1_length) * 2

    ell = ELL("ELL_BODY",
              focus1,
              focus2,
              length,
              flukaregistry=freg)

    z = Zone()
    z.addIntersection(ell)
    region = Region("ELL_REG")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)


    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes()
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
