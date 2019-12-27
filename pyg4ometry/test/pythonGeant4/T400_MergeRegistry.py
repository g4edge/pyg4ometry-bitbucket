import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi

def MakeGeometry() :
    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "50", reg, True)
    wy = _gd.Constant("wy", "50", reg, True)
    wz = _gd.Constant("wz", "50", reg, True)

    bx = _gd.Constant("bx", "10", reg, True)
    by = _gd.Constant("by", "10", reg, True)
    bz = _gd.Constant("bz", "10", reg, True)

    wm = _g4.MaterialPredefined("G4_Galactic")
    bm = _g4.MaterialPredefined("G4_Fe")

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    bs = _g4.solid.Box("bs", bx, by, bz, reg, "mm")

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], bl, "b_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    return reg


def Test(vis = False, interactive=False) :
    reg0 = _g4.Registry()
    reg1 = MakeGeometry()
    reg2 = MakeGeometry()

    l1 = reg1.getWorldVolume()
    l2 = reg2.getWorldVolume()

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
    w.write(_os.path.join(_os.path.dirname(__file__), "T400_MergeRegistry.gdml"))

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)
    extent   = wl.extent(includeBoundingSolid=False)

    # visualisation
    v = None
    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg0.getWorldVolume())
        v.addAxes(_vi.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}


if __name__ == "__main__":
    Test()
