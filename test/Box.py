import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()
    
    worldSolid      = _g4.solid.Box('worldBox',250,250,100)
    worldLogical    = _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')

    boxSolid1    = _g4.solid.Box('box1',25,25,25)
    boxLogical1  = _g4.LogicalVolume(boxSolid1,'G4_Cu','boxLogical1')
    boxPhysical1 = _g4.PhysicalVolume([0,0,0],[-200,-200,0],boxLogical1,'boxPhysical1',worldLogical)

    boxSolid2    = _g4.solid.Box('box2',25,25,75)
    boxLogical2  = _g4.LogicalVolume(boxSolid2,'G4_Cu','boxLogical2')
    boxPhysical2 = _g4.PhysicalVolume([0,0,0],[-200,0,0],boxLogical2,'boxPhysical2',worldLogical)

    boxSolid3    = _g4.solid.Box('box3',25,75,25)
    boxLogical3  = _g4.LogicalVolume(boxSolid3,'G4_Cu','boxLogical3')
    boxPhysical3 = _g4.PhysicalVolume([0,0,0],[-200,200,0],boxLogical3,'boxPhysical3',worldLogical)

    boxSolid4    = _g4.solid.Box('box4',75,25,25)
    boxLogical4  = _g4.LogicalVolume(boxSolid4,'G4_Cu','boxLogical4')
    boxPhysical4 = _g4.PhysicalVolume([0,0,0],[0,-200,0],boxLogical4,'boxPhysical4',worldLogical)

    # register the world volume
    _g4.registry.setWorld('worldLogical')
    
    m = worldLogical.pycsgmesh()
    
    if vtkViewer : 
        v = _vtk.Viewer()
        v.addPycsgMeshList(m)
        v.view();

    # write gdml
    if gdmlWriter : 
        w = _gdml.Writer()
        w.addDetector(_g4.registry)
        w.write('./Box.gdml')
