import pyg4ometry.geant4 as _g4
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi

import pyg4ometry.test.pythonGeant4.T001_Box as _T001_Box

def Test() :

    # registry
    reg = _g4.Registry()

    # solids
    ws = _g4.solid.Box("ws", 200, 200, 200, reg, "mm")
    b1s = _g4.solid.Box("b1s", 50,   50,  50, reg, "mm")
    b2s = _g4.solid.Box("b2s", 10,   10,  10, reg, "mm")

    # materials
    wm = _g4.MaterialPredefined("G4_Galactic")
    bm = _g4.MaterialPredefined("G4_Fe")

    # structure
    wl  = _g4.LogicalVolume(ws, wm, "wl", reg)
    b1l = _g4.LogicalVolume(b1s, bm, "b1l", reg)
    b2l = _g4.LogicalVolume(b2s, bm, "b2l", reg)

    b2p1 = _g4.PhysicalVolume([0,0,0.5],[0,15,0], b2l, "b2_pv1", b1l, reg)
    b2p2 = _g4.PhysicalVolume([0,0,0],[0,-15,0], b2l, "b2_pv2", b1l, reg)

    b1p1 = _g4.PhysicalVolume([0, 0,  -0.5],     [0, 0, -50], b1l, "b1_pv1", wl, reg)
    b1p2 = _g4.PhysicalVolume([0, 0,  0.0],     [0, 0,   0], b1l, "b1_pv2", wl, reg)
    b1p3 = _g4.PhysicalVolume([0, 0,  0.5],     [0, 0,  50], b1l, "b1_pv3", wl, reg)

    v = _vi.VtkViewer()
    v.addLogicalVolume(wl)
    v.view()

    # set world volume
    reg.setWorld(wl.name)

    # freg, nfb = _convert.geant42Fluka(wl)

    freg = _convert.g2fTopLogical(wl)

    w = _fluka.Writer()
    w.addDetector(freg)
    w.write("T001_GdmlBox2Fluka.inp")
