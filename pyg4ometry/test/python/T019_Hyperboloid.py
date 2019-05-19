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
    
    pi    = _gd.Constant("pi","3.1415926",reg,True)
    hrmin = _gd.Constant("hrmin","1.0",reg,True)
    hrmax = _gd.Constant("hrmax","2.0",reg,True)
    hz    = _gd.Constant("hz","20.0",reg,True)
    hinst = _gd.Constant("hinst","3",reg,True)
    houtst= _gd.Constant("houtst","4",reg,True)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    hm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    hs = _g4.solid.Hype("ps",hrmin, hrmax, hinst, houtst, hz, reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    hl = _g4.LogicalVolume(hs, hm, "hl", reg)
    hp = _g4.PhysicalVolume([0,0,0],[0,0,0],  hl, "h_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T019_Hyperboloid.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True
