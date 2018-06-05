import pyg4ometry.geant4 as _g4
import pyg4ometry.vtk as _vtk
import pyg4ometry.gdml as _gdml

def pycsgmeshTest(vtkViewer = True, gdmlWriter = True) :
    _g4.registry.clear()
    
    worldSolid      = _g4.solid.Box('worldBox',250,250,100)
    worldLogical    = _g4.LogicalVolume(worldSolid,'G4_Galactic','worldLogical')


    is1          = _g4.Isotope("Wheat", 10, 15, 14.3)
    is2          = _g4.Isotope("Seeds", 10, 18, 2.3)

    el1          = _g4.Element.simple("Beef", "Bf", 54, 80)
    el2          = _g4.Element.simple("Cheese", "Ch", 26, 35)
    el3          = _g4.Element.composite("Bread", "Br", 2)
    el3.add_isotope(is1, 0.9)
    el3.add_isotope(is2, 0.1)

    mat1         = _g4.Material.composite("Hamburger", 1.67, 3)
    mat1.add_element_massfraction(el1, 0.3)
    mat1.add_element_massfraction(el2, 0.2)
    mat1.add_element_massfraction(el3, 0.5)

    #bsize        = _g4.Parameter("BOXSIZE",25)
    #boffset      = _g4.Parameter("BOXOFFSET",200)
    #zero         = _g4.Parameter("ZERO",0)

    bsize        = 25
    boffset      = 200
    zero         = 0

    #boxSolid1    = _g4.solid.Box('box1',2*bsize,2*bsize,2*bsize)
    #boxLogical1  = _g4.LogicalVolume(boxSolid1, mat1, 'boxLogical1')
    #boxPhysical1 = _g4.PhysicalVolume([0,0,0], [-2*boffset,-2*boffset,zero], boxLogical1,'boxPhysical1',worldLogical)

    boxSolid2    = _g4.solid.Box('box2',bsize,bsize,3*bsize)
    boxLogical2  = _g4.LogicalVolume(boxSolid2, mat1, 'boxLogical2')
    boxPhysical2 = _g4.PhysicalVolume([0,0,0],[zero,zero,zero],boxLogical2,'boxPhysical2',worldLogical)

    # clip the world logical volume
    worldLogical.setClip();

    # register the world volume
    _g4.registry.setWorld('worldLogical')

    # mesh the geometry
    m = worldLogical.pycsgmesh()

    # view the geometry
    if vtkViewer : 
        v = _vtk.Viewer()
        v.addPycsgMeshList(m)
        v.view();

    # write gdml
    if gdmlWriter : 
        w = _gdml.Writer()
        w.addDetector(_g4.registry)
        w.write('./Material.gdml')
        w.writeGmadTester('Material.gmad')        
