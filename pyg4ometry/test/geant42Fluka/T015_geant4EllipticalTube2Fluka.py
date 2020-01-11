import pyg4ometry.geant4 as _g4
import pyg4ometry.gdml as _gd
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi


def Test() :

    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "100", reg, True)
    wy = _gd.Constant("wy", "100", reg, True)
    wz = _gd.Constant("wz", "100", reg, True)

    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    ex = _gd.Constant("ex", "10", reg, True)
    ey = _gd.Constant("ey", "25", reg, True)
    ez = _gd.Constant("ez", "20", reg, True)

    wm = _g4.MaterialPredefined("G4_Galactic")
    em = _g4.MaterialPredefined("G4_Fe")

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    es = _g4.solid.EllipticalTube("es", ex, ey, ez, reg)

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    el = _g4.LogicalVolume(es, em, "el", reg)
    ep = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], el, "e_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    v = _vi.VtkViewer()
    v.addLogicalVolume(wl)
    v.view()

    freg = _convert.geant42FlukaLogical(wl)

    w = _fluka.Writer()
    w.addDetector(freg)
    w.write("T015_geant4EllipticalTube2Fluka.inp")
