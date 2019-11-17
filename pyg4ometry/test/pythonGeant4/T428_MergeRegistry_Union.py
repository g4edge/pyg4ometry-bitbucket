import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


import T001_Box
import T028_Union

def Test(vis = False, interactive = False) :
    reg0 = _g4.Registry()

    l1 = T001_Box.Test(False,False)["logicalVolume"]
    l2 = T028_Union.Test(False,False)["logicalVolume"]

    wx0 = _gd.Constant("wx0", "200", reg0, True)
    wy0 = _gd.Constant("wy0", "200", reg0, True)
    wz0 = _gd.Constant("wz0", "200", reg0, True)

    wm = _g4.MaterialPredefined("G4_Galactic")
    ws = _g4.solid.Box("ws", wx0, wy0, wz0, reg0, "mm")
    wl = _g4.LogicalVolume(ws, wm, "wl", reg0)

    p1 = _g4.PhysicalVolume([0,0,0],[-50,0,0], l1, "l1_pv", wl, reg0)
    p2 = _g4.PhysicalVolume([0,0,0],[ 50,0,0], l2, "l2_pv", wl, reg0)

    reg0.addVolumeRecursive(p1)
    reg0.addVolumeRecursive(p2)

    reg0.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg0)
    w.write(_os.path.join(_os.path.dirname(__file__), "T428_MergeRegistry_Union.gdml"))

    # visualisation
    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg0.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus":True, "logicalVolume":wl, "registrty":reg0}

if __name__ == "__main__":
    Test()