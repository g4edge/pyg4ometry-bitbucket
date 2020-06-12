from pyg4ometry.fluka import RPP, RCC, FlukaRegistry, Zone, Region
import pyg4ometry.visualisation as vi


def main():
    freg = FlukaRegistry()

    rpp1 = RPP("RPP1", 0, 10, 0, 10, 0, 10, flukaregistry=freg)
    rpp2 = RPP("RPP2", 2.5, 7.5, 2.5, 7.5, 2.5, 7.5, flukaregistry=freg)
    rcc = RCC("RCC", [2.5, 2.5, 2.5], [0, 0, 5], 2.5, flukaregistry=freg)

    z1 = Zone()
    z1.addIntersection(rpp1)
    z2 = Zone()
    z1.addSubtraction(z2)
    z2.addIntersection(rpp2)
    z2.addSubtraction(rcc)
    region = Region("thing")
    region.addZone(z1)

    assert len(z1.toDNF("dnfreg").zones) == 2
    assert len(region.toDNF("dnfreg").zones) == 2

    v = vi.VtkViewer()
    v.addMeshSimple(dnfreg2.mesh())
    v.view()
    pass


if __name__ == '__main__':
    main()
