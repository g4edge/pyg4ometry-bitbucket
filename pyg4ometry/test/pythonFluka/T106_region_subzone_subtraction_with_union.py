import pyg4ometry.convert as convert
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP, ZCC

from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi

# This is same as T105_REGION_SUBZONE_SUBTRACTION.py but with a union
# as well.

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    rpp = RPP("RPP_BODY1", -20, 20, -20, 20, -20, 20, flukaregistry=freg)
    rppsub = RPP("RPP2_BODY2", -10, 10, -10, 10, -30, 30, flukaregistry=freg)

    rppunion = RPP("RPP_BODY3", 0, 20, -20, 20, -20, 20, flukaregistry=freg)

    zcc = ZCC("ZCC_BODY", 0, 0, 10, flukaregistry=freg)

    # +rpp -(+rppsub -zcc) | +rpp3

    z = Zone()
    z.addIntersection(rpp)

    z2 = Zone()
    z2.addIntersection(rppsub)
    z2.addSubtraction(zcc)

    # Adding zone2 as a subtraction to the first zone.
    z.addSubtraction(z2)


    z3 = Zone()
    z3.addIntersection(rppunion)

    region = Region("RPP_REG")

    region.addZone(z)
    region.addZone(z3)

    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)


    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True,True)
