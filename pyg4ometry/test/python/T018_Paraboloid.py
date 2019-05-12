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
    
    pi   = _gd.Constant("pi","3.1415926",reg,True)
    prlo = _gd.Constant("prlo","2",reg,True)
    prhi = _gd.Constant("prhi","15",reg,True)
    pz   = _gd.Constant("pz","50",reg,True)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    pm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ps = _g4.solid.Paraboloid("ps",pz,prlo,prhi,reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    pl = _g4.LogicalVolume(ps, pm, "pl", reg)
    pp = _g4.PhysicalVolume([0,0,0],[0,0,0],  pl, "p_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T018_Paraboid.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True
