import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import QUA, Region, Zone, FlukaRegistry, Extent, XYP, XZP

def Test(vis=False, interactive=False) :
    freg = FlukaRegistry()



    parabolicCylinder = QUA("parab",
                            0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -20,
                            flukaregistry=freg)

    end1 = XYP("end1", 20, flukaregistry=freg)
    end2 = XYP("end2",  0, flukaregistry=freg)
    end3 = XZP("end3", -30, flukaregistry=freg)

    z = Zone()
    z.addIntersection(parabolicCylinder)
    z.addIntersection(end1)
    z.addSubtraction(end2)
    z.addSubtraction(end3)

    region = Region("QUA_REG", material="COPPER")
    region.addZone(z)
    freg.addRegion(region)

    quaExtent = {"QUA_REG": Extent([-150., 0., 0], [150., 200., 200.])}

    greg = convert.fluka2Geant4(freg,
                                quadricRegionExtents=quaExtent)

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer":v}

if __name__ == '__main__':
    Test(True, True)
