import os as _os
import pyg4ometry.geant4 as _g4
import pyg4ometry.gdml as _gd
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi
import numpy as _np

normal = 1
zcut_outofrange = 2

def Test(vis = False, interactive = False, type = normal, n_slice=16) :

    # registry
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)
    
    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    edx    = _gd.Constant("eax","0.2",reg,True)
    edy    = _gd.Constant("eby","0.4",reg,True)
    ezmax  = _gd.Constant("ecz","50",reg,True)
    ezcut  = _gd.Constant("ebc","0.5",reg,True)

    if type == zcut_outofrange : 
        ezcut.setExpression(30)

    wm = _g4.MaterialPredefined("G4_Galactic") 
    em = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    es = _g4.solid.EllipticalCone("es",edx,edy,ezmax,ezcut,reg,"mm",nslice=n_slice)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    el = _g4.LogicalVolume(es, em, "el", reg)
    ep = _g4.PhysicalVolume([0,0,0],[0,0,0],  el, "e_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # test extent of physical volume
    extentBB = wl.extent(includeBoundingSolid=True)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T017_geant4EllipticalCone2Fluka.gdml"))

    # fluka conversion
    #freg = _convert.geant4Logical2Fluka(wl)
    #w = _fluka.Writer()
    #w.addDetector(freg)
    #w.write(_os.path.join(_os.path.dirname(__file__),"T017_geant4EllipticalCone2Fluka.inp"))

    # flair output file
    f = _fluka.Flair("T017_geant4EllipticalCone2Fluka.inp",extentBB)
    f.write(_os.path.join(_os.path.dirname(__file__),"T017_geant4Elliptical2Fluka.flair"))

    if vis :
        v = _vi.VtkViewer()
        v.addLogicalVolume(wl)
        v.addAxes(_vi.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)
