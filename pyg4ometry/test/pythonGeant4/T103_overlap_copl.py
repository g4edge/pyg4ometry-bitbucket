import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    bx = _gd.Constant("bx","10",reg,True)

    b1pos = _gd.Position("b1pos",-bx,0,0,"mm",reg,True)
    b2pos = _gd.Position("b2pos",0,0,0,"mm",reg,True)
    b2pos = _gd.Position("b3pos",bx,0,0,"mm",reg,True)


    wm = _g4.MaterialPredefined("G4_Galactic") 
    bm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    bs = _g4.solid.Box("bs",bx,0.9*bx,0.9*bx, reg, "mm")
    rs = _g4.solid.Box("rs",3*bx,2*bx,2*bx, reg, "mm")


    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)

    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    rl = _g4.LogicalVolume(rs, wm, "rl", reg)

    bp1 = _g4.PhysicalVolume([0.2,0,0],  [-bx,0,0],  bl, "b_pv1", rl, reg)
    bp2 = _g4.PhysicalVolume([0.4,0,0],  [0  ,0,0],  bl, "b_pv2", rl, reg)
    bp3 = _g4.PhysicalVolume([0.6,0,0],[bx ,0,0],  bl, "b_pv3", rl, reg)

    rp  = _g4.PhysicalVolume([0,0,0],  [0,0,0],    rl, "r_pv1", wl, reg)

    # check for overlaps
    wl.checkOverlaps(True)

    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T103_overlap_copl.gdml"))

    # test __repr__
    str(bs)

    # test extent of physical volume
    wlextent           = wl.extent(True)
    wlextent_daughters = wl.extent(False)

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume":wl}

if __name__ == "__main__":
    Test()