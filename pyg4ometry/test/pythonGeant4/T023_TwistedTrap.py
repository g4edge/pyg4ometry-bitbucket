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
    
    ttwist = _gd.Constant("tptwist","1.0",reg,True)

    tx1    = _gd.Constant("tx1","5",reg,True)
    tx2    = _gd.Constant("tx2","5",reg,True)
    tx3    = _gd.Constant("tx3","10",reg,True)
    tx4    = _gd.Constant("tx4","10",reg,True)

    ty1    = _gd.Constant("ty1","5",reg,True)
    ty2    = _gd.Constant("ty2","7.5",reg,True)

    tz     = _gd.Constant("tz","10.0",reg,True)

    ttheta = _gd.Constant("ttheta","0.6",reg,True)
    tphi   = _gd.Constant("tphi","0.0",reg,True)
    talp   = _gd.Constant("talp","0.0",reg,True)
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    tm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ts = _g4.solid.TwistedTrap("ts",ttwist,tz,ttheta,tphi,ty1,tx1,tx2,ty2,tx3,tx4,talp,reg)
        
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
    w.write(_os.path.join(_os.path.dirname(__file__), "T023_TwistedTrap.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view(interactive = interactive )

    return {"testStatus": True, "logicalVolume":wl}

if __name__ == "__main__":
    Test()
