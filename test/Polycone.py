import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml
import numpy as _np

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()
    
    worldSolid      = _g4.solid.Box('worldBox',250,250,100)
    worldLogical    = _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')

    polyconeSolid1    = _g4.solid.Polycone("polycone_solid1", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical1  = _g4.LogicalVolume(polyconeSolid1,'G4_Cu','polyconeLogical1')
    polyconePhysical1 = _g4.PhysicalVolume([0,0,0],[-200,-200,0],polyconeLogical1,'polyconePhysical1',worldLogical)

    polyconeSolid2    = _g4.solid.Polycone("polycone_solid2", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical2  = _g4.LogicalVolume(polyconeSolid2,'G4_Cu','polyconeLogical2')
    polyconePhysical2 = _g4.PhysicalVolume([0,0,0],[-200,0,0],polyconeLogical2,'polyconePhysical2',worldLogical)

    polyconeSolid3    = _g4.solid.Polycone("polycone_solid3", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical3  = _g4.LogicalVolume(polyconeSolid3,'G4_Cu','polyconeLogical3')
    polyconePhysical3 = _g4.PhysicalVolume([0,0,0],[-200,200,0],polyconeLogical3,'polyconePhysical3',worldLogical)

    polyconeSolid4    = _g4.solid.Polycone("polycone_solid4", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical4  = _g4.LogicalVolume(polyconeSolid4,'G4_Cu','polyconeLogical4')
    polyconePhysical4 = _g4.PhysicalVolume([0,0,0],[0,-200,0],polyconeLogical4,'polyconePhysical4',worldLogical)

    polyconeSolid5    = _g4.solid.Polycone("polycone_solid5", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical5  = _g4.LogicalVolume(polyconeSolid5,'G4_Cu','polyconeLogical5')
    polyconePhysical5 = _g4.PhysicalVolume([0,0,0],[0,0,0],polyconeLogical5,'polyconePhysical5',worldLogical)
    
    polyconeSolid6    = _g4.solid.Polycone("polycone_solid6", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical6  = _g4.LogicalVolume(polyconeSolid6,'G4_Cu','polyconeLogical6')
    polyconePhysical6 = _g4.PhysicalVolume([0,0,0],[0,200,0],polyconeLogical6,'polyconePhysical6',worldLogical)

    polyconeSolid7    = _g4.solid.Polycone("polycone_solid7", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical7  = _g4.LogicalVolume(polyconeSolid7,'G4_Cu','polyconeLogical7')
    polyconePhysical7 = _g4.PhysicalVolume([0,0,0],[200,-200,0],polyconeLogical7,'polyconePhysical7',worldLogical)

    polyconeSolid8    = _g4.solid.Polycone("polycone_solid8", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical8  = _g4.LogicalVolume(polyconeSolid8,'G4_Cu','polyconeLogical8')
    polyconePhysical8 = _g4.PhysicalVolume([0,0,0],[200,0,0],polyconeLogical8,'polyconePhysical8',worldLogical)

    polyconeSolid9    = _g4.solid.Polycone("polycone_solid9", _np.pi/4., 3*_np.pi/2, [5*5,5*7,5*9,5*11,5*25,5*27,5*29,5*31,5*35], [0,0,0,0,0,0,0,0,0], [0,5*10,5*10,5*5,5*5,5*10,5*10,5*2,5*2])
    polyconeLogical9  = _g4.LogicalVolume(polyconeSolid9,'G4_Cu','polyconeLogical9')
    polyconePhysical9 = _g4.PhysicalVolume([0,0,0],[200,200,0],polyconeLogical9,'polyconePhysical9',worldLogical)

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
        w.write('./Polycone.gdml')
