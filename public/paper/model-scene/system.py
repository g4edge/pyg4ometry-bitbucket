import pyg4ometry 
import os 

def buildSystem(vis = True, write = True) :
    # 
    reg = pyg4ometry.geant4.Registry()

    world_material = pyg4ometry.geant4.MaterialPredefined("G4_Galactic")
    world_solid    = pyg4ometry.geant4.solid.Box("world_solid", 10000, 10000, 10000, reg, "mm")
    world_logical  = pyg4ometry.geant4.LogicalVolume(world_solid, world_material, "world_logical", reg)

    # load gun chamber 
    reader_gunChamber   = pyg4ometry.gdml.Reader("./CuboidalChamber.gdml")
    gunChamber_logical  = reader_gunChamber.getRegistry().getWorldVolume()
    gunChamber_assembly = gunChamber_logical.assemblyVolume()
    # gunChamber_logical.clipSolid()
    gunChamber_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                           [0,0,0],
                                                           gunChamber_assembly,
                                                           "gunChamber_physical",
                                                           world_logical,
                                                           reg,
                                                           addRegistry=False) 
    
    print(gunChamber_logical.extent(includeBoundingSolid=False))

    reg.addVolumeRecursive(gunChamber_physical)

    # load gate 
    reader_gateValve  = pyg4ometry.stl.Reader("./GV-100CF-C-M.stl")
    gateValve_solid   = reader_gateValve.getSolid()
    gateValve_material= pyg4ometry.geant4.MaterialPredefined("G4_Fe")     
    gateValve_logical = pyg4ometry.geant4.LogicalVolume(gateValve_solid,
                                                        gateValve_material,
                                                        "gateValve_logical",
                                                        reg)
    gateValve_assembly= gateValve_logical.assemblyVolume()
    # gateValve_logical.clipSolid()
    print(gateValve_logical.extent(includeBoundingSolid=True))
    gateValve_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                          [0,0,900+38.9001],
                                                          gateValve_logical,
                                                          "gateValve_physical",
                                                          world_logical,
                                                          reg,
                                                          False)     
    reg.addVolumeRecursive(gateValve_physical)

    # load magnets
    reader_triplet = pyg4ometry.gdml.Reader("./quad_triplet.gdml")
    triplet_logical = reader_triplet.getRegistry().getWorldVolume()
    triplet_assembly = triplet_logical.assemblyVolume()
    triplet_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                        [0,0,900+2*38.9001],
                                                        triplet_assembly,
                                                        "triplet_physical",
                                                        world_logical,
                                                        reg,
                                                        addRegistry=False)
    #triplet_logical.clipSolid()
    print(triplet_logical.extent(includeBoundingSolid=False))
    reg.addVolumeRecursive(triplet_physical,"reuse")


    # load cad dipole 
    reader_dipole = pyg4ometry.freecad.Reader("./09_SectorBendSmall.step")
    reader_dipole.relabelModel()
    reader_dipole.convertFlat()

    dipole_placement = reader_dipole.rootPlacement
    dipole_logical  = reader_dipole.getRegistry().getWorldVolume()
    dipole_assembly = dipole_logical.assemblyVolume()
    # dipole_logical.clipSolid()
    dipole_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                       [dipole_placement[0],dipole_placement[1],900+2*38.9001+2450.000018+dipole_placement[2]],
                                                       dipole_assembly,
                                                       "dipole_physical",
                                                       world_logical,
                                                       reg,
                                                       addRegistry=False)
    print(dipole_logical.extent(includeBoundingSolid=True))
    reg.addVolumeRecursive(dipole_physical,"reuse") 
   
    reg.setWorld("world_logical")
    
    if vis :
        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(reg.getWorldVolume())
        # v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
        v.view(interactive=True)

    
    # gdml output
    if write :
        w = pyg4ometry.gdml.Writer()
        w.addDetector(reg)
        w.write(os.path.join(os.path.dirname(__file__), "system.gdml"))    
    
    
    
