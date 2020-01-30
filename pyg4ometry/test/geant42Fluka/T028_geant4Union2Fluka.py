import pyg4ometry.gdml as _gd
import pyg4ometry.convert as _convert
import pyg4ometry.geant4 as _g4
import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False, disjoint = False) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    bx = _gd.Constant("bx","10",reg,True)
    by = _gd.Constant("by","10",reg,True)
    bz = _gd.Constant("bz","10",reg,True)
    
    wm = _g4.MaterialPredefined("G4_Galactic") 
    bm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    bs = _g4.solid.Box("bs",bx,by,bz, reg, "mm")
    if not disjoint :
        us = _g4.solid.Union("us",bs,bs,[[0.1,0.2,0.3],[bx/2,by/2,bz/2]],reg)
    else :
        us = _g4.solid.Union("us",bs,bs,[[0.1,0.2,0.3],[bx*2,by*2,bz*2]],reg)
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    ul = _g4.LogicalVolume(us, bm, "ul", reg)
    up = _g4.PhysicalVolume([0,0,0],[0,0,0],  ul, "u_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

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

    freg = _convert.geant4Logical2Fluka(wl)

    w = _fluka.Writer()
    w.addDetector(freg)
    w.write("T028_geant4Union2Fluka.inp")

if __name__ == "__main__":
    Test()