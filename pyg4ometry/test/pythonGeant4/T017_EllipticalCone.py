import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi

normal = 1
zcut_outofrange = 2

def Test(vis = False, interactive = False, type = normal,n_slice=16) :
    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx","100",reg,True)
    wy = _gd.Constant("wy","100",reg,True)
    wz = _gd.Constant("wz","100",reg,True)

    # pi     = _gd.Constant("pi","3.1415926",reg,True)
    edx    = _gd.Constant("eax","0.5",reg,True)
    edy    = _gd.Constant("eby","1",reg,True)
    ezmax  = _gd.Constant("ecz","40",reg,True)
    ezcut  = _gd.Constant("ebc","20",reg,True)

    if type == zcut_outofrange :
        ezcut.setExpression(30)

    wm = _g4.MaterialPredefined("G4_Galactic")
    em = _g4.MaterialPredefined("G4_Fe")

    # solids
    ubox = _g4.solid.Box("boxxx",500, 500, 500, reg, "mm")
    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    es = _g4.solid.EllipticalCone("es",edx,edy,ezmax,ezcut,reg,"mm",nslice=n_slice)
    union = _g4.solid.Union("myunion", ubox, es, [[0, 0, 0], [0, 0, 0,]], reg)

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    el = _g4.LogicalVolume(es, em, "el", reg)
    # el = _g4.LogicalVolume(union, em, "ul", reg)
    ep = _g4.PhysicalVolume([0,0,0],[0,0,0],  el, "e_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T017_EllipticalCone.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T017_EllipticalCone.gmad"),"T017_EllipticalCone.gdml")

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
        v.addAxes(length=20)
        v.view(interactive = interactive)

    return {"testStatus": True, "logicalVolume":wl, "vtkViewer":v}
