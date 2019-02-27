import pyg4ometry.gdml as gd
import pyg4ometry.geant4 as g4
import pyg4ometry.visualisation as vi

# create empty data storage structure
reg = g4.Registry()

# expressions
wx = gd.Constant("wx","50",reg)
wy = gd.Constant("wy","50",reg)
wz = gd.Constant("wz","50",reg)
bx = gd.Constant("bx","10",reg)
by = gd.Constant("by","10",reg)
bz = gd.Constant("bz","10",reg)

# materials
bm = g4.Material.nist("G4_Galactic")
wm = g4.Material.nist("G4_Fe")

# solids
wb = g4.solid.Box("wb",wx,wy,wz,reg)
b  = g4.solid.Box("b",bx,by,bz,reg)

# structure
wl = g4.LogicalVolume(wb, wm, "wl", reg)
bl = g4.LogicalVolume(b, bm, "b", reg)
bp1 = g4.PhysicalVolume([0,0,0],[0,0,0],
                        bl, "b_pv1", wl, reg)
bp2 = g4.PhysicalVolume([0,0,-0.25],[-3*bx,0,0],
                        bl, "b_pv2", wl, reg)
bp3 = g4.PhysicalVolume([0,0,0.5],[3*bx,0,0],
                        bl, "b_pv3", wl, reg)

# physical volume vistualisation attributes
bp1.visOptions.color = (1,0,0)
bp1.visOptions.alpha = 0.25
bp2.visOptions.color = (0,1,0)
bp2.visOptions.representation = "wireframe"
bp3.visOptions.color = (0,0,1)

# gdml output
w = gd.Writer()
w.write(reg,"output.gdml")

# visualisation
v = vi.VtkViewer()
v.addLogicalVolume(wl)
v.addAxes()
v.view()
