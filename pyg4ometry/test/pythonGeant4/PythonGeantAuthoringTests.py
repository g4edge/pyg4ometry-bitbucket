import unittest as _unittest
import testtools as _testtools
import numpy as _np

import pyg4ometry

from . import T000_SolidBase
from . import T001_Box
from . import T002_Tubs
from . import T003_CutTubs
from . import T0031_CutTubs_number
from . import T0032_CutTubs_string
from . import T0033_CutTubs_expression
from . import T0034_CutTubs_DefineTree
from . import T004_Cons
from . import T005_Para
from . import T006_Trd
from . import T007_Trap
from . import T008_Sphere
from . import T009_Orb
from . import T010_Torus
from . import T011_Polycone
from . import T012_GenericPolycone
from . import T013_Polyhedra
from . import T014_GenericPolyhedra
from . import T015_EllipticalTube
from . import T016_Ellipsoid
from . import T017_EllipticalCone
from . import T018_Paraboloid
from . import T019_Hyperboloid
from . import T020_Tet
from . import T021_ExtrudedSolid
from . import T022_TwistedBox
from . import T023_TwistedTrap
from . import T024_TwistedTrd
from . import T025_TwistedTubs
from . import T026_GenericTrap
from . import T028_Union
from . import T029_Subtraction
from . import T030_Intersection
from . import T031_MultiUnion
from . import T032_Scaled
from . import T033_TessellatedSolid
from . import T101_physical_logical
from . import T102_overlap_none
from . import T103_overlap_copl
from . import T104_overlap_volu
from . import T105_assembly
from . import T106_replica_x
from . import T107_replica_y
from . import T108_replica_z
from . import T109_replica_phi
from . import T110_replica_rho
from . import T111_parameterised_box
from . import T112_parameterised_tube
from . import T201_Materials
from . import T202_OpticalSurface
from . import T203_MaterialsRegistry
from . import T204_NIST_Element
from . import T205_NIST_Material
from . import T300_overlap_assembly_regular_lv
from . import T301_overlap_assembly_none
from . import T302_overlap_assembly_coplanar
from . import T303_overlap_assembly_daughter_collision
from . import T304_overlap_assembly_volumetric
from . import T305_overlap_assembly_nested
from . import T306_overlap_replica_x
from . import T307_overlap_replica_x_internal
from . import T400_MergeRegistry
from . import T401_MergeRegistry_Box
from . import T402_MergeRegistry_Tubs
from . import T403_MergeRegistry_CutTubs
from . import T404_MergeRegistry_Cons
from . import T405_MergeRegistry_Para
from . import T406_MergeRegistry_Trd
from . import T407_MergeRegistry_Trap
from . import T408_MergeRegistry_Sphere
from . import T409_MergeRegistry_Orb
from . import T410_MergeRegistry_Torus
from . import T411_MergeRegistry_Polycone
from . import T412_MergeRegistry_GenericPolycone
from . import T413_MergeRegistry_Polyhedra
from . import T414_MergeRegistry_GenericPolyhedra
from . import T415_MergeRegistry_EllipticalTube
from . import T416_MergeRegistry_Ellipoid
from . import T417_MergeRegistry_EllipticalCone
from . import T418_MergeRegistry_Paraboloid
from . import T419_MergeRegistry_Hyperboloid
from . import T420_MergeRegistry_Tet
from . import T421_MergeRegistry_ExtrudedSolid
from . import T422_MergeRegistry_TwistedBox
from . import T423_MergeRegistry_TwistedTrap
from . import T424_MergeRegistry_TwistedTrd
from . import T425_MergeRegistry_TwistedTubs
from . import T426_MergeRegistry_GenericTrap
from . import T428_MergeRegistry_Union
from . import T429_MergeRegistry_Subtraction
from . import T430_MergeRegistry_Intersection
from . import T431_MergeRegistry_MultiUnion
from . import T432_MergeRegistry_Box_AssemblyConversion
from . import T433_MergeRegistry_Scale

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonGeantAuthoringTests(_unittest.TestCase) :
    def test_PythonGeant_Plane(self) :
        p = pyg4ometry.geant4.solid.Plane("plane",[0,0,1],1000)
        str(p)

    def test_PythonGeant_Wedge(self) :
        w = pyg4ometry.geant4.solid.Wedge("wedge",1000,0,1.5*_np.pi,10000)
        str(w)

    def test_PythonGeant_T000_SolidBase(self) :
        self.assertTrue(T000_SolidBase.Test()["testStatus"])

    def test_PythonGeant_T001_Box(self) :
        self.assertTrue(T001_Box.Test(False,False)["testStatus"])

    def test_PythonGeant_T002_Tubs(self) :
        self.assertTrue(T002_Tubs.Test(False,False))

    def test_PythonGeant_T003_CutTubs(self) :
        self.assertTrue(T003_CutTubs.Test(False, False, T003_CutTubs.normal)["testStatus"])
        self.assertTrue(T003_CutTubs.Test(False, False, T003_CutTubs.flat_ends)["testStatus"])
        self.assertTrue(T0031_CutTubs_number.Test(False, False)["testStatus"])
        self.assertTrue(T0032_CutTubs_string.Test(False, False)["testStatus"])
        self.assertTrue(T0033_CutTubs_expression.Test(False, False)["testStatus"])
        self.assertTrue(T0034_CutTubs_DefineTree.Test(False,False)["testStatus"])

    def test_PythonGeant_T004_Cons(self) :
        try :
            self.assertTrue(T004_Cons.Test(False,False,T004_Cons.r1min_gt_r1max)["testStatus"])
        except ValueError :
            pass

        try : 
            self.assertTrue(T004_Cons.Test(False,False,T004_Cons.r2min_gt_r2max)["testStatus"])
        except ValueError : 
            pass

        try : 
            self.assertTrue(T004_Cons.Test(False,False,T004_Cons.dphi_gt_2pi)["testStatus"])
        except ValueError : 
            pass

        self.assertTrue(T004_Cons.Test(False,False,T004_Cons.dphi_eq_2pi)["testStatus"])
        self.assertTrue(T004_Cons.Test(False,False,T004_Cons.cone_up)["testStatus"])
        self.assertTrue(T004_Cons.Test(False,False,T004_Cons.inner_cylinder)["testStatus"])

        self.assertTrue(T004_Cons.Test(False,False)["testStatus"])
      
    def test_PythonGeant_T005_Para(self) :
        self.assertTrue(T005_Para.Test(False,False)["testStatus"])

    def test_PythonGeant_T006_Trd(self) :
        self.assertTrue(T006_Trd.Test(False,False)["testStatus"])

    def test_PythonGeant_T007_Trap(self) :
        self.assertTrue(T007_Trap.Test(False,False)["testStatus"])

    def test_PythonGeant_T008_Sphere(self) :
        self.assertTrue(T008_Sphere.Test(False,False))

    def test_PythonGeant_T009_Orb(self) :
        self.assertTrue(T009_Orb.Test(False,False))

    def test_PythonGeant_T010_Torus(self) :
        self.assertTrue(T010_Torus.Test(False,False))

    def test_PythonGeant_T011_Polycone(self) :
        self.assertTrue(T011_Polycone.Test(False,False))

    def test_PythonGeant_T012_GenericPolycone(self) :
        self.assertTrue(T012_GenericPolycone.Test(False,False,T012_GenericPolycone.normal))

        try : 
            T012_GenericPolycone.Test(False,False,T012_GenericPolycone.two_planes)
        except ValueError : 
            pass

    def test_PythonGeant_T013_Polyhedra(self) :
        self.assertTrue(T013_Polyhedra.Test())

    def test_PythonGeant_T014_GenericPolyhedra(self) :
        self.assertTrue(T014_GenericPolyhedra.Test(False,False,T014_GenericPolyhedra.normal))

        try : 
            T014_GenericPolyhedra.Test(False,False, T014_GenericPolyhedra.two_planes)
        except ValueError : 
            pass

    def test_PythonGeant_T015_EllipticalTube(self) :
        self.assertTrue(T015_EllipticalTube.Test())

    def test_PythonGeant_T016_Ellipsoid(self) :
        self.assertTrue(T016_Ellipsoid.Test())

    def test_PythonGeant_T017_EllipticalCone(self) :
        self.assertTrue(T017_EllipticalCone.Test())
        
        try : 
            T017_EllipticalCone.Test(False,False, T017_EllipticalCone.zcut_outofrange)
        except ValueError : 
            pass

    def test_PythonGeant_T018_Paraboloid(self) :
        self.assertTrue(T018_Paraboloid.Test())

    def test_PythonGeant_T019_Hyperboloid(self) :
        self.assertTrue(T019_Hyperboloid.Test(False,False,T019_Hyperboloid.normal))
        self.assertTrue(T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_eq_zero))

        try : 
            T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_gt_rmax)
        except ValueError : 
            pass

    def test_PythonGeant_T020_Tet(self) :
        self.assertTrue(T020_Tet.Test())        

    def test_PythonGeant_T021_ExtrudedSolid(self) :
        self.assertTrue(T021_ExtrudedSolid.Test())        

    def test_PythonGeant_T022_TwistedBox(self) :
        self.assertTrue(T022_TwistedBox.Test())

    def test_PythonGeant_T023_TwistedTrap(self) :
        self.assertTrue(T023_TwistedTrap.Test())

    def test_PythonGeant_T024_TwistedTrd(self) :
        self.assertTrue(T024_TwistedTrd.Test())

    def test_PythonGeant_T025_TwistedTubs(self) :
        self.assertTrue(T025_TwistedTubs.Test())

    def test_PythonGeant_T026_GenericTrap(self) :
        self.assertTrue(T026_GenericTrap.Test())

    def test_PythonGeant_T028_Union(self) :
        self.assertTrue(T028_Union.Test(False,False,False)["testStatus"])
        self.assertTrue(T028_Union.Test(False,False,True)["testStatus"])

    def test_PythonGeant_T029_Subtraction(self) :
        self.assertTrue(T029_Subtraction.Test(False,False,False)["testStatus"])

        #try :
        #    T029_Subtraction.Test(False,False,True)
        #except pyg4ometry.exceptions.NullMeshError :
        #    pass

    def test_PythonGeant_T030_Intersection(self) :
        self.assertTrue(T030_Intersection.Test(False,False,T030_Intersection.normal))

        #try :
        #    T030_Intersection.Test(False,False,T030_Intersection.non_intersecting)
        #except pyg4ometry.exceptions.NullMeshError :
        #    pass

    def test_PythonGeant_T031_MultiUnion(self) :
        self.assertTrue(T031_MultiUnion.Test())

    def test_PythonGeant_T032_Scaled(self):
        self.assertTrue(T032_Scaled.Test()["testStatus"])

    def test_PythonGeant_T033_Tessellated(self):
        self.assertTrue(T033_TessellatedSolid.Test()["testStatus"])

    def test_PythonGeant_T101_PhysicalLogical(self):
        self.assertTrue(T101_physical_logical.Test()["testStatus"])

    def test_PythonGeant_T102_OverlapMone(self):
        self.assertTrue(T102_overlap_none.Test()["testStatus"])

    def test_PythonGeant_T103_OverlapCopl(self):
        self.assertTrue(T103_overlap_copl.Test()["testStatus"])

    def test_PythonGeant_T104_OverlapVolu(self):
        self.assertTrue(T104_overlap_volu.Test()["testStatus"])

    def test_PythonGeant_T105_Assembly(self):
        self.assertTrue(T105_assembly.Test()["testStatus"])

    def test_PythonGeant_T106_ReplicaX(self):
        self.assertTrue(T106_replica_x.Test()["testStatus"])

    def test_PythonGeant_T107_ReplicaY(self):
        self.assertTrue(T107_replica_y.Test()["testStatus"])

    def test_PythonGeant_T108_ReplicaZ(self):
        self.assertTrue(T108_replica_z.Test()["testStatus"])

    def test_PythonGeant_T109_ReplicaPhi(self):
        self.assertTrue(T109_replica_phi.Test()["testStatus"])

    def test_PythonGeant_T110_ReplicaRho(self):
        self.assertTrue(T110_replica_rho.Test()["testStatus"])

    def test_PythonGeant_T111_parameterised_box(self):
        self.assertTrue(T111_parameterised_box.Test()["testStatus"])

    def test_PythonGeant_T112_parameterised_tube(self):
        self.assertTrue(T112_parameterised_tube.Test()["testStatus"])

    def test_PythonGeant_T201_Materials(self):
        T201_Materials.Test_MaterialPredefined()
        T201_Materials.Test_MaterialSingleElement()
        T201_Materials.Test_MaterialCompoundMassFraction()
        T201_Materials.Test_MaterialCompoundAtoms()
        T201_Materials.Test_MaterialMixture()
        T201_Materials.Test_MaterialIsotopes()

    def test_PythonGeant_T202_OpticalSurface(self):
        T202_OpticalSurface.Test_OpticalSurface()

    def test_PythonGeant_T203_MaterialsRegistry(self):
        T203_MaterialsRegistry.Test_MaterialsRegistry()

    def test_PythonGeant_T204_NIST_Element(self):
        T204_NIST_Element.Test_NIST_Element()

    def test_PythonGeant_T205_NIST_Material(self):
        T205_NIST_Material.Test_NIST_Material()

    def test_PythonGeant_T400_MergeRegistry(self):
        self.assertTrue(T400_MergeRegistry.Test())

    def test_PythonGeant_T401_MergeRegistry_Box(self):
        self.assertTrue(T401_MergeRegistry_Box.Test(False,False)["testStatus"])

    def test_PythonGeant_T402_MergeRegistry_Tubs(self):
        self.assertTrue(T402_MergeRegistry_Tubs.Test()["testStatus"])

    def test_PythonGeant_T403_MergeRegistry_CutTubs(self):
        self.assertTrue(T403_MergeRegistry_CutTubs.Test()["testStatus"])

    def test_PythonGeant_T404_MergeRegistry_Cons(self):
        self.assertTrue(T404_MergeRegistry_Cons.Test()["testStatus"])

    def test_PythonGeant_T405_MergeRegistry_Para(self):
        self.assertTrue(T405_MergeRegistry_Para.Test()["testStatus"])

    def test_PythonGeant_T406_MergeRegistry_Trd(self):
        self.assertTrue(T406_MergeRegistry_Trd.Test()["testStatus"])

    def test_PythonGeant_T407_MergeRegistry_Trap(self):
        self.assertTrue(T407_MergeRegistry_Trap.Test()["testStatus"])

    def test_PythonGeant_T408_MergeRegistry_Sphere(self):
        self.assertTrue(T408_MergeRegistry_Sphere.Test()["testStatus"])

    def test_PythonGeant_T409_MergeRegistry_Orb(self):
        self.assertTrue(T409_MergeRegistry_Orb.Test()["testStatus"])

    def test_PythonGeant_T410_MergeRegistry_Torus(self):
        self.assertTrue(T410_MergeRegistry_Torus.Test()["testStatus"])

    def test_PythonGeant_T411_MergeRegistry_Polycone(self):
        self.assertTrue(T411_MergeRegistry_Polycone.Test()["testStatus"])

    def test_PythonGeant_T412_MergeRegistry_GenericPolycone(self):
        self.assertTrue(T412_MergeRegistry_GenericPolycone.Test()["testStatus"])

    def test_PythonGeant_T413_MergeRegistry_Polyhedra(self):
        self.assertTrue(T413_MergeRegistry_Polyhedra.Test()["testStatus"])

    def test_PythonGeant_T414_MergeRegistry_GenericPolyhedra(self):
        self.assertTrue(T414_MergeRegistry_GenericPolyhedra.Test()["testStatus"])

    def test_PythonGeant_T415_MergeRegistry_EllipticalTube(self):
        self.assertTrue(T415_MergeRegistry_EllipticalTube.Test()["testStatus"])

    def test_PythonGeant_T416_MergeRegistry_Ellipsoid(self):
        self.assertTrue(T416_MergeRegistry_Ellipoid.Test()["testStatus"])

    def test_PythonGeant_T417_MergeRegistry_EllipticalCone(self):
        self.assertTrue(T417_MergeRegistry_EllipticalCone.Test()["testStatus"])

    def test_PythonGeant_T418_MergeRegistry_EllipticalParaboloid(self):
        self.assertTrue(T418_MergeRegistry_Paraboloid.Test()["testStatus"])

    def test_PythonGeant_T419_MergeRegistry_Hyperboloid(self):
        self.assertTrue(T419_MergeRegistry_Hyperboloid.Test()["testStatus"])

    def test_PythonGeant_T420_MergeRegistry_Tet(self):
        self.assertTrue(T420_MergeRegistry_Tet.Test()["testStatus"])

    def test_PythonGeant_T421_MergeRegistry_ExtrudedSolid(self):
        self.assertTrue(T421_MergeRegistry_ExtrudedSolid.Test()["testStatus"])

    def test_PythonGeant_T422_MergeRegistry_TwistedBox(self):
        self.assertTrue(T422_MergeRegistry_TwistedBox.Test()["testStatus"])

    def test_PythonGeant_T423_MergeRegistry_TwistedTrap(self):
        self.assertTrue(T423_MergeRegistry_TwistedTrap.Test()["testStatus"])

    def test_PythonGeant_T424_MergeRegistry_TwistedTrd(self):
        self.assertTrue(T424_MergeRegistry_TwistedTrd.Test()["testStatus"])

    def test_PythonGeant_T425_MergeRegistry_TwistedTubs(self):
        self.assertTrue(T425_MergeRegistry_TwistedTubs.Test()["testStatus"])

    def test_PythonGeant_T426_MergeRegistry_GenericTrap(self):
        self.assertTrue(T426_MergeRegistry_GenericTrap.Test()["testStatus"])

    def test_PythonGeant_T428_MergeRegistry_Union(self):
        self.assertTrue(T428_MergeRegistry_Union.Test()["testStatus"])

    def test_PythonGeant_T429_MergeRegistry_Subtraction(self):
        self.assertTrue(T429_MergeRegistry_Subtraction.Test()["testStatus"])

    def test_PythonGeant_T430_MergeRegistry_Intersection(self):
        self.assertTrue(T430_MergeRegistry_Intersection.Test()["testStatus"])

    def test_PythonGeant_T431_MergeRegistry_MultiUnion(self):
        self.assertTrue(T431_MergeRegistry_MultiUnion.Test()["testStatus"])

    def test_PythonGeant_T432_MergeRegistryBoxAssemblyConverion(self):
        self.assertTrue(T432_MergeRegistry_Box_AssemblyConversion.Test()["testStatus"])

    def test_PythonGeant_T433_MergeRegistry_Scale(self):
        self.assertTrue(T433_MergeRegistry_Scale.Test()["testStatus"])

if __name__ == '__main__':
    _unittest.main(verbosity=2)

    class TracingStreamResult(_testtools.StreamResult):
        def status(self, *args, **kwargs):
            print('{0[test_id]}: {0[test_status]}'.format(kwargs))
