=========
Tutorials
=========

Geant4 python scripting 
-----------------------

Making use of pyg4ometry requires the following modules 

.. code-block :: python

   import pyg4ometry               

To make a simple geometery of a box located at the origin

.. code-block :: python

   # load pyg4ometry
   import pyg4ometry               

   # registry to store gdml data
   reg  = pyg4ometry.geant4.Registry()
  
   # world solid and logical
   ws   = pyg4ometry.geant4.solid.Box("ws",50,50,50,reg)
   wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","wl",reg)

   # box placed at origin
   b1   = pyg4ometry.geant4.solid.Box("b1",10,10,10,reg)
   b1_l = pyg4ometry.geant4.LogicalVolume(b1,"G4_Fe","b1_l",reg)
   b1_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,0],b1_l,"b1_p",wl,reg)

   # visualise geometry
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(wl)
   v.addAxes(20)
   v.view()


A triangular mesh is generated from any physical ``volume`` by the following command 

.. code-block :: python

   m = volume.pycsgmesh()

Given an output from ``m = volume.pycsgmesh()`` it can be viewed in the ``vtk`` viewer with the following example

.. code-block :: python

    v = pyg4ometry.vtk.Viewer()  
    v.addPycsgMeshList(m)
    v.view();

To write an STL file from ``m = volume.pycsgmesh()`` 

.. code-block :: python

    vtkConverter = vtk.Convert()
    vtkPD        =  vtkConverter.MeshListToPolyData(m)
    r = vtk.WriteSTL("file.stl",vtkPD)

To write an GDML file file 

.. code-block :: python

    w = _gdml.Writer()
    w.addDetector(pyg.geant4.registry)
    w.write('./file.gdml')
    w.writeGmadTester('./file.gmad')  


GDML input 
----------

STL input 
---------

STEP/STP input
---------------

FULKA scripting
---------------

FLUKA input 
-----------

Merging geometry
----------------

STL output
----------
