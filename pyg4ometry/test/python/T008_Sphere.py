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
    srmin  = _gd.Constant("rmin","8",reg,True)    
    srmax  = _gd.Constant("rmax","10",reg,True)
    ssphi  = _gd.Constant("sphi","0",reg,True)    
    sdphi  = _gd.Constant("dphi","pi",reg,True)
    sstheta= _gd.Constant("stheta","0",reg,True)    
    sdtheta= _gd.Constant("dtheta","3*pi/4",reg,True)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    sm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ss = _g4.solid.Sphere("ss",srmin,srmax,ssphi,sdphi,sstheta,sdtheta,reg,"mm","rad")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    sl = _g4.LogicalVolume(ss, sm, "sl", reg)
    sp = _g4.PhysicalVolume([0,0,0],[0,0,0],  sl, "s_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T008_Sphere.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True