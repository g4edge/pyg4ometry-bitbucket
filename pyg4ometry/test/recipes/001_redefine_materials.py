import pyg4ometry


def redefineMaterialsFreecad():
    r = pyg4ometry.freecad.Reader("../freecad/05_Placement.step")
    r.convertFlat()

    # Get the registry
    reg = r.getRegistry()

    # Make new materials as needed
    new_mat = pyg4ometry.geant4.MaterialPredefined("G4_Cu")

    # Define a dictionary mapping volume names to new materials
    new_mats = {"Cone_ZRot_lv" : new_mat}

    # Assign new materials only to volumes from the dict
    for lvname in reg.logicalVolumeDict:
        mat = reg.logicalVolumeDict[lvname].material
        reg.logicalVolumeDict[lvname].material = new_mats.get(lvname, mat)

    w = pyg4ometry.gdml.Writer()
    w.addDetector(r.getRegistry())
    w.write("001_redefined_materials.gdml")

if __name__=="__main__":
    redefineMaterialsFreecad()
