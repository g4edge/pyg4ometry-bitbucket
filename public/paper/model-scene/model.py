import pyg4ometry 
import os 

def buildModel(vis = True, write = True, render = False) :
    # 
    reg = pyg4ometry.geant4.Registry()

    world_material = pyg4ometry.geant4.MaterialPredefined("G4_Galactic")
    world_solid    = pyg4ometry.geant4.solid.Box("world_solid", 10000, 10000, 10000, reg, "mm")
    world_logical  = pyg4ometry.geant4.LogicalVolume(world_solid, world_material, "world_logical", reg)
    print(world_logical.name)

    # load gun chamber 
    reader_gunChamber   = pyg4ometry.gdml.Reader("./CuboidalChamber.gdml")
    gunChamber_logical  = reader_gunChamber.getRegistry().getWorldVolume()
    gunChamber_logical.name = "gunChamber_lv"
    print("gun chamber ",gunChamber_logical.name)
    gunChamber_assembly = gunChamber_logical.assemblyVolume()
    gunChamber_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                           [0,0,0],
                                                           gunChamber_assembly,
                                                           "gunChamber_physical",
                                                           world_logical,
                                                           reg,
                                                           addRegistry=False)
    print("gun chamber",gunChamber_logical.extent(includeBoundingSolid=False))
    reg.addVolumeRecursive(gunChamber_physical)

    # load gate
    reader_gateValve  = pyg4ometry.stl.Reader("./GV-100CF-C-M.stl")
    gateValve_solid   = reader_gateValve.getSolid()
    gateValve_material= pyg4ometry.geant4.MaterialPredefined("G4_Fe")
    gateValve_logical = pyg4ometry.geant4.LogicalVolume(gateValve_solid,
                                                        gateValve_material,
                                                        "gateValve_logical",
                                                        reg)
    gateValve_logical.name = "gateValve_lv"
    print("gate chamber",gateValve_logical.name)
    gateValve_assembly= gateValve_logical.assemblyVolume()
    # gateValve_logical.clipSolid()
    print("gate value", gateValve_logical.extent(includeBoundingSolid=True))
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
    triplet_logical.name = "triplet_lv"
    print("triplet ",triplet_logical.name)
    triplet_assembly = triplet_logical.assemblyVolume()
    triplet_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                        [0,0,900+2*38.9001],
                                                        triplet_assembly,
                                                        "triplet_physical",
                                                        world_logical,
                                                        reg,
                                                        addRegistry=False)
    #triplet_logical.clipSolid()
    print("triplet", triplet_logical.extent(includeBoundingSolid=False))
    reg.addVolumeRecursive(triplet_physical,"reuse")


    # load cad dipole
    reader_dipole = pyg4ometry.freecad.Reader("./10_SectorBendMedium.step")
    reader_dipole.relabelModel()
    reader_dipole.convertFlat()

    # Set materials for freecad dipole from G4_Galactic to something solid
    dipole_lvd = reader_dipole.getRegistry().logicalVolumeDict
    dipole_lvd["Solid_lv"].material = pyg4ometry.geant4.MaterialPredefined("G4_Fe")
    dipole_lvd["Solid001_lv"].material = pyg4ometry.geant4.MaterialPredefined("G4_Cu")
    dipole_lvd["Solid002_lv"].material = pyg4ometry.geant4.MaterialPredefined("G4_Cu")

    dipole_placement = reader_dipole.rootPlacement
    dipole_logical  = reader_dipole.getRegistry().getWorldVolume()
    dipole_logical.name = "dipole_lv"
    print("dipole ",dipole_logical.name)
    dipole_assembly = dipole_logical.assemblyVolume()
    # dipole_logical.clipSolid()
    dipole_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                       [dipole_placement[0],dipole_placement[1],900+2*38.9001+2450.000018+dipole_placement[2]],
                                                       dipole_assembly,
                                                       "dipole_physical",
                                                       world_logical,
                                                       reg,
                                                       addRegistry=False)
    print("dipole",dipole_logical.extent(includeBoundingSolid=True))
    reg.addVolumeRecursive(dipole_physical,"reuse")

    # load faraday cup
    reader_faraday  = pyg4ometry.fluka.Reader("faradayCup2.inp")
    faraday_greg    = pyg4ometry.convert.fluka2Geant4(reader_faraday.flukaregistry)
    faraday_logical = faraday_greg.getWorldVolume()
    faraday_logical.name = "faraday_lv"

    for d in faraday_logical.daughterVolumes :
        if d.name == "air_pv" :
            faraday_logical.daughterVolumes.remove(d)

    extentBB = faraday_logical.extent(includeBoundingSolid=False)

    print("faraday ",faraday_logical.name)
    faraday_assembly = faraday_logical.assemblyVolume()
    faraday_assembly.name = "faraday_av"

    faraday_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                      [0,0,900+2*38.9001+2450.000018+437.37*2+100],
                                                      faraday_assembly,
                                                      "faraday_physical",
                                                      world_logical,
                                                      reg,
                                                      addRegistry=False)
    print("faraday",faraday_logical.extent(includeBoundingSolid=True))
    reg.addVolumeRecursive(faraday_physical,"reuse")


    reg.setWorld("world_logical")

    print("world extent ", reg.getWorldVolume().extent())

    if vis :
        v = pyg4ometry.visualisation.PubViewer(size=(int(3360/2), int(920/2)))

        v.addLogicalVolume(reg.getWorldVolume())
        # v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])

        cam = v.ren.GetActiveCamera()
        cam.SetRoll(0)
        cam.SetPosition(2500, 1450.0, 1450.0)
        cam.SetFocalPoint(0, 0, 1700.00)
        cam.SetDistance(3400)

        v.view(interactive=True, resetCamera=False)

    
    # gdml output
    if write :
        w = pyg4ometry.gdml.Writer()
        w.addDetector(reg)
        w.write(os.path.join(os.path.dirname(__file__), "model.gdml"))    

    if render :
        r = pyg4ometry.visualisation.RenderWriter()
        r.addLogicalVolumeRecursive(reg.getWorldVolume())
        r.write("./model")

    return v

def buildSectorBend(vis=True, inter=True):
    # load cad dipole
    reader_dipole = pyg4ometry.freecad.Reader("./10_SectorBendMedium.step")
    reader_dipole.relabelModel()
    reader_dipole.convertFlat()

    dipole_placement = reader_dipole.rootPlacement
    dipole_logical   = reader_dipole.getRegistry().getWorldVolume()

    extentBB = dipole_logical.extent(includeBoundingSolid=False)

    if vis :
        v = pyg4ometry.visualisation.VtkViewer(size=(2280,1800))
        v.addLogicalVolume(dipole_logical)
        v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0]*1.25)

        v.actors[1].GetProperty().SetRepresentationToWireframe()
        v.setOpacity(1.0)
        v.setRandomColours(3)
        v.actors[1].GetProperty().SetColor(1,1,1)
        v.actors[1].GetProperty().SetLineWidth(5)
        cam = v.ren.GetActiveCamera()
        cam.SetRoll(0)
        cam.SetPosition(500,0, 2000)
        cam.SetDistance(795)

        v.view(interactive=inter, resetCamera=False)

    return v

def buildFaradayCup(vis = True,inter = True) :
    reader_faraday = pyg4ometry.fluka.Reader("faradayCup2.inp")
    faraday_greg = pyg4ometry.convert.fluka2Geant4(reader_faraday.flukaregistry)
    faraday_logical  = faraday_greg.worldVolume

    for d in faraday_logical.daughterVolumes :
        if d.name == "air_pv" :
            faraday_logical.daughterVolumes.remove(d)

    extentBB = faraday_logical.extent(includeBoundingSolid=False)
    
    if vis :
        v = pyg4ometry.visualisation.PubViewer(size=(1024,1024))
        v.addLogicalVolume(faraday_logical)
        v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
        v.setOpacity(0.7,4)


        cam = v.ren.GetActiveCamera()
        cam.SetRoll(0)
        cam.SetPosition(375, 375, -375)

        v.view(interactive=inter, resetCamera=False)

    return v

def buildChamber(vis = True, inter = True):
    reg = pyg4ometry.geant4.Registry()

    world_material = pyg4ometry.geant4.MaterialPredefined("G4_Galactic")
    world_solid    = pyg4ometry.geant4.solid.Box("world_solid", 10000, 10000, 10000, reg, "mm")
    world_logical  = pyg4ometry.geant4.LogicalVolume(world_solid, world_material, "world_logical", reg)

    # load gun chamber
    reader_gunChamber   = pyg4ometry.gdml.Reader("./CuboidalChamber.gdml")
    gunChamber_logical  = reader_gunChamber.getRegistry().getWorldVolume()
    gunChamber_assembly = gunChamber_logical.assemblyVolume()
    gunChamber_physical = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                                           [0,0,0],
                                                           gunChamber_assembly,
                                                           "gunChamber_physical",
                                                           world_logical,
                                                           reg,
                                                           addRegistry=False)

    extentBB = gunChamber_logical.extent(includeBoundingSolid=False)

    if vis :
        v = pyg4ometry.visualisation.VtkViewer(size=(int(3360/2), int(2010/2)))
        v.addLogicalVolume(gunChamber_logical)
        v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0]*1.25)

        v.setOpacity(1.0)
        v.setRandomColours(3)

        cam = v.ren.GetActiveCamera()
        cam.SetRoll(0)
        cam.SetPosition(1977.2553779137681, 1437.1208947635857, 1788.4781360684926)
        cam.SetFocalPoint(-170.93546811748698, 155.35523039050074, 99.51238355558247)
        cam.SetDistance(3018.319473233368)

        v.view(interactive=inter, resetCamera=False)

    return v

if __name__ == '__main__':
    buildModel()
