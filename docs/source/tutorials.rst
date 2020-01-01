=========
Tutorials
=========

GDML input 
----------

STL input 
---------

STEP/STP input
---------------

FLUKA input 
-----------

Merging geometry
----------------

Assembly conversion
-------------------

GDML output 
-----------

To write an GDML file file 

.. code-block :: python

    w = _gdml.Writer()
    w.addDetector(pyg.geant4.registry)
    w.write('./file.gdml')
    w.writeGmadTester('./file.gmad')  


STL output
----------

To write an STL file from ``m = volume.pycsgmesh()`` 

.. code-block :: python

    vtkConverter = vtk.Convert()
    vtkPD        =  vtkConverter.MeshListToPolyData(m)
    r = vtk.WriteSTL("file.stl",vtkPD)

