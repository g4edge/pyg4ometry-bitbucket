import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()

    worldSolid   = _g4.solid.Box('worldBox', 250,250,100)
    worldLogical =  _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')
    
    tetSolid1 = _g4.solid.Tet('tet1',[0,0,17],[0,8,0],[8,-8,0],[-8,-8,0])
    tetLogical1  = _g4.LogicalVolume(tetSolid1,'G4_Cu','tetLogical1')
    tetPhysical1 = _g4.PhysicalVolume([0,0,0],[0,0,0], tetLogical1,'tetPhysical1',worldLogical)

    # clip the world logical volume
    worldLogical.setClip();

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
        w.write('./Tet.gdml')
        w.writeGmadTester('Tet.gmad')
