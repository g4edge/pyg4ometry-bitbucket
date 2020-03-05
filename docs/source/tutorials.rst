=========
Tutorials
=========

GDML loading 
------------

In directory ``pyg4ometry/pyg4ometry/test/gdmlG4examples/ChargeExchangeMC/``

.. code-block :: python

   import pyg4ometry
   r = pyg4ometry.gdml.Reader("lht.gdml")
   l = r.getRegistry().getWorldVolume()
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(l)
   v.view()

.. figure:: tutorials/tutorial1.png
   :alt: Example of loading a GDML file


STL loading 
-----------

STL files are typically used for a single watertight solid mesh. This mesh is 
converted to a TesselatedSolid and then a logical volume which can be placed 
in a geometry. In directory ``pyg4ometry/pyg4ometry/test/stl``.

.. code-block :: python

   import pyg4ometry
   reg = pyg4ometry.geant4.Registry()
   r = pyg4ometry.stl.Reader("utahteapot.stl")
   l = r.logicalVolume("test","G4_Cu",reg)
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(l)
   v.view()

.. figure:: tutorials/tutorial2.png
   :alt: Example of STL loading in pyg4ometry


STEP/STP loading
----------------

In directory ``pyg4ometry/pyg4ometry/test/freecad``

.. code-block :: python 

   import pyg4ometry
   r  = pyg4ometry.freecad.Reader("./08_AshTray.step")
   r.relabelModel()
   r.convertFlat()
   l = r.getRegistry().getWorldVolume()
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(l)
   v.view()

.. figure:: tutorials/tutorial3.png
   :alt: Example of STEP loading in pyg4ometry

Fluka loading and conversion to Geant4
--------------------------------------

Merging geometry
----------------

Assembly conversion
-------------------

Given two sources of geometry, placement of top level world logical volume solids will 
likely result in an overlap. To avoid these types of problems, it might required to convert
one of the logical volumes to an AssemblyVolume.

STL output
----------

To write an STL file from ``m = volume.pycsgmesh()`` 

.. code-block :: python

    vtkConverter = vtk.Convert()
    vtkPD        =  vtkConverter.MeshListToPolyData(m)
    r = vtk.WriteSTL("file.stl",vtkPD)

Conversion to Fluka and output
------------------------------

It is possible convert a pyg4ometry geometry to Fluka. This is currently a work in 
progress and not all geant4-GDML constructions are implemented, although they can
be quickly added. Given a LV variable named ``logical``  

.. code-block :: python

   import pyg4ometry
   freg = _convert.geant4Logical2Fluka(logical)
   w = pyg4ometry.fluka.Writer()
   w.addDetector(freg)
   w.write("FileName.inp")

