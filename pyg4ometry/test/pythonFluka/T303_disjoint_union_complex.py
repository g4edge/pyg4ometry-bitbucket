import pyg4ometry.convert as convert
import os
import pyg4ometry.geant4 as g4
from pyg4ometry.fluka.Body import RPP, RCC

from pyg4ometry.fluka.FlukaRegistry import FlukaRegistry
import pyg4ometry.visualisation as vi
import pyg4ometry.gdml as gdml


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    # 1 overlaps with 2
    # 2 overlaps with 1 and 3
    # 3 overlaps with 2 and 4
    # 4 overlaps with 3
    # All 4 nodes are connected.
    # multipl each one by 100
    rpp1 = RPP("RPP1", -25, 25, -25, 25, 0.0, 100, flukaregistry=freg)
    rpp2 = RPP("RPP2", -50, 50, -50, 50, 50, 150, flukaregistry=freg)

    rpp3 = RPP("RPP3", -75, 75, -75, 75, 125, 225, flukaregistry=freg)
    rpp4 = RPP("RPP4", -100, 100, -100, 100, 200, 300, flukaregistry=freg)
    # These two are connected but not with the previous other 4
    rpp5 = RPP("RPP5", -125, 125, -125, 125, 500, 600, flukaregistry=freg)
    rpp6 = RPP("RPP6", -150, 150, -150, 150, 550, 650, flukaregistry=freg)
    # This one is connected to no other bodies in the union
    rpp7 = RPP("RPP7", -175, 175, -175, 175, 800, 900, flukaregistry=freg)

    # region 	   5 | +RPP1 | +RPP2 | +RPP3 | +RPP4 | +RPP5 | +RPP6 | +RPP7
    z1 = Zone(name="connected_part_1")
    z1.addIntersection(rpp1)
    z2 = Zone(name="connected_part_2")
    z2.addIntersection(rpp2)

    z3 = Zone(name="connected_part_3")
    z3.addIntersection(rpp3)
    z4 = Zone(name="connected_part_4")
    z4.addIntersection(rpp4)
    z5 = Zone(name="connected_part_5")
    z5.addIntersection(rpp5)
    z6 = Zone(name="connected_part_6")
    z6.addIntersection(rpp6)
    z7 = Zone(name="connected_part_7")
    z7.addIntersection(rpp7)

    region = Region("REGION")
    region.addZone(z1)
    region.addZone(z2)
    region.addZone(z3)
    region.addZone(z4)
    region.addZone(z5)
    region.addZone(z6)
    region.addZone(z7)

    # region._determine_connected_zones()

    freg.addRegion(region)



    greg = convert.fluka2Geant4(freg)

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
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



if __name__ == '__main__':
    Test(True, True)
