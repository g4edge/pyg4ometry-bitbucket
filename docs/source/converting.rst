.. _converting:

===================
Converting Geometry
===================



Assembly Conversion
-------------------

It is possible transform a logical volume into an assembly volume. This
is useful in the case of two sources of geometry: placement of top level world
logical volume solids will likely result in an overlap. This effectively removes
the outermost logical volume but keeps the daughters. The produced assembly
volume can then be placed or imprinted somewhere in the geometry.

An assembly **cannot** be used as an outermost 'world' volume for a geometry hierarchy.

Assuming :code:`lv` is a :code:`pyg4ometry.geant4.LogicalVolume` instance:

.. code-block::

   av = lv.assemblyVolume()



GDML to FLUKA
-------------

It is possible convert a pyg4ometry geometry to FLUKA. This is currently a work in
progress and not all Geant4-GDML constructions are implemented, although they can
be quickly added. Given a LV variable named ``logical``

.. code-block :: python
   :linenos:

   import pyg4ometry
   reader = pyg4ometry.gdml.Reader("input.gdml")
   reg = reader.getRegistry()
   logical = reg.getWorldVolume()
   freg = pyg4ometry.convert.geant4Reg2FlukaReg(reg)
   w = pyg4ometry.fluka.Writer()
   w.addDetector(freg)
   w.write("FileName.inp")

If you want to load a file into Flair then a flair file can be written based on ``FileName.inp`` using the following

.. code-block :: python
   :linenos:

    extent = logical.extent(includeBoundingSolid=True)
    f = pyg4ometry.fluka.Flair("FileName.inp",extent)
    f.write("FileName.flair")

Here is an example (viewed in Flair) of a simple Geant G4 solid that has been converted to FLUKA using this
method

.. figure:: tutorials/tutorial8a.png
   :alt: GDML CutTubs

.. figure:: tutorials/tutorial8b.png
   :alt: GDML CutTubs converted to FLUKA

.. note::
   All GDML placements are respected in the conversion from GDML to FLUKA, for both Placements and
   Boolean Solids. So for example a tree of LV-PV placements are reduced into a single transformation
   of a LV into a global coordinate space for FLUKA. A similar process is used for a tree of CSG
   operations.

.. warning::

   Currently there are some things which are not implemented in the conversion. 1) Materials, 2) Scaled solids,
   3) Reflections in placements, 4) Division, replica and parameterised placements. Some of these are straight
   forward to implement, like Materials and the non-Placement physical volumes can be done quickly if a user
   requires it.

FLUKA To GDML
-------------

FLUKA geometry can be converted to GDML using
``pyg4ometry.convert.fluka2geant4``. The conversion process is robust and
supports all FLUKA geometry constructs.  Given a FLUKA file `model.inp`,
the following code can be used to translate it to a GDML file.

.. code-block :: python
   :linenos:

   import pyg4ometry.fluka as fluka
   import pyg4ometry.gdml as gdml
   from pyg4ometry.convert import fluka2Geant4

   # Read the FLUKA file, get the FlukaRegistry, convert the registry to a
   # Geant4 Registry
   reader = fluka.Reader("model.inp")
   flukaregistry = reader.flukaregistry
   geant4Registry = fluka2Geant4(flukaRegistry)

   worldLogicalVolume = geant4Registry.getWorldVolume()
   worldLogicalVolume.clipSolid()

   writer = gdml.Writer()
   writer.addDetector(geant4Registry)
   writer.write("model.gdml")

The core of this functionality is the translation of the `FlukaRegistry`
instance into the equivalent `Registry` (i.e. Geant4) instance.

Here is an example of a model viewed in flair and the resulting visualisation
in VTK of the Geant4 model

.. figure:: tutorials/faradayCupFlair.png
   :alt: A faraday cup designed and viewed in flair

.. figure:: tutorials/faradayCupVTK.png
   :alt: A faraday cup converted from FLAIR to Geant4 and shown in VTK


A number of keyword arguments are available to further modify the
conversion.  The `fluka2Geant4` keyword arguments `region` and
`omitRegions` allow the user to select a subset of the named regions to be
translated.

The conversion of QUA bodies (fluka2geant4 kwarg `quadricRegionAABBs`) is
complex and requires further explanation. In Pyg4ometry the mesh and GDML
representations of FLUKA infinite circular cylinders, elliptical cylinders
and half-spaces are all finite (but very large) cylinders, elliptical
cylinders and boxes.  This is robust as increasing the length of cylinders
and depth/breadth of boxes does not increase the number of polygons used in
the underlying mesh representation for that solid.  However, this is not
true of the quadric surface.  A quadric surface cannot simply be generated
to be "very large", as the number of polygons will grow quickly, along with
the memory consumption and facets in the resulting GDML TesselatedSolid,
which will also slowing down tracking time in Geant4.  For this reason the
user must provide axis-aligned bounding boxes of the regions where any QUA
bodies are present.  It is recommended that these boxes be a centimetre
larger than formally necessary to ensure a correct conversion.  Providing
the bounding box ensures that an efficient and accurate mesh of the QUA
bodies can be generated meaning that the conversion to be performed in a
tractable amount of time as well giving more performant tracking in Geant4.

CAD (STEP/IGES) To GDML
-----------------------

The conersion from CAD (STEP) to GDML uses OpenCascade to read, interrogate 
and tesselate the geometry. A CAD file might have a significant number of parts and assemblies. This naturally lends itself to the logical and physical volume structure 
of Geant4/GDML. Often the entire CAD file does not need to be converted, only
a sub-assembly. To determine what the stucture of the CAD file is the following commands
can be called, creation of a CAD reader and dumping to the terminal the structure 
of the CAD file.  


.. code-block :: python 
    
    r = _pyg4.pyoce.Reader("1_BasicSolids_Bodies.step")
    r.shapeTool.Dump()

This particular example with have the following output 


.. code-block :: console 

      XCAFDoc_ShapeTool Trans. 0; Valid;  ID = efd212ee-6dfd-11d4-b9c8-0060b0ee281b

   PART COMPOUND 0:1:1:1 "1_BasicSolids_Bodies v2" 
      SOLID 0:1:1:1:1
      SOLID 0:1:1:1:2
      SOLID 0:1:1:1:3
      SOLID 0:1:1:1:4
      SOLID 0:1:1:1:5


   Free Shapes: 1
   PART COMPOUND  0:1:1:1 "1_BasicSolids_Bodies v2" 


This example is 5 basic solids. So they are stored as a COMPOUND 0:1:1:1 and each SOLID is labelled 0:1:1:1:(1,2,3,4,5). Elements of the file do not need to have a name, it is more helpful to the user if they do. To convert a CAD model or a sub-assembly of a model the label is required. So a geant4 pyg4ometry registry can be created by calling.  

.. code-block :: python

   reg = pyg4ometry.convert.oce2Geant4(r.shapeTool,"1_BasicSolids_Bodies v2")

It is also possible to call with the numerical tag, so 

.. code-block :: python 

   reg = pyg4ometry.convert.oce2Geant4(r.shapeTool,"0:1:1:1")


Either way of accessing a particular SOLID, COMPOUND or ASSEMBLY. Once created the registry can be written as described in the Exporting Geometry section. So putting it all together


.. code-block :: python 
    
   r = _pyg4.pyoce.Reader("1_BasicSolids_Bodies.step")
   reg = pyg4ometry.convert.oce2Geant4(r.shapeTool,"1_BasicSolids_Bodies v2")
   w = p4gometry.gdml.Writer()
   w.addDetector(reg)
   w.write('1_BasicSolids_Bodies.gdml')






