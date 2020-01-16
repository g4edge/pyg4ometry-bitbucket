import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import QUA, Region, Zone, FlukaRegistry

def Test(vis=False, interactive=False) :
    freg = FlukaRegistry()

    qua = QUA("QUA_BODY",10,10,0,0,10,0,0,0,0,-1, flukaregistry=freg)
    z = Zone()
    z.addIntersection(qua)
    region = Region("QUA_REG", material="COPPER")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    greg.getWorldVolume().clipSolid()

    # test extent of physical volume
    extentBB = greg.getWorldVolume().extent(includeBoundingSolid=True)

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=vi.axesFromExtents(extentBB)[0])
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer":v}

if __name__ == '__main__':
    Test(True, True)
