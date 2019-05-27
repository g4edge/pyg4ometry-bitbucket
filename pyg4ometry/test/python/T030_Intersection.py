import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis = False) : 
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    bx = _gd.Constant("bx","10",reg,True)
    by = _gd.Constant("by","10",reg,True)
    bz = _gd.Constant("bz","10",reg,True)
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    bm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    bs = _g4.solid.Box("bs",bx,by,bz, reg, "mm")
    ns = _g4.solid.Intersection("ns",bs,bs,[[0.1,0.2,0.3],[bx/2,by/2,bz/2]],reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    nl = _g4.LogicalVolume(ns, bm, "nl", reg)
    np = _g4.PhysicalVolume([0,0,0],[0,0,0],  nl, "i_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # test __repr__
    str(ns)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T030_Intersection.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True

if __name__ == "__main__":
    Test()