import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()

    worldSolid   = _g4.solid.Box('worldBox', 250,250,100)
    worldLogical =  _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')

    extrudedsolidSolid1    = _g4.solid.ExtrudedSolid('extrudedsolid1',
                                                     [[-30,-30],[-30,30],[30,30],[30,-30],[15,-30],[15,15],[-15,15],[-15,-30]],
                                                     [[-60,[0,30],0.8],[-15,[0,-30],1.],[10,[0,0],0.6],[60,[0,30],1.2]])
    extrudedsolidLogical1  = _g4.LogicalVolume(extrudedsolidSolid1,'G4_Cu','extrudedsolidLogical1')
    extrudedsolidPhysical1 = _g4.PhysicalVolume([0,0,0],[-200,-200,0], extrudedsolidLogical1,'extrudedsolidPhysical1',worldLogical)

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
        w.write('./ExtrudedSolid.gdml')
