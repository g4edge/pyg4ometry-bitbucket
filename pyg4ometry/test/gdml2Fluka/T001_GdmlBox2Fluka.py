import pyg4ometry.geant4 as _g4
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka

import pyg4ometry.test.pythonGeant4.T001_Box as _T001_Box

def Test() :

    # registry
    reg = _g4.Registry()

    # solids
    ws = _g4.solid.Box("ws", 100, 100, 100, reg, "mm")
    bs = _g4.solid.Box("bs", 20,   20,  20, reg, "mm")

    # materials
    wm = _g4.MaterialPredefined("G4_Galactic")
    bm = _g4.MaterialPredefined("G4_Fe")

    # structure
    wl  = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl  = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp1 = _g4.PhysicalVolume([0, 0, 0],     [0, 0, -50], bl, "b_pv1", wl, reg)
    bp2 = _g4.PhysicalVolume([0, 0, 0],     [0, 0,   0], bl, "b_pv2", wl, reg)
    bp3 = _g4.PhysicalVolume([0, 0, 0.785], [0, 0,  50], bl, "b_pv3", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    freg, nfb = _convert.geant42Fluka(wl)

    w = _fluka.Writer()
    w.addDetector(freg)
    w.write("T001_GdmlBox2Fluka.inp")