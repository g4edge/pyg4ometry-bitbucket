import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()

    worldSolid   = _g4.solid.Box('worldBox', 250,250,100)
    worldLogical =  _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')
    
    tetSolid1 = _g4.solid.Tet('tet1',[0,0,17],[0,8,0],[8,-8,0],[-8,-8,0])
    tetLogical1  = _g4.LogicalVolume(tetSolid1,'G4_Cu','tetLogical1')
    tetPhysical1 = _g4.PhysicalVolume([0,0,0],[20,20,0], tetLogical1,'tetPhysical1',worldLogical)

    tetSolid2 = _g4.solid.Tet('tet2',[0,0,17.3],[0,2*8.2,-5.8],[-1.41,-0.8,-0.58],[1.41,-0.8,-0.58])
    tetLogical2  = _g4.LogicalVolume(tetSolid2,'G4_Cu','tetLogical2')
    tetPhysical2 = _g4.PhysicalVolume([0,0,0],[20,0,0], tetLogical2,'tetPhysical2',worldLogical)

    tetSolid3 = _g4.solid.Tet('tet3',[0,0,0],[0,10,0],[10,0,0],[0,0,10])
    tetLogical3  = _g4.LogicalVolume(tetSolid3,'G4_Cu','tetLogical3')
    tetPhysical3 = _g4.PhysicalVolume([0,0,0],[0,20,0], tetLogical3,'tetPhysical3',worldLogical)

    tetSolid4 = _g4.solid.Tet('tet4',[0,0,6],[0,9,0],[0,-8,0],[-8,-8,0])
    tetLogical4  = _g4.LogicalVolume(tetSolid4,'G4_Cu','tetLogical4')
    tetPhysical4 = _g4.PhysicalVolume([0,0,0],[0,0,0], tetLogical1,'tetPhysical4',worldLogical)

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
