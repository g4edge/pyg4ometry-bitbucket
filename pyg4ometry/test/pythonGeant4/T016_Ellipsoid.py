import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False, n_slice=25,n_stack=25) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)
    
    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    eax = _gd.Constant("eax", "10", reg, True)
    eby = _gd.Constant("eby", "15", reg, True)
    ecz = _gd.Constant("ecz", "20", reg, True)
    ebc = _gd.Constant("ebc", "-15", reg, True)
    etc = _gd.Constant("etc", "15", reg, True)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    em = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    es = _g4.solid.Ellipsoid("es",eax,eby,ecz,ebc,etc,reg,nslice=n_slice,nstack=n_stack)

    print(es.mesh())
    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    el = _g4.LogicalVolume(es, em, "el", reg)
    ep = _g4.PhysicalVolume([0,0,0],[0,0,0],  el, "e_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T016_Ellipsoid.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T016_Ellipsoid.gmad"),"T016_Ellipsoid.gdml")

    # test __repr__
    str(es)

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
