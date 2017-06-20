import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml
import numpy as _np

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()

    worldSolid   = _g4.solid.Box('worldBox', 250,250,100)
    worldLogical =  _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')

    trapSolid1    = _g4.solid.Trap('trap1',
                                   60,
                                   _np.pi/9., 5*_np.pi/180.,
                                   40, 30, 40,
                                   _np.pi/18.,
                                   16, 10, 14,
                                   _np.pi/18.)
    
    trapLogical1  = _g4.LogicalVolume(trapSolid1,'G4_Cu','trapLogical1')
    trapPhysical1 = _g4.PhysicalVolume([0,0,0],[0,0,0], trapLogical1,'trapPhysical1',worldLogical)

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
        w.write('./Trap.gdml')
        w.writeGmadTester('Trap.gmad')        
