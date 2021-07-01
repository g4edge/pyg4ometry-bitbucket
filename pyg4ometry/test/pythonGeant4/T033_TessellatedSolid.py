import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis=False, interactive=False):
    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "5000", reg, True)
    wy = _gd.Constant("wy", "5000", reg, True)
    wz = _gd.Constant("wz", "5000", reg, True)

    p1 = [(-500, 500, 0), (500, 500, 0), (500, -500, 0), (-500, -500, 0)]
    p2 = [(-1000, 1000, 2000), (1000, 1000, 2000), (1000, -1000, 2000), (-1000, -1000, 2000)]

    polygons = [p1, p2]

    wm = _g4.MaterialPredefined("G4_Galactic")
    xm = _g4.MaterialPredefined("G4_Fe")

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    xtess = _g4.solid.createTessellatedSolid('test', polygons, reg)

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    tess_l = _g4.LogicalVolume(xtess, xm, "tess_l", reg)
    tess_p = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], tess_l, "tess_p", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T033_TessellatedSolid.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__), "T033_TessellatedSolid.gmad"), "T033_TessellatedSolid.gdml")

    # test __repr__
    str(xtess)

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)
    extent = wl.extent(includeBoundingSolid=False)

    # visualisation
    v = None
    if vis:
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.addAxes(_vi.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": wl, "vtkViewer": v}


if __name__ == "__main__":
    Test()
