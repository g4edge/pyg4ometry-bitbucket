import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi

normal = 1
two_planes = 2

def Test(vis = False, interactive = False, type = normal) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    
    pi     = _gd.Constant("pi","3.1415926",reg,True)
    psphi  = _gd.Constant("sphi","1",reg,True)
    pdphi  = _gd.Constant("dphi","4",reg,True)
    pnsid  = _gd.Constant("pnsid","4",reg,True) 
    
    pr1    = _gd.Constant("pr1","1",reg,True)
    pz1    = _gd.Constant("pz1","-10",reg,True)

    pr2    = _gd.Constant("pr2","2",reg,True)
    pz2    = _gd.Constant("pz2","0",reg,True)

    pr3    = _gd.Constant("pr3","1",reg,True)
    pz3    = _gd.Constant("pz3","10",reg,True)

    pr     = [pr1,pr2,pr3]
    pz     = [pz1,pz2,pz3]

    if type == two_planes : 
        pr = [pr1,pr2]
        pz = [pz1,pz2]
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    pm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    ps = _g4.solid.GenericPolyhedra("ps",psphi,pdphi,pnsid,pr,pz,reg,"mm","rad")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    pl = _g4.LogicalVolume(ps, pm, "pl", reg)
    tp = _g4.PhysicalVolume([0,0,0],[0,0,0],  pl, "p_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T014_GenericPolyhedra.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T014_GenericPolyhedra.gmad"),"T014_GenericPolyhedra.gdml")

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
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}

if __name__ == "__main__":
    Test()
