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
    eax    = _gd.Constant("eax","10",reg,True)
    eby    = _gd.Constant("eby","15",reg,True)
    ecz    = _gd.Constant("ecz","20",reg,True)
    ebc    = _gd.Constant("ebc","-15",reg,True)
    etc    = _gd.Constant("etc","15",reg,True)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    em = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    es = _g4.solid.Ellipsoid("es",eax,eby,ecz,ebc,etc,reg)
        
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
    w.write(_os.path.join(_os.path.dirname(__file__), "T016_Ellipsoid.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True

if __name__ == "__main__":
    Test()
