import os as _os

import pyg4ometry.geant4 as _g4
import pyg4ometry.gdml   as _gd

def Test_MaterialPredefined() :

    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "100", reg, True)
    wy = _gd.Constant("wy", "100", reg, True)
    wz = _gd.Constant("wz", "100", reg, True)

    bx = _gd.Constant("bx", "10", reg, True)
    by = _gd.Constant("by", "10", reg, True)
    bz = _gd.Constant("bz", "10", reg, True)

    #######################################################################################
    wm = _g4.MaterialPredefined("G4_Galactic")
    bm = _g4.MaterialPredefined("G4_Fe")
    #######################################################################################

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    bs = _g4.solid.Box("bs", bx, by, bz, reg, "mm")

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], bl, "b_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T201_MaterialPredefined.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T201_MaterialPredefined.gmad"),"T201_MaterialPredefined.gdml")

def Test_MaterialSingleElement() :

    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "100", reg, True)
    wy = _gd.Constant("wy", "100", reg, True)
    wz = _gd.Constant("wz", "100", reg, True)

    bx = _gd.Constant("bx", "10", reg, True)
    by = _gd.Constant("by", "10", reg, True)
    bz = _gd.Constant("bz", "10", reg, True)

    #######################################################################################
    wm = _g4.MaterialSingleElement("galactic",1,1.008,1e-25,reg)   # low density hydrogen
    bm = _g4.MaterialSingleElement("iron",26,55.8452,7.874,reg)    # iron at near room temp
    #######################################################################################

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    bs = _g4.solid.Box("bs", bx, by, bz, reg, "mm")

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], bl, "b_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T201_MaterialSingleElement.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T201_MaterialSingleElement.gmad"),"T201_MaterialSingleElement.gdml")

def Test_MaterialCompoundMassFraction() :

    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "100", reg, True)
    wy = _gd.Constant("wy", "100", reg, True)
    wz = _gd.Constant("wz", "100", reg, True)

    bx = _gd.Constant("bx", "10", reg, True)
    by = _gd.Constant("by", "10", reg, True)
    bz = _gd.Constant("bz", "10", reg, True)

    #######################################################################################
    wm = _g4.MaterialCompound("air",1.290,2,reg)
    ne = _g4.ElementSimple("nitrogen","N",7,14.01)
    oe = _g4.ElementSimple("oxygen","O",8,16.0)
    wm.add_element_massfraction(ne,0.7)
    wm.add_element_massfraction(oe,0.3)
    bm = _g4.MaterialSingleElement("iron",26,55.8452,7.874,reg)    # iron at near room temp
    #######################################################################################

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    bs = _g4.solid.Box("bs", bx, by, bz, reg, "mm")

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bl = _g4.LogicalVolume(bs, bm, "bl", reg)
    bp = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], bl, "b_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T201_MaterialCompound.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),"T201_MaterialCompound.gmad"),"T201_MaterialCompound.gdml")