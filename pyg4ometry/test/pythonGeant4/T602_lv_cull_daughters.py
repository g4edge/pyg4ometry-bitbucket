import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis=False, interactive=False):
    reg = _g4.Registry()

    wm = _g4.Material(name="G4_Galactic")
    bm = _g4.Material(name="G4_W")

    # solids
    ws = _g4.solid.Box("ws", 3, 3, 3, reg, "m")

    x = 1
    ds = _g4.solid.Box("ds", x, x, x, reg, "m")
    dds = _g4.solid.Box("dds", 0.2, 0.2, 0.2, reg, "m")
    
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    dlv = _g4.LogicalVolume(ds, wm, "dlv", reg)
    ddlv = _g4.LogicalVolume(dds, bm, "ddlv", reg)

    nX = 4
    dX = x*1000 / nX
    x0 = -0.5*x*1000 + 0.5*dX
    print(x0)
    for xi in range(nX):
        for yi in range(nX):
            pos = [x0+xi*dX, x0+yi*dX, 0]
            print(pos)
            _g4.PhysicalVolume([0,0,0],
                               pos,
                               ddlv,
                               "ddpv_"+str(xi)+str(yi),
                               dlv,
                               reg)

    _g4.PhysicalVolume([0,0,0],
                       [0,0,0],
                       dlv,
                       "dlv_pv",
                       wl,
                       reg)

    # now for the culling
    clipFW = 500 # this should cut out the middle 4 from 16
    clipBox = _g4.solid.Box("clipper", clipFW, clipFW, clipFW, reg, "mm")
    dlv.cullDaughtersOutsideSolid(clipBox)

    # set world volume
    reg.setWorld(wl)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T602_lv_cull_daughters.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__))+"T602_lv_cull_daughters.gmad","T602_lv_cull_daughters.gdml")
    
    # visualisation
    v = None
    if vis:
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.addSolid(clipBox)
        v.view(interactive=interactive)

    assert(len(dlv.daughterVolumes) == 4)

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}


if __name__ == "__main__":
    Test(vis=True)
