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

    # pi        = _gd.Constant("pi","3.1415926",reg,True)

    ttwist    = _gd.Constant("tptwist","1.0",reg,True)
    trmin     = _gd.Constant("trmin","2.5",reg,True)
    trmax     = _gd.Constant("trmax","10.0",reg,True)    
    tz        = _gd.Constant("tz","50",reg,True)
    tphi      = _gd.Constant("phi","1.5*pi",reg,True)
    
    wm = _g4.Material(name="G4_Galactic") 
    bm = _g4.Material(name="G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ts = _g4.solid.TwistedTubs("ts",trmin,trmax,tz,tphi,ttwist,reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    tl = _g4.LogicalVolume(ts, bm, "tl", reg)
    tp = _g4.PhysicalVolume([0,0,0],[0,0,0],  tl, "t_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T025_TwistedTubs.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T025_TwistedTubs.gmad"),"T025_TwistedTubs.gdml")

    # test __repr__
    str(ts)

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)
    extent   = wl.extent(includeBoundingSolid=False)

    # visualisation
    v = None
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.addAxes(_vi.axesFromExtents(extentBB)[0])
        v.view(interactive = interactive )

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}

if __name__ == "__main__":
    Test()
