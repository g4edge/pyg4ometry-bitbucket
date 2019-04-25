import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test() : 
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    bx = _gd.Constant("bx","10",reg,True)
    by = _gd.Constant("by","10",reg,True)
    bz = _gd.Constant("bz","10",reg,True)
    
    wm = _g4.Material(name="G4_Galactic") 
    bm = _g4.Material(name="G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, "mm", reg)
    bs = _g4.solid.Box("bs",bx,by,bz, "mm", reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp = _g4.PhysicalVolume([0,0,0],[0,0,0],  bl, "b_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write("T001_Box.gdml")

    return True
