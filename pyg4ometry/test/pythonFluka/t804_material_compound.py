import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import (RPP, Region,
                              Zone, FlukaRegistry,
                              Element, Compound)

def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    fr = Element("FRANCIUM", 87, 2.48, flukaregistry=freg)
    es = Element("EINSTEIN", 99, 8.84, flukaregistry=freg)

    fr2es3 = Compound("Fr2Es3", 7.5, [(fr, 2.0), (es, 3.0)],
                      fractionType="atomic", flukaregistry=freg)

    card = fr2es3.toCards()
    # from IPython import embed; embed()
    # assert card.keyword == "MATERIAL"
    # assert card.what1 == z
    # assert card.what3 == density
    # assert card.what6 == massNumber


    rpp = RPP("RPP_BODY", 0, 10, 0, 10, 0, 10, flukaregistry=freg)
    zone = Zone()
    zone.addIntersection(rpp)
    region = Region("RPP_REG") # should this be string or

    # material instance or maybe either?
    region.addZone(zone)
    freg.addRegion(region)

    freg.addMaterialAssignments(fr2es3, region)

    greg = convert.fluka2Geant4(freg)

    lvmat = greg.logicalVolumeDict["RPP_REG_lv"].material
    # assert lvmat.name == "FRANCIUM"
    # assert lvmat.density == density
    # assert lvmat.atomic_number == z
    # assert lvmat.atomic_weight == 223
    greg.getWorldVolume().clipSolid()

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer":v}

if __name__ == '__main__':
    Test(True, True)
