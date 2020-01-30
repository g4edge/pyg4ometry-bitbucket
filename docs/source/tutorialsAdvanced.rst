==================
Advanced tutorials
==================

Edit existing geometry
----------------------

After loading some geometry it is possible to modify the memory resident geometry.
This could adjusting the parameter of a given solid or PV, or replacing entirely the
type of solid used for an LV.

Complex geometry builder
------------------------

Having access to geometry contruction in python allows the rapid contruction of 
geometry using functions which return an appropriate LV. Examples of this available in 
``pyg4ometry/pyg4ometry/test/pythonCompoundExamples``

Fluka geometry scripting
------------------------

In a very similar way to geant4 geometry authoring it is possible to 
use pyg4ometry to create fluka output. To create a simple region consisting 
of a single body

.. code-block :: python
   :linenos:

   import pyg4ometry.convert as convert
   import pyg4ometry.visualisation as vi
   from pyg4ometry.fluka import RPP, Region, Zone, FlukaRegistry

   freg = FlukaRegistry()

   rpp = RPP("RPP_BODY", 0, 10, 0, 10, 0, 10, flukaregistry=freg)
   z = Zone()
   z.addIntersection(rpp)
   region = Region("RPP_REG", material="COPPER")
   region.addZone(z)
   freg.addRegion(region)

   greg = convert.fluka2Geant4(freg)
   greg.getWorldVolume().clipSolid()

   v = vi.VtkViewer()
   v.addAxes(length=20)
   v.addLogicalVolume(greg.getWorldVolume())
   v.view()


Export scene to unity/unreal
----------------------------

The quickest way to get gemetry to Unity/Unreal is to use a standard asset 
format. This takes a vtkRenderer and creates a OBJ file. The vtkRenderer 
managed within pyg4ometry from the vtkViwer class, once a geometry is created
(either from any source) then an OBJ file can be created. Taking the example in ``pyg4ometry/pyg4ometry/test/pythonCompoundExamples/``

.. code-block :: python
   :linenos:

   import pyg4ometry
   r = pyg4ometry.gdml.Reader("./Chamber.gdml")
   l = r.getRegistry().getWorldVolume()
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(l)
   v.exportOBJScene("Chamber")

``obj`` files are written ``Chamber.obj`` and ``Chamber.mtl``.

For a Fluka file, first it must be converted to geant4 and then the same process should be followed.

.. code-block :: python
   :linenos:

   import pyg4ometry
   r = pyg4ometry.fluka.Reader("./Chamber.inp")
   greg = pyg4ometry.convert.fluka2geant4(r.getRegistry())
   l = greg.getWorldVolume()
   v = pyg4ometry.visualisation.VtkViewer()
   v.addLogicalVolume(l)
   v.exportOBJScene("Chamber")

As the meshing might need to changed for the visualisation application, 
the parameters for the meshing for each solid might need to changed. 