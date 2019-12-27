import unittest as _unittest
import testtools as _testtools
import numpy as _np

import pyg4ometry

import T000_SolidBase
import T001_Box
import T002_Tubs
import T003_CutTubs
import T0031_CutTubs_number
import T0032_CutTubs_string
import T0033_CutTubs_expression
import T0034_CutTubs_DefineTree
import T004_Cons
import T005_Para
import T006_Trd
import T007_Trap
import T008_Sphere
import T009_Orb
import T010_Torus
import T011_Polycone
import T012_GenericPolycone
import T013_Polyhedra
import T014_GenericPolyhedra
import T015_EllipticalTube
import T016_Ellipsoid
import T017_EllipticalCone
import T018_Paraboloid
import T019_Hyperboloid
import T020_Tet
import T021_ExtrudedSolid
import T022_TwistedBox
import T023_TwistedTrap
import T024_TwistedTrd
import T025_TwistedTubs
import T026_GenericTrap

import T028_Union
import T029_Subtraction
import T030_Intersection
import T031_MultiUnion
import T032_Scaled

import T101_physical_logical
import T102_overlap_none
import T103_overlap_copl
import T104_overlap_volu
import T105_assembly
import T106_replica_x
import T107_replica_y
import T108_replica_z
import T109_replica_phi
import T110_replica_rho
import T111_DefineTree

import T400_MergeRegistry
import T401_MergeRegistry_Box
import T402_MergeRegistry_Tubs
import T403_MergeRegistry_CutTubs
import T404_MergeRegistry_Cons
import T405_MergeRegistry_Para
import T406_MergeRegistry_Trd
import T407_MergeRegistry_Trap
import T408_MergeRegistry_Sphere
import T409_MergeRegistry_Orb
import T410_MergeRegistry_Torus
import T411_MergeRegistry_Polycone
import T412_MergeRegistry_GenericPolycone
import T413_MergeRegistry_Polyhedra
import T414_MergeRegistry_GenericPolyhedra
import T415_MergeRegistry_EllipticalTube
import T416_MergeRegistry_Ellipoid
import T417_MergeRegistry_EllipticalCone
import T418_MergeRegistry_Paraboloid
import T419_MergeRegistry_Hyperboloid
import T420_MergeRegistry_Tet
import T421_MergeRegistry_ExtrudedSolid
import T422_MergeRegistry_TwistedBox
import T423_MergeRegistry_TwistedTrap
import T424_MergeRegistry_TwistedTrd
import T425_MergeRegistry_TwistedTubs
import T426_MergeRegistry_GenericTrap
import T428_MergeRegistry_Union
import T429_MergeRegistry_Subtraction
import T430_MergeRegistry_Intersection
import T431_MergeRegistry_MultiUnion
import T432_MergeRegistry_Box_AssemblyConversion

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

    def test_PythonGeant_SolidBase(self) :
        self.assertTrue(T000_SolidBase.Test()["testStatus"])

    def test_PythonGeant_Box(self) :
        self.assertTrue(T001_Box.Test(True,False)["testStatus"])

    def test_PythonGeant_Tubs(self) :
        self.assertTrue(T002_Tubs.Test(True,False))

    def test_PythonGeant_CutTubs(self) :
        self.assertTrue(T003_CutTubs.Test(True, False, T003_CutTubs.normal)["testStatus"])
        self.assertTrue(T003_CutTubs.Test(True, False, T003_CutTubs.flat_ends)["testStatus"])
        self.assertTrue(T0031_CutTubs_number.Test(True, False)["testStatus"])
        self.assertTrue(T0032_CutTubs_string.Test(True, False)["testStatus"])
        self.assertTrue(T0033_CutTubs_expression.Test(True, False)["testStatus"])
        self.assertTrue(T0034_CutTubs_DefineTree.Test(True,False)["testStatus"])

    def test_PythonGeant_Cons(self) :
        try :
            self.assertTrue(T004_Cons.Test(True,False,T004_Cons.r1min_gt_r1max)["testStatus"])
        except ValueError :
            pass

        try : 
            self.assertTrue(T004_Cons.Test(True,False,T004_Cons.r2min_gt_r2max)["testStatus"])
        except ValueError : 
            pass

        try : 
            self.assertTrue(T004_Cons.Test(True,False,T004_Cons.dphi_gt_2pi)["testStatus"])
        except ValueError : 
            pass

        self.assertTrue(T004_Cons.Test(True,False,T004_Cons.dphi_eq_2pi)["testStatus"])
        self.assertTrue(T004_Cons.Test(True,False,T004_Cons.cone_up)["testStatus"])
        self.assertTrue(T004_Cons.Test(True,False,T004_Cons.inner_cylinder)["testStatus"])

        self.assertTrue(T004_Cons.Test(True,False)["testStatus"])
      
    def test_PythonGeant_Para(self) :
        self.assertTrue(T005_Para.Test(True,False)["testStatus"])

    def test_PythonGeant_Trd(self) :
        self.assertTrue(T006_Trd.Test(True,False)["testStatus"])

    def test_PythonGeant_Trap(self) :
        self.assertTrue(T007_Trap.Test(True,False)["testStatus"])

    def test_PythonGeant_Sphere(self) :
        self.assertTrue(T008_Sphere.Test())

    def test_PythonGeant_Orb(self) :
        self.assertTrue(T009_Orb.Test())

    def test_PythonGeant_Torus(self) :
        self.assertTrue(T010_Torus.Test())

    def test_PythonGeant_Polycone(self) :
        self.assertTrue(T011_Polycone.Test())

    def test_PythonGeant_GenericPolycone(self) :
        self.assertTrue(T012_GenericPolycone.Test(False,False,T012_GenericPolycone.normal))

        try : 
            T012_GenericPolycone.Test(False,False,T012_GenericPolycone.two_planes)
        except ValueError : 
            pass

    def test_PythonGeant_Polyhedra(self) :
        self.assertTrue(T013_Polyhedra.Test())

    def test_PythonGeant_GenericPolyhedra(self) :
        self.assertTrue(T014_GenericPolyhedra.Test(False,False,T014_GenericPolyhedra.normal))

        try : 
            T014_GenericPolyhedra.Test(False,False, T014_GenericPolyhedra.two_planes)
        except ValueError : 
            pass

    def test_PythonGeant_EllipticalTube(self) :
        self.assertTrue(T015_EllipticalTube.Test())

    def test_PythonGeant_Ellipsoid(self) :
        self.assertTrue(T016_Ellipsoid.Test())

    def test_PythonGeant_EllipticalCone(self) :
        self.assertTrue(T017_EllipticalCone.Test())
        
        try : 
            T017_EllipticalCone.Test(False,False, T017_EllipticalCone.zcut_outofrange)
        except ValueError : 
            pass

    def test_PythonGeant_Paraboloid(self) :
        self.assertTrue(T018_Paraboloid.Test())

    def test_PythonGeant_Hyperboloid(self) :
        self.assertTrue(T019_Hyperboloid.Test(False,False,T019_Hyperboloid.normal))
        self.assertTrue(T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_eq_zero))

        try : 
            T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_gt_rmax)
        except ValueError : 
            pass

    def test_PythonGeant_Tet(self) :
        self.assertTrue(T020_Tet.Test())        

    def test_PythonGeant_ExtrudedSolid(self) :
        self.assertTrue(T021_ExtrudedSolid.Test())        

    def test_PythonGeant_TwistedBox(self) :
        self.assertTrue(T022_TwistedBox.Test())

    def test_PythonGeant_TwistedTrap(self) :
        self.assertTrue(T023_TwistedTrap.Test())

    def test_PythonGeant_TwistedTrd(self) :
        self.assertTrue(T024_TwistedTrd.Test())

    def test_PythonGeant_TwistedTubs(self) :
        self.assertTrue(T025_TwistedTubs.Test())

    def test_PythonGeant_GenericTrap(self) :
        self.assertTrue(T026_GenericTrap.Test())

    def test_PythonGeant_Union(self) :
        self.assertTrue(T028_Union.Test(True,False,False)["testStatus"])
        self.assertTrue(T028_Union.Test(True,False,True)["testStatus"])

    def test_PythonGeant_Subtraction(self) :
        self.assertTrue(T029_Subtraction.Test(True,False,False)["testStatus"])

        try :
            T029_Subtraction.Test(True,False,True)
        except pyg4ometry.exceptions.NullMeshError :
            pass

    def test_PythonGeant_Intersection(self) :
        self.assertTrue(T030_Intersection.Test(False,False,T030_Intersection.normal))

        try : 
            T030_Intersection.Test(False,False,T030_Intersection.non_intersecting)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def test_PythonGeant_MultiUnion(self) :
        self.assertTrue(T031_MultiUnion.Test())

    def test_PythonGeant_Scaled(self):
        self.assertTrue(T032_Scaled.Test()["testStatus"])

    def test_PythonGeant_PhysicalLogical(self):
        self.assertTrue(T101_physical_logical.Test()["testStatus"])

    def test_PythonGeant_OverlapMone(self):
        self.assertTrue(T102_overlap_none.Test()["testStatus"])

    def test_PythonGeant_OverlapCopl(self):
        self.assertTrue(T103_overlap_copl.Test()["testStatus"])

    def test_PythonGeant_OverlapVolu(self):
        self.assertTrue(T104_overlap_volu.Test()["testStatus"])

    def test_PythonGeant_Assembly(self):
        self.assertTrue(T105_assembly.Test()["testStatus"])

    def test_PythonGeant_ReplicaX(self):
        self.assertTrue(T106_replica_x.Test()["testStatus"])

    def test_PythonGeant_ReplicaY(self):
        self.assertTrue(T107_replica_y.Test()["testStatus"])

    def test_PythonGeant_ReplicaZ(self):
        self.assertTrue(T108_replica_z.Test()["testStatus"])

    def test_PythonGeant_ReplicaPhi(self):
        self.assertTrue(T109_replica_phi.Test()["testStatus"])

    def test_PythonGeant_ReplicaRho(self):
        self.assertTrue(T110_replica_rho.Test()["testStatus"])

    def test_PythonGeant_DefineTree(self):
        self.assertTrue(T111_DefineTree.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry(self):
        self.assertTrue(T400_MergeRegistry.Test())

    def test_PythonGeant_MergeRegistry_Box(self):
        self.assertTrue(T401_MergeRegistry_Box.Test(False,False)["testStatus"])

    def test_PythonGeant_MergeRegistry_Tubs(self):
        self.assertTrue(T402_MergeRegistry_Tubs.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_CutTubs(self):
        self.assertTrue(T403_MergeRegistry_CutTubs.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Cons(self):
        self.assertTrue(T404_MergeRegistry_Cons.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Para(self):
        self.assertTrue(T405_MergeRegistry_Para.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Trd(self):
        self.assertTrue(T406_MergeRegistry_Trd.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Trap(self):
        self.assertTrue(T407_MergeRegistry_Trap.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_(self):
        self.assertTrue(T407_MergeRegistry_Trap.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Sphere(self):
        self.assertTrue(T408_MergeRegistry_Sphere.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Orb(self):
        self.assertTrue(T409_MergeRegistry_Orb.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Torus(self):
        self.assertTrue(T410_MergeRegistry_Torus.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Polycone(self):
        self.assertTrue(T411_MergeRegistry_Polycone.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_GenericPolycone(self):
        self.assertTrue(T412_MergeRegistry_GenericPolycone.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Polyhedra(self):
        self.assertTrue(T413_MergeRegistry_Polyhedra.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_GenericPolyhedra(self):
        self.assertTrue(T414_MergeRegistry_GenericPolyhedra.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_GenericPolyhedra(self):
        self.assertTrue(T414_MergeRegistry_GenericPolyhedra.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_EllipticalTube(self):
        self.assertTrue(T415_MergeRegistry_EllipticalTube.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Ellipsoid(self):
        self.assertTrue(T416_MergeRegistry_Ellipoid.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_EllipticalCone(self):
        self.assertTrue(T417_MergeRegistry_EllipticalCone.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_EllipticalParaboloid(self):
        self.assertTrue(T418_MergeRegistry_Paraboloid.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Hyperboloid(self):
        self.assertTrue(T419_MergeRegistry_Hyperboloid.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Tet(self):
        self.assertTrue(T420_MergeRegistry_Tet.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_ExtrudedSolid(self):
        self.assertTrue(T421_MergeRegistry_ExtrudedSolid.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_TwistedBox(self):
        self.assertTrue(T422_MergeRegistry_TwistedBox.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_TwistedTrap(self):
        self.assertTrue(T423_MergeRegistry_TwistedTrap.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_TwistedTrd(self):
        self.assertTrue(T424_MergeRegistry_TwistedTrd.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_TwistedTubs(self):
        self.assertTrue(T425_MergeRegistry_TwistedTubs.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_GenericTrap(self):
        self.assertTrue(T426_MergeRegistry_GenericTrap.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Union(self):
        self.assertTrue(T428_MergeRegistry_Union.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Subtraction(self):
        self.assertTrue(T429_MergeRegistry_Subtraction.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_Intersection(self):
        self.assertTrue(T430_MergeRegistry_Intersection.Test()["testStatus"])

    def test_PythonGeant_MergeRegistry_MultiUnion(self):
        self.assertTrue(T431_MergeRegistry_MultiUnion.Test()["testStatus"])

    def test_PythonGeant_MergeRegistryBoxAssemblyConverion(self):
        self.assertTrue(T432_MergeRegistry_Box_AssemblyConversion.Test()["testStatus"])

if __name__ == '__main__':
    _unittest.main(verbosity=2)

    class TracingStreamResult(_testtools.StreamResult):
        def status(self, *args, **kwargs):
            print('{0[test_id]}: {0[test_status]}'.format(kwargs))