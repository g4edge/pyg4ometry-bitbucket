import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False, n_slice = 20, n_stack = 20) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    trmin  = _gd.Constant("rmin","8.0",reg,True)
    trmax  = _gd.Constant("rmax","10.0",reg,True)
    trtor  = _gd.Constant("rtor","40.0",reg,True)
    tsphi  = _gd.Constant("sphi","0",reg,True)
    tsphi2 = _gd.Constant("sphi2s","0.3*pi",reg,True)
    tdphi  = _gd.Constant("dphi","1.5*pi",reg,True)
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    tm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ts1 = _g4.solid.Torus("ts1",trmin,trmax,trtor,tsphi, tdphi,reg,"mm","rad",nslice=n_slice,nstack=n_stack)
    ts2 = _g4.solid.Torus("ts2",trmin,trmax,trtor,tsphi2,tdphi,reg,"mm","rad",nslice=n_slice,nstack=n_stack)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    tl1 = _g4.LogicalVolume(ts1, tm, "tl1", reg)
    tl2 = _g4.LogicalVolume(ts2, tm, "tl2", reg)
    tp1 = _g4.PhysicalVolume([0,0,0],[0,0,0],   tl1, "t1_pv1", wl, reg)
    tp2 = _g4.PhysicalVolume([0,0,0],[0,0,2*trmax+5],  tl2, "t2_pv1", wl, reg) 

    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T010_Torus.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T010_Torus.gmad"),"T010_Torus.gdml")

    # test __repr__
    str(ts1)

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)
    extent   = wl.extent(includeBoundingSolid=False)

    # visualisation
    v = None
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.addAxes(_vi.axesFromExtents(extentBB)[0])
        v.view(interactive = interactive)

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}

if __name__ == "__main__":
    Test()
