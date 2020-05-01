import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False, n_slice = 64) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)
    
    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    psphi  = _gd.Constant("sphi","0",reg,True)
    pdphi  = _gd.Constant("dphi","1.5*pi",reg,True)

    prmin1 = _gd.Constant("prmin1","1",reg,True)
    prmax1 = _gd.Constant("prmax1","9",reg,True)
    pz1    = _gd.Constant("z1","-10",reg,True)

    prmin2 = _gd.Constant("prmin2","5",reg,True)
    prmax2 = _gd.Constant("prmax2","9",reg,True)
    pz2    = _gd.Constant("z2","0",reg,True)

    prmin3 = _gd.Constant("prmin3","3",reg,True)
    prmax3 = _gd.Constant("prmax3","5",reg,True)
    pz3    = _gd.Constant("z3","10",reg,True)

    prmin = [prmin1,prmin2,prmin3]
    prmax = [prmax1,prmax2,prmax3]
    pz    = [pz1,pz2,pz3]
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    pm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ps = _g4.solid.Polycone("ps",psphi,pdphi,pz,prmin,prmax,reg,"mm","rad",nslice=n_slice)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    pl = _g4.LogicalVolume(ps, pm, "pl", reg)
    tp = _g4.PhysicalVolume([0,0,0],[0,0,0],  pl, "p_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T011_Polycone.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T011_Polycone.gmad"),"T011_Polycone.gdml")

    # test __repr__
    str(ps)

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
