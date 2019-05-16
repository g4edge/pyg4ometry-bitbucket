import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def CF_BeamPipe(bpLength = 200, bpId = 10, bpThickness = 5, cf_dn = '16') : 
    reg = _g4.Registry()

    cf_data = {'16': {'od':34, 'id':16, 'bd':27, 'h':7.5, 'nh':6, 'hd':4.3}}

    print cf_data[cf_dn]
    
    # defines 
    wx = _gd.Constant("wx",2*bpLength,reg,True)
    wy = _gd.Constant("wy",2*bpLength,reg,True)
    wz = _gd.Constant("wz",2*bpLength,reg,True)

    bpl  = _gd.Constant("bpl",bpLength,reg,True)
    bpId = _gd.Constant("bpId",cf_data[cf_dn]['id']/2.,reg,True)
    bpThickness = 
    bpOd = bpId+


    wm = _g4.MaterialPredefined("G4_Galactic") 
    bm = _g4.MaterialPredefined("G4_Fe") 

    # solids
    bps = _g4.solid.Box("bps",bpId,bpOd,bpl,0,2*_np.pi, reg, "mm")
    bs = _g4.solid.Box("bs",bx,by,bz, reg, "mm")
        
    # structure 
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp = _g4.PhysicalVolume([0,0,0],[0,0,0],  bl, "b_pv1", wl, reg) 
    
    # set world volume
    reg.setWorld(wl.name)
    
    # gdml output 
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "CF_BeamPipe.gdml"))

    v = _vi.VtkViewer()
    v.addLogicalVolume(reg.getWorldVolume())
    v.view()
