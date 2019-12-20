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
    
    tbx    = _gd.Constant("bx","10",reg,True)
    tby    = _gd.Constant("by","20",reg,True)
    tbz    = _gd.Constant("bz","30",reg,True)
    tbphit = _gd.Constant("bt","1.0",reg,True)
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    tm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ts = _g4.solid.TwistedBox("ts",tbphit, tbx, tby, tbz, reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    tl = _g4.LogicalVolume(ts, tm, "tl", reg)
    tp = _g4.PhysicalVolume([0,0,0],[0,0,0],  tl, "t_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # test __repr__
    str(ts)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T022_TwistedBox.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T022_TwistedBox.gmad"),"T022_TwistedBox.gdml")


    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view(interactive = interactive)

    return {"testStatus": True, "logicalVolume":wl}

if __name__ == "__main__":
    Test()
