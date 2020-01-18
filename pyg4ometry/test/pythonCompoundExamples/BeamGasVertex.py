import pyg4ometry as _pyg
import pyg4ometry.visualisation as _vis

import numpy as _np

def Test(vis=False, interactive=False) :
    reg = _pyg.geant4.Registry() 

    safety       = _pyg.gdml.Defines.Constant("length_safety",1e-8,reg)
    twoPi        = _pyg.gdml.Defines.Constant("twoPi","2*pi",reg)
        
    bp_radius    = _pyg.gdml.Defines.Constant("beam_pipe_radius",7.5,reg)
    
    d_thickness  = _pyg.gdml.Defines.Constant("d_thickness",5,reg)
    d_height     = _pyg.gdml.Defines.Constant("d_height",300,reg)
    d_width      = _pyg.gdml.Defines.Constant("d_width",150,reg)

    d1_innerR    = _pyg.gdml.Defines.Constant("d1_innerR",15,reg)
    d1_outerR    = _pyg.gdml.Defines.Constant("d1_outerR",60,reg)
    d1_z         = _pyg.gdml.Defines.Constant("d1_z",0,reg)
    d1_y         = _pyg.gdml.Defines.Constant("d1_y",30,reg)+d_width/2

    d2_innerR    = _pyg.gdml.Defines.Constant("d2_innerR",15,reg)
    d2_outerR    = _pyg.gdml.Defines.Constant("d2_outerR",60,reg)
    d2_z         = _pyg.gdml.Defines.Constant("d2_z",500,reg)
    d2_y         = _pyg.gdml.Defines.Constant("d2_y",30,reg)+d_width/2

    d3_innerR    = _pyg.gdml.Defines.Constant("d3_innerR",15,reg)
    d3_outerR    = _pyg.gdml.Defines.Constant("d3_outerR",60,reg)
    d3_z         = _pyg.gdml.Defines.Constant("d3_z",1000,reg)
    d3_y         = _pyg.gdml.Defines.Constant("d3_y",30,reg)+d_width/2
    
    w_solid     = _pyg.geant4.solid.Box("w_solid",500,500,500 ,reg)
    w_logical   = _pyg.geant4.LogicalVolume(w_solid,"G4_Galactic","w_logical",reg)

    d_solid     = _pyg.geant4.solid.Box("d_solid",d_width,d_height,d_thickness,reg)
    bp_solid    = _pyg.geant4.solid.Polycone("bp_solid",0,twoPi,
                                             [0,10,10+1e-9,50,600,600+1e-9,1990,1990+1e-9,2000], 
                                             [15,15,15,15,195,15,15,15,15], 
                                             [30,30,20,20,200,20,20,30,30],reg,"mm","rad")
    d_logical   = _pyg.geant4.LogicalVolume(d_solid,"G4_Si","d_logical",reg)
    bp_logical  = _pyg.geant4.LogicalVolume(bp_solid,"G4_Fe","bp_logical",reg)

    d_physical1 = _pyg.geant4.PhysicalVolume([0,0,0],[d1_y,0,d1_z],d_logical,"d_physical1",w_logical,reg)
    d_physical2 = _pyg.geant4.PhysicalVolume([0,0,0],[d2_y,0,d2_z],d_logical,"d_physical2",w_logical,reg)
    d_physical3 = _pyg.geant4.PhysicalVolume([0,0,0],[d3_y,0,d3_z],d_logical,"d_physical3",w_logical,reg)

    d_physical4 = _pyg.geant4.PhysicalVolume([0,0,0],[-d1_y,0,d1_z],d_logical,"d_physical4",w_logical,reg)
    d_physical5 = _pyg.geant4.PhysicalVolume([0,0,0],[-d2_y,0,d2_z],d_logical,"d_physical5",w_logical,reg)
    d_physical6 = _pyg.geant4.PhysicalVolume([0,0,0],[-d3_y,0,d3_z],d_logical,"d_physical6",w_logical,reg)

    bp_physical = _pyg.geant4.PhysicalVolume([0,0,0],[0,0,-660],bp_logical,"bp_physical",w_logical,reg)

    w_logical.clipSolid()

    reg.setWorld("w_logical")

    ################################
    # visualisation
    ################################
    v = None
    if vis :
        v = _vis.VtkViewer()
        v.addLogicalVolume(w_logical)
        v.addAxes(100)
        v.setOpacity(0.25)
        v.view(interactive=interactive)


    w = _pyg.gdml.Writer() 
    w.addDetector(reg)
    w.write("detector.gdml")
    
    return w_logical

