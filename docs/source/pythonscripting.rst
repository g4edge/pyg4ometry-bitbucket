===============================
Basic python geometry scripting
===============================

Geant4 python scripting 
-----------------------

Making use of pyg4ometry requires the following modules 

.. code-block :: python

   import pyg4ometry               

To make a simple geometery of a box located at the origin

.. code-block :: python
   :linenos:

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

Here is the vtk visualiser output of the above example

.. figure:: pythonscripting/pythonscripting1.tiff
   :alt: map to buried treasure

GDML defines 
------------

In GDML there are multiple ``define`` objects that can be used parametrise 
geometry, materials etc. For example a GDML constant can be created in the 
following way 

.. code-block :: python

   # registry to store gdml data
   reg = pyg4ometry.geant4.Registry()

   # constant called x 
   x = pyg4ometry.gdml.Constant("x",10,reg)

The normal set of mathematical operations in python can be performed and 
evaluated

.. code-block :: python

   y = 2*x + 10
   y.eval()

.. code-block :: python

   >> 30

The constant ``x`` can of course be changed and ``y`` re-evaluated
   
.. code-block :: python

   x.setExpression(5)
   y.eval()

.. code-block :: python

   >> 20

So the box example above can be rewritten using constants

.. code-block :: python
   :linenos:     
   :emphasize-lines: 7-9,16

   # load pyg4ometry
   import pyg4ometry

   # registry to store gdml data
   reg  = pyg4ometry.geant4.Registry()

   bx = pyg4ometry.gdml.Constant("bx","10",reg,True)
   by = pyg4ometry.gdml.Constant("by",2*bx,reg,True)
   bz = pyg4ometry.gdml.Constant("bz",2*by,reg,True)

   # world solid and logical
   ws   = pyg4ometry.geant4.solid.Box("ws",50,50,50,reg)
   wl   = pyg4ometry.geant4.LogicalVolume(ws,"G4_Galactic","wl",reg)

   # box placed at origin
   b1   = pyg4ometry.geant4.solid.Box("b1",bx,by,bz,reg)
   b1_l = pyg4ometry.geant4.LogicalVolume(b1,"G4_Fe","b1_l",reg)
   b1_p = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,0],b1_l,"b1_p",wl,reg)

   # visualise geometry
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(wl)
   v.addAxes(20)
   v.view()

.. note::
   All GDML defines (Constant, Variable, etc) can be used in the construction of other pyg4ometry classes interchangably instead
   of floats or strings

.. warning::
   Avoid redefining defines using basic python types 

Solids 
------

The python geant4 solids match the Geant4 constructors as much possible (different constructor signatures are not supported in python). For example looking at the ``G4Box`` class

.. code-block :: python

   pyg4ometry.geant4.solid.Box(name, pX, pY, pZ, registry, lunit)

.. code-block :: c++

   G4Box(const G4String& pName, G4double  pX, G4double  pY, G4double pZ)

Detector contruction 
--------------------

Materials 
---------

Optical surfaces 
----------------

Registry and GDML output
------------------------

The registry class is a storage class for a complete GDML file. At the
construction stage of almost all objects a registry is required. If the 
object is added to the resistry then it will appear explicitly in the GDML 
output



Visualisation
-------------

Any logical volume ``lv`` can be visualised using 

.. code-block :: python

   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(lv)
   v.addAxes(20)
   v.view()

which will open a Vtk render window. The render window now receives keyboard and mouse commands. 
To exit render window ``q``, to restart interaction with the visualiser 

.. code-block :: python

   v.start()

Overlap checking
----------------




