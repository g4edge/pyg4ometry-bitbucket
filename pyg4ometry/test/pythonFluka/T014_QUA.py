import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import QUA, Region, Zone, FlukaRegistry

def Test(vis, interactive) :
    freg = FlukaRegistry()

    qua = QUA("QUA_BODY",10,10,10,0,0,0,0,0,0,0, flukaregistry=freg)
    z = Zone()
    z.addIntersection(qua)
    region = Region("QUA_REG", material="COPPER")
    region.addZone(z)
    freg.addRegion(region)

    greg = convert.fluka2Geant4(freg)

    greg.getWorldVolume().clipSolid()

    v = None
    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(greg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume(), "vtkViewer":v}

if __name__ == '__main__':
    Test()
