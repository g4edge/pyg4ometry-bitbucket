import numpy as np

import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import REC, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    face = [0, 0, 0]
    direction = [0, 0, 10]
    semiminor = [10, 0, 0]
    semimajor = [0, 5, 0]

    rec = REC("REC_BODY",
              face,
              direction,
              semiminor,
              semimajor,
              expansion=2.0,
              flukaregistry=freg)

    z = Zone()
    z.addIntersection(rec)
    region = Region("REC_REG", material="COPPER")
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
