import pyg4ometry.geant4 as _g4
import pyg4ometry.visualisation as _vis
import pyg4ometry.gdml as _gdml
import warnings as _warnings

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()

    worldSolid      = _g4.solid.Box('worldBox',250,250,100)
    worldLogical    = _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')

    box1_solid   = _g4.solid.Box("b1", 10, 10, 10)
    box1_logical = _g4.LogicalVolume(box1_solid,'G4_Cu','box1_logical')
    box1_volume  = _g4.PhysicalVolume([0,0,0], [0, 0, 0], box1_logical,  "box1_physical", worldLogical)

    box2_solid   = _g4.solid.Box("b2", 10, 10, 10)
    box2_logical = _g4.LogicalVolume(box2_solid,'G4_Cu','box2_logical')
    box2_volume  = _g4.PhysicalVolume([0,0,0.785], [0, 0, 7.5], box2_logical,  "box2_physical", worldLogical)


    # clip the world logical volume
    worldLogical.setClip();

    # register the world volume
    _g4.registry.setWorld('worldLogical')

    if vtkViewer:
        _vis.viewWorld(checkOverlaps=True)

    if gdmlWriter:
        warnings.warn("GDML file writing not supported for overlap test! No file produced, contunie...")



