import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False, n_slice=10, n_stack=10) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    srmin  = _gd.Constant("rmin","8",reg,True)    
    srmax  = _gd.Constant("rmax","10",reg,True)
    ssphi  = _gd.Constant("sphi","0",reg,True)
    # sdphi  = _gd.Constant("dphi","2*pi",reg,True)
    sdphi = _gd.Constant("dphi", "1.75*pi", reg, True)
    sstheta= _gd.Constant("stheta","0",reg,True)
    sdtheta= _gd.Constant("dtheta","0.75*pi",reg,True)
    # sdtheta = _gd.Constant("dtheta", "pi", reg, True)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    sm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ss = _g4.solid.Sphere("ss",srmin,srmax,ssphi,sdphi,sstheta,sdtheta,reg,"mm","rad",nslice=n_slice, nstack=n_stack)
        
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
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T008_Sphere.gmad"),"T008_Sphere.gdml")

    # test __repr__
    str(ss)

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)
    extent   = wl.extent(includeBoundingSolid=False)

    # visualisation
    v = None
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.addAxes(_vi.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}

if __name__ == "__main__":
    Test()
    
