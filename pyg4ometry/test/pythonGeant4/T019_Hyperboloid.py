import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi

normal = 1
rmin_eq_zero = 2
rmin_gt_rmax = 3

def Test(vis = False, interactive = False, type = normal, n_slice = 16, n_stack = 16) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)
    
    pi    = _gd.Constant("pi","3.1415926",reg,True)
    hrmin = _gd.Constant("hrmin","20",reg,True)
    hrmax = _gd.Constant("hrmax","30.0",reg,True)
    hz    = _gd.Constant("hz","50.0",reg,True)
    hinst = _gd.Constant("hinst","0.7",reg,True)
    houtst= _gd.Constant("houtst","0.7",reg,True)
    
    if type == rmin_eq_zero : 
        hrmin.setExpression(0)

    if type == rmin_gt_rmax :
        hrmin.setExpression(2)
        hrmax.setExpression(1)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    hm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    hs = _g4.solid.Hype("ps",hrmin, hrmax, hinst, houtst, hz, reg,nslice=n_slice,nstack=n_stack)
        
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
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T019_Hyperboloid.gmad"),"T019_Hyperboloid.gdml")

    # test __repr__
    str(hs)

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
