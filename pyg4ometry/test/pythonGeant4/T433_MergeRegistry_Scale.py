import pyg4ometry


def Test(vis=False, interactive=False):

    reg0 = pyg4ometry.geant4.Registry()
    scale = pyg4ometry.gdml.Defines.Scale("sca_reflection", 1, 1, -1, registry=reg0)

    vacuum = pyg4ometry.geant4.MaterialPredefined("G4_Galactic", reg0)
    iron   = pyg4ometry.geant4.MaterialPredefined("G4_Fe", reg0)

    world   = pyg4ometry.geant4.solid.Box("world_solid", 200, 200, 200, reg0)
    worldLV = pyg4ometry.geant4.LogicalVolume(world, vacuum, "world_lv", reg0)
    
    box   = pyg4ometry.geant4.solid.Box("box_solid", 10, 20, 50, reg0)
    boxLV = pyg4ometry.geant4.LogicalVolume(box, iron, "box_lv", reg0)

    pv1 = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                           [50,0,0],
                                           boxLV,
                                           "box_pv1",
                                           worldLV,
                                           reg0)

    pv2 = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                           [-50,0,0],
                                           boxLV,
                                           "box_pv2",
                                           worldLV,
                                           reg0,
                                           scale=scale)

    pv3 = pyg4ometry.geant4.PhysicalVolume([0,0,0],
                                           [-50,-50,0],
                                           boxLV,
                                           "box_pv3",
                                           worldLV,
                                           reg0,
                                           scale=scale)

    # create another registry and add the world to it
    reg1 = pyg4ometry.geant4.Registry()
    reg1.addVolumeRecursive(worldLV)

    v = None
    if vis:
        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(worldLV)
        v.view()

    return {"testStatus": True, "logicalVolume":worldLV, "vtkViewer":v}
    
if __name__ == "__main__":
    Test()
