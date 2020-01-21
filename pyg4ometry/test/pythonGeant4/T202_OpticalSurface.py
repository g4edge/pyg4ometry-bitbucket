import os as _os

import pyg4ometry.geant4 as _g4
import pyg4ometry.gdml   as _gd


def Test_OpticalSurface():
    reg = _g4.Registry()

    # defines
    # first dimension is energy, second dimension is a value of interest - e.g. refrective index
    ri_a = _gd.Matrix("RIND_Air", 2, [2.034e-06, 1, 2.068e-06, 1, 2.103e-06, 1, 2.139e-06, 1], reg)
    ri_w = _gd.Matrix("RIND_Water", 2, [2.034e-06, 1.3435, 2.068e-06, 1.344, 2.103e-06, 1.3445, 2.139e-06, 1.345], reg)
    al_w = _gd.Matrix("ABSLEN_Water", 2, [2.034e-06, 3448, 2.068e-06, 4082, 2.103e-06, 6329, 2.139e-06, 9174], reg)
    yr_w = _gd.Constant("YIELDRATIO", "0.8", reg, True)


    # World box
    wx = _gd.Constant("wx", "150", reg, True)
    wy = _gd.Constant("wy", "150", reg, True)
    wz = _gd.Constant("wz", "150", reg, True)

    # Outer big box
    ox = _gd.Constant("ox", "100", reg, True)
    oy = _gd.Constant("oy", "100", reg, True)
    oz = _gd.Constant("oz", "100", reg, True)

    # Water tank
    tx = _gd.Constant("tx", "50", reg, True)
    ty = _gd.Constant("ty", "50", reg, True)
    tz = _gd.Constant("tz", "50", reg, True)

    # Air bubble
    bx = _gd.Constant("bx", "10", reg, True)
    by = _gd.Constant("by", "10", reg, True)
    bz = _gd.Constant("bz", "10", reg, True)

    #######################################################################################
    wm = _g4.MaterialPredefined("G4_Galactic")

    ne = _g4.ElementSimple("Nitrogen", "N", 7, 14.01)
    he = _g4.ElementSimple("Hydrogen", "H", 1, 1.01)
    oe = _g4.ElementSimple("Oxygen", "O", 8, 16.0)

    air = _g4.MaterialCompound("Air", 1.290e-3, 2, reg)
    air.add_element_massfraction(ne, 0.7)
    air.add_element_massfraction(oe, 0.3)
    air.add_property("RINDEX", ri_a.name)

    water = _g4.MaterialCompound("Water", 1.0, 2, reg)
    water.add_element_massfraction(he, 0.112)
    water.add_element_massfraction(oe, 0.888)
    water.add_property("RINDEX", ri_w.name)
    water.add_property("YIELDRATIO", yr_w.name)

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    bigbox = _g4.solid.Box("bigbox", ox, oy, oz, reg, "mm")
    tank = _g4.solid.Box("tank", tx, ty, tz, reg, "mm")
    bubble = _g4.solid.Box("bubble", bx, by, bz, reg, "mm")

    opa = _g4.solid.OpticalSurface("AirSurface", finish="0", model="0", surf_type="1", value="1", registry=reg)
    opw = _g4.solid.OpticalSurface("WaterSurface", finish="3", model="1", surf_type="1", value="0", registry=reg)

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    ol = _g4.LogicalVolume(bigbox, wm, "bigbox_logical", reg)
    tl = _g4.LogicalVolume(tank, water, "tank_logical", reg)
    bl = _g4.LogicalVolume(bubble, air, "bubble_logical", reg)
    op = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], ol, "bigbox_pv", wl, reg)
    tp = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], tl, "tank_pv1", ol, reg)
    bp = _g4.PhysicalVolume([0, 0, 0], [0, 2.5, 0], bl, "bubble_pv1", tl, reg)
    _g4.SkinSurface("AirSurface", bl.name, "AirSurface", reg)
    _g4.BorderSurface("WaterSurface", bp.name, op.name, "WaterSurface", reg)

    #######################################################################################

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T202_Optical.gdml"))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__), "T201_Optical.gmad"),
                      "T201_Optical.gdml")