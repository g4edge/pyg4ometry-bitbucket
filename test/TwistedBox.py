import pygeometry.geant4 as _g4
import pygeometry.vtk as _vtk
import pygeometry.gdml as _gdml

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()

    worldSolid   = _g4.solid.Box('worldBox', 250,250,100)
    worldLogical =  _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')

    twistedBoxSolid1    = _g4.solid.TwistedBox('twistedBox1',0.5, 30, 40, 60)
    twistedBoxLogical1  = _g4.LogicalVolume(twistedBoxSolid1,'G4_Cu','twistedBoxLogical1')
    twistedBoxPhysical1 = _g4.PhysicalVolume([0,0,0],[0,0,0], twistedBoxLogical1,'twistedBoxPhysical1',worldLogical)

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
        w.write('./TwistedBox.gdml')
