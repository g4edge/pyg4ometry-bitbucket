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

    pi     = _gd.Constant("pi","3.1415926",reg,True)
    crmin1 = _gd.Constant("crmin1","6",reg,True)
    crmax1 = _gd.Constant("crmax1","20",reg,True)
    crmin2 = _gd.Constant("crmin2","5",reg,True)
    crmax2 = _gd.Constant("crmax2","10",reg,True)
    cz     = _gd.Constant("cz","100",reg,True)
    cdp    = _gd.Constant("cdp","1.5*pi",reg,True)
    zero   = _gd.Constant("zero","0.0",reg,False)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    cm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    cs = _g4.solid.Cons("cs",crmin1,crmax1,crmin2,crmax2,cz,zero,1.5*pi,reg,"mm")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    cl = _g4.LogicalVolume(cs, cm, "cl", reg)
    cp = _g4.PhysicalVolume([0,0,0],[0,0,0],  cl, "c_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T004_Cons.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True

if __name__ == "__main__":
    Test()
