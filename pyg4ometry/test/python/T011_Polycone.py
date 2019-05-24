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
    psphi  = _gd.Constant("sphi","1",reg,True)
    pdphi  = _gd.Constant("dphi","4",reg,True)

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
    ps = _g4.solid.Polycone("ps",psphi,pdphi,pz,prmin,prmax,reg,"mm","rad")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    pl = _g4.LogicalVolume(ps, pm, "pl", reg)
    tp = _g4.PhysicalVolume([0,0,0],[0,0,0],  pl, "p_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # test __repr__
    str(ps)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T011_Polycone.gdml"))

    # visualisation
    if vis : 
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view()

    return True

if __name__ == "__main__":
    Test()
