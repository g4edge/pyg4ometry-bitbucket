import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi


def Test(vis = False, interactive = False) :
    reg = _g4.Registry()
    
    # defines 
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)
    
    p1x = _gd.Constant("p1x","-15",reg,True)
    p1y = _gd.Constant("p1y","-15",reg,True)

    p2x = _gd.Constant("p2x","-15",reg,True)
    p2y = _gd.Constant("p2y","15",reg,True)

    p3x = _gd.Constant("p3x","15",reg,True)
    p3y = _gd.Constant("p3y","15",reg,True)

    p4x = _gd.Constant("p4x","15",reg,True)
    p4y = _gd.Constant("p4y","-15",reg,True)    

    z1  = _gd.Constant("z1","-20",reg,True)
    x1  = _gd.Constant("x1","0",reg,True)
    y1  = _gd.Constant("y1","0",reg,True)
    s1  = _gd.Constant("s1","2.0",reg,True)

    z2  = _gd.Constant("z2","0",reg,True)
    x2  = _gd.Constant("x2","5",reg,True)
    y2  = _gd.Constant("y2","5",reg,True)
    s2  = _gd.Constant("s2","0.5",reg,True)

    z3  = _gd.Constant("z3","20",reg,True)
    x3  = _gd.Constant("x3","0",reg,True)
    y3  = _gd.Constant("y3","0",reg,True)
    s3  = _gd.Constant("s3","1.0",reg,True)

    polygon = [[p1x,p1y], [p2x,p2y], [p3x,p3y], [p3x,p4y]]
    slices  = [[z1,[x1,y1],s1], [z2,[x2,y2],s2], [z3,[x3,y3],s3]]
          
    wm = _g4.MaterialPredefined("G4_Galactic") 
    xm = _g4.MaterialPredefined("G4_Fe")

    # solids
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    xs = _g4.solid.ExtrudedSolid("xs", polygon,slices, reg)
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    xl = _g4.LogicalVolume(xs, xm, "xl", reg)
    xp = _g4.PhysicalVolume([0,0,0],[0,0,0],  xl, "x_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)

    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T021_geant4ExtrudedSolid2Fluka.gdml"))

    # fluka conversion
    freg = _convert.geant4Logical2Fluka(wl)
    w = _fluka.Writer()
    w.addDetector(freg)
    w.write("T021_geant4ExtrudedSolid2Fluka.inp")

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
