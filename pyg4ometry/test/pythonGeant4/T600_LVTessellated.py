import os as _os
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vi


def Test(vis=False, interactive=False):
    reg = _g4.Registry()

    # defines
    wx = _gd.Constant("wx", "150", reg, True)
    wy = _gd.Constant("wy", "150", reg, True)
    wz = _gd.Constant("wz", "150", reg, True)

    # pi         = _gd.Constant("pi","3.1415926",reg,True)
    ctrmin     = _gd.Constant("trmin", "2.5", reg, True)
    ctrmax     = _gd.Constant("trmax", "10.0", reg, True)
    ctz        = _gd.Constant("tz", "110", reg, True)
    ctstartphi = _gd.Constant("startphi", "0", reg, True)
    ctdeltaphi = _gd.Constant("deltaphi", "1.5*pi", reg, True)
    ctlowx     = _gd.Constant("ctlowx", "-1", reg, True)
    ctlowy     = _gd.Constant("ctlowy", "-1", reg, True)
    ctlowz     = _gd.Constant("ctlowz", "-1", reg, True)
    cthighx    = _gd.Constant("cthighx", "1", reg, True)
    cthighy    = _gd.Constant("cthighy", "1", reg, True)
    cthighz    = _gd.Constant("cthighz", "1", reg, True)

    wm = _g4.Material(name="G4_Galactic")
    bm = _g4.Material(name="G4_Fe")

    # solids
    ws = _g4.solid.Box("ws", wx, wy, wz, reg, "mm")
    cts = _g4.solid.CutTubs("ts", ctrmin, ctrmax, ctz, ctstartphi, ctdeltaphi,
                            [ctlowx, ctlowy, ctlowz], [cthighx, cthighy, cthighz], reg, "mm", "rad")

    # structure
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    ctl = _g4.LogicalVolume(cts, bm, "ctl", reg)

    # Replace the standard solid of the logical volume with a Tessellated Solid version of itself
    ctl.makeSolidTessellated()  # Operation is in-place

    # Place the lv as normal
    ctp = _g4.PhysicalVolume([0, 0, 0], [0, 0, 0], ctl, "ct_pv1", wl, reg)

    # set world volume
    reg.setWorld(wl.name)

    # gdml output
    w = _gd.Writer()
    w.addDetector(reg)
    w.write(_os.path.join(_os.path.dirname(__file__), "T600_LVTessellated.gdml"))

    # visualisation
    if vis:
        v = _vi.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        v.view(interactive=interactive)

    return {"testStatus": True, "logicalVolume": wl}


if __name__ == "__main__":
    Test()
