import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka import PLA, Region, Zone, FlukaRegistry


def Test(vis=False, interactive=False):
    freg = FlukaRegistry()

    # Bigger cube.
    pla_a1 = PLA("PLA_A1_BODY",
                 [0, 0, 20],
                 [0, 0, 20],
                 flukaregistry=freg)
    pla_a2 = PLA("PLA_A2_BODY",
                 [0, 0, 20],
                 [0, 0, 0],
                 flukaregistry=freg)
    pla_b1 = PLA("PLA_B1_BODY",
               [0, 20, 0],
               [0, 20, 0],
               flukaregistry=freg)
    pla_b2 = PLA("PLA_B2_BODY",
               [0, 20, 0],
               [0, 0, 0],
               flukaregistry=freg)
    pla_c1 = PLA("PLA_C1_BODY",
               [20, 0, 0],
               [20, 0, 0],
               flukaregistry=freg) 
    pla_c2 = PLA("PLA_C2_BODY",
               [20, 0, 0],
               [0, 0, 0],
               flukaregistry=freg) 
    
    z1 = Zone()

    # Box1:
    z1.addIntersection(pla_a1)
    z1.addSubtraction(pla_a2)
    z1.addIntersection(pla_b1)
    z1.addSubtraction(pla_b2)
    z1.addIntersection(pla_c1)
    z1.addSubtraction(pla_c2)


    region1 = Region("REG_INF1")
    region1.addZone(z1)
    
    freg.addRegion(region1)

    greg = convert.fluka2Geant4(freg, True, False)

    wlv = greg.getWorldVolume()
    wlv.checkOverlaps()

    if vis:
        v = vi.VtkViewer()
        v.addAxes(length=20)
        v.addLogicalVolume(wlv)
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": greg.getWorldVolume()}



if __name__ == '__main__':
    Test(True, True)