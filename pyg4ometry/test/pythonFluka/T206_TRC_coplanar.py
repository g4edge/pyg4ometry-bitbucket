import pyg4ometry.convert as convert
import os
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import TRC
from pyg4ometry.fluka.Region import Region, Zone
from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()
    greg = g4.Registry()

    # trivially coplanar:
    trc1 = TRC("TRC_BODY1", [0, 0, 0], [5, 5, 5], 5, 2, flukaregistry=freg)
    trc2 = TRC("TRC_BODY2", [10, 10, 10], [-5, -5, -5], 5, 2, flukaregistry=freg)
    trc3 = TRC("TRC_BODY3", [10, 10, 10], [5, 5, 5], 5, 2, flukaregistry=freg)

    z1 = Zone()
    z2 = Zone()
    z3 = Zone()

    z1.addIntersection(trc1)
    z2.addIntersection(trc2)
    z3.addIntersection(trc3)

    region1 = Region("TRC_REG1")
    region2 = Region("TRC_REG2")
    region3 = Region("TRC_REG3")

    region1.addZone(z1)
    region2.addZone(z2)
    region3.addZone(z3)

    freg.addRegion(region1)
    freg.addRegion(region2)
    freg.addRegion(region3)


    # default is True, but to be explicit:
    greg = convert.fluka2Geant4(freg,
                                with_length_safety=True,
                                split_disjoint_unions=False)

    wv = greg.getWorldVolume()
    wv.checkOverlaps()

    # Test extents??
    # clip wv?

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wv)
        v.view(interactive=interactive)


    # gdml output
    w = gdml.Writer()
    w.addDetector(greg)
    this_file_name = __file__
    gmad_name = this_file_name.rstrip(".py") + ".gmad"
    gdml_name = this_file_name.rstrip(".py") + ".gdml"
    w.write(os.path.join(os.path.dirname(__file__), gdml_name))
    w.writeGmadTester(os.path.join(os.path.dirname(__file__))+gmad_name,
                      gdml_name)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)
