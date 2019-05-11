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
    trmin  = _gd.Constant("rmin","8.0",reg,True)
    trmax  = _gd.Constant("rmax","10.0",reg,True)
    trtor  = _gd.Constant("rtor","50.0",reg,True)    
    tsphi  = _gd.Constant("sphi","0",reg,True)
    tdphi  = _gd.Constant("dphi","2*pi",reg,True)
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    tm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ts = _g4.solid.Torus("ts",trmin,trmax,trtor,tsphi,tdphi,reg,"mm","rad")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    tl = _g4.LogicalVolume(ts, tm, "tl", reg)
    tp = _g4.PhysicalVolume([0,0,0],[0,0,0],  tl, "t_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T010_Torus.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True
