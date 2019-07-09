import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi

normal = 1
zcut_outofrange = 2

def Test(vis = False, type = normal) : 
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)
    
    pi     = _gd.Constant("pi","3.1415926",reg,True)
    edx    = _gd.Constant("eax","0.2",reg,True)
    edy    = _gd.Constant("eby","0.4",reg,True)
    ezmax  = _gd.Constant("ecz","50",reg,True)
    ezcut  = _gd.Constant("ebc","15",reg,True)

    if type == zcut_outofrange : 
        ezcut.setExpression(30)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    em = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    es = _g4.solid.EllipticalCone("es",edx,edy,ezmax,ezcut,reg,"mm")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    el = _g4.LogicalVolume(es, em, "el", reg)
    ep = _g4.PhysicalVolume([0,0,0],[0,0,0],  el, "e_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # test __repr__
    str(es)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T017_EllipticalCone.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True

if __name__ == "__main__":
    Test()