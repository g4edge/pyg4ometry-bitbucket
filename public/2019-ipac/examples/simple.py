import pyg4ometry.gdml as gd
import pyg4ometry.geant4 as g4
import pyg4ometry.visualisation as vi

import numpy as _np

# create empty data storage structure
reg = g4.Registry()

# expressions 
wx = gd.Constant("wx","100",reg)
wy = gd.Constant("wy","100",reg)
wz = gd.Constant("wz","100",reg)

bx = gd.Constant("bx","10",reg)
by = gd.Constant("by","10",reg)
bz = gd.Constant("bz","10",reg)

# materials
wm = g4.MaterialPredefined("G4_Galactic",reg) 
m  = g4.MaterialPredefined("G4_Fe",reg) 

# solids
wb = g4.solid.Box("wb",wx,wy,wz,reg)
b  = g4.solid.Box("b",bx,by,bz,reg)
s  = g4.solid.Orb("o",bx/2,reg)
t  = g4.solid.Tubs("t",0,bx/2,bz,0,2*_np.pi,reg)

# structure 
wl = g4.LogicalVolume(wb, wm, "wl", reg)
bl = g4.LogicalVolume(b, m, "b", reg)
sl = g4.LogicalVolume(s, m, "s", reg)
tl = g4.LogicalVolume(t, m, "t", reg)

bp = g4.PhysicalVolume([0,0,0.0],[0,0,0], 
                        bl, "b_pv", wl,reg) 
sp = g4.PhysicalVolume([0,0,0],[-2*bx,0,0], 
                        sl, "s_pv", wl,reg)  
tp = g4.PhysicalVolume([0,0.5,0],[2*bx,0,0], 
                        tl, "t_pv", wl,reg) 

# set world volume
reg.setWorld("wl")
                        
# gdml output
w = gd.Writer()
w.addDetector(reg)
w.write("simple.gdml")

# visualisation 
v = vi.VtkViewer()
v.addLogicalVolume(wl)
v.addAxes(40)
v.view()
