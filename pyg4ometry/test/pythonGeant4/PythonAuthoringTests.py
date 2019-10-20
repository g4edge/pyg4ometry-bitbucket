import unittest as _unittest
import numpy as _np

import pyg4ometry

import T000_SolidBase
import T001_Box
import T002_Tubs
import T003_CutTubs
import T0031_CutTubs_number
import T0032_CutTubs_string
import T0033_CutTubs_expression
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

import logging as _log

logger = _log.getLogger()
logger.disabled = True

class PythonAuthoringTests(_unittest.TestCase) :
    def testPlane(self) : 
        p = pyg4ometry.geant4.solid.Plane("plane",[0,0,1],1000)
        str(p)

    def testWedge(self) : 
        w = pyg4ometry.geant4.solid.Wedge("wedge",1000,0,1.5*_np.pi,10000)
        str(w)

    def testSolidBase(self) :         
        self.assertTrue(T000_SolidBase.Test())

    def testBox(self) :
        self.assertTrue(T001_Box.Test(False,False)["testStatus"])

    def testTubs(self) :
        self.assertTrue(T002_Tubs.Test(False,False))

    def testCutTubs(self) :
        self.assertTrue(T003_CutTubs.Test(False, False, T003_CutTubs.normal)["testStatus"])
        self.assertTrue(T003_CutTubs.Test(False, False, T003_CutTubs.flat_ends)["testStatus"])

    def testCons(self) :
        try : 
            T004_Cons.Test(False,False,T004_Cons.r1min_gt_r1max)
        except ValueError :
            pass

        try : 
            T004_Cons.Test(False,False,T004_Cons.r2min_gt_r2max)
        except ValueError : 
            pass

        try : 
            T004_Cons.Test(False,False,T004_Cons.dphi_gt_2pi)
        except ValueError : 
            pass

        self.assertTrue(T004_Cons.Test(False,False,T004_Cons.dphi_eq_2pi)["testStatus"])
        self.assertTrue(T004_Cons.Test(False,False,T004_Cons.cone_up)["testStatus"])
        self.assertTrue(T004_Cons.Test(False,False,T004_Cons.inner_cylinder)["testStatus"])

        self.assertTrue(T004_Cons.Test(False,False)["testStatus"])
      
    def testPara(self) :
        self.assertTrue(T005_Para.Test(False,False)["testStatus"])

    def testTrd(self) :
        self.assertTrue(T006_Trd.Test(False,False)["testStatus"])

    def testTrap(self) :
        self.assertTrue(T007_Trap.Test(False,False)["testStatus"])

    def testSphere(self) :
        self.assertTrue(T008_Sphere.Test())

    def testOrb(self) :
        self.assertTrue(T009_Orb.Test())

    def testTorus(self) :
        self.assertTrue(T010_Torus.Test())

    def testPolycone(self) :
        self.assertTrue(T011_Polycone.Test())

    def testGenericPolycone(self) :
        self.assertTrue(T012_GenericPolycone.Test(False,False,T012_GenericPolycone.normal))

        try : 
            T012_GenericPolycone.Test(False,False,T012_GenericPolycone.two_planes)
        except ValueError : 
            pass

    def testPolyhedra(self) :
        self.assertTrue(T013_Polyhedra.Test())

    def testGenericPolyhedra(self) : 
        self.assertTrue(T014_GenericPolyhedra.Test(False,False,T014_GenericPolyhedra.normal))

        try : 
            T014_GenericPolyhedra.Test(False,False, T014_GenericPolyhedra.two_planes)
        except ValueError : 
            pass

    def testEllipticalTube(self) : 
        self.assertTrue(T015_EllipticalTube.Test())

    def testEllipsoid(self) : 
        self.assertTrue(T016_Ellipsoid.Test())

    def testEllipticalCone(self) : 
        self.assertTrue(T017_EllipticalCone.Test())
        
        try : 
            T017_EllipticalCone.Test(False,False, T017_EllipticalCone.zcut_outofrange)
        except ValueError : 
            pass

    def testParaboloid(self) : 
        self.assertTrue(T018_Paraboloid.Test())

    def testHyperboloid(self) : 
        self.assertTrue(T019_Hyperboloid.Test(False,False,T019_Hyperboloid.normal))
        self.assertTrue(T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_eq_zero))

        try : 
            T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_gt_rmax)
        except ValueError : 
            pass

    def testTet(self) :
        self.assertTrue(T020_Tet.Test())        

    def testExtrudedSolid(self) :
        self.assertTrue(T021_ExtrudedSolid.Test())        

    def testTwistedBox(self) : 
        self.assertTrue(T022_TwistedBox.Test())

    def testTwistedTrap(self) : 
        self.assertTrue(T023_TwistedTrap.Test())

    def testTwistedTrd(self) : 
        self.assertTrue(T024_TwistedTrd.Test())

    def testTwistedTubs(self) : 
        self.assertTrue(T025_TwistedTubs.Test())

    def testGenericTrap(self) : 
        self.assertTrue(T026_GenericTrap.Test())

    def testUnion(self) : 
        self.assertTrue(T028_Union.Test())

    def testSubtraction(self) : 
        self.assertTrue(T029_Subtraction.Test())

    def testIntersection(self) : 
        self.assertTrue(T030_Intersection.Test(False,False,T030_Intersection.normal))

        try : 
            T030_Intersection.Test(False,False,T030_Intersection.non_intersecting)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def testMultiUnion(self) : 
        self.assertTrue(T031_MultiUnion.Test())

    def testScaled(self):
        self.assertTrue(T032_Scaled.Test()["testStatus"])
    def testMergeRegistry(self):
        self.assertTrue(T400_MergeRegistry.Test())

    def testMergeRegistry_Box(self):
        self.assertTrue(T401_MergeRegistry_Box.Test(False,False)["testStatus"])

    def testMergeRegistry_Tubs(self):
        self.assertTrue(T402_MergeRegistry_Tubs.Test()["testStatus"])

    def testMergeRegistry_CutTubs(self):
        self.assertTrue(T403_MergeRegistry_CutTubs.Test()["testStatus"])

    def testMergeRegistry_Cons(self):
        self.assertTrue(T404_MergeRegistry_Cons.Test()["testStatus"])

    def testMergeRegistry_Para(self):
        self.assertTrue(T405_MergeRegistry_Para.Test()["testStatus"])

    def testMergeRegistry_Trd(self):
        self.assertTrue(T406_MergeRegistry_Trd.Test()["testStatus"])

    def testMergeRegistry_Trap(self):
        self.assertTrue(T407_MergeRegistry_Trap.Test()["testStatus"])

    def testMergeRegistry_(self):
        self.assertTrue(T407_MergeRegistry_Trap.Test()["testStatus"])

    def testMergeRegistry_Sphere(self):
        self.assertTrue(T408_MergeRegistry_Sphere.Test()["testStatus"])

    def testMergeRegistry_Orb(self):
        self.assertTrue(T409_MergeRegistry_Orb.Test()["testStatus"])

    def testMergeRegistry_Torus(self):
        self.assertTrue(T410_MergeRegistry_Torus.Test()["testStatus"])

    def testMergeRegistry_Polycone(self):
        self.assertTrue(T411_MergeRegistry_Polycone.Test()["testStatus"])

    def testMergeRegistry_GenericPolycone(self):
        self.assertTrue(T412_MergeRegistry_GenericPolycone.Test()["testStatus"])

    def testMergeRegistry_Polyhedra(self):
        self.assertTrue(T413_MergeRegistry_Polyhedra.Test()["testStatus"])

    def testMergeRegistry_GenericPolyhedra(self):
        self.assertTrue(T414_MergeRegistry_GenericPolyhedra.Test()["testStatus"])

    def testMergeRegistry_GenericPolyhedra(self):
        self.assertTrue(T414_MergeRegistry_GenericPolyhedra.Test()["testStatus"])

    def testMergeRegistry_EllipticalTube(self):
        self.assertTrue(T415_MergeRegistry_EllipticalTube.Test()["testStatus"])

    def testMergeRegistry_Ellipsoid(self):
        self.assertTrue(T416_MergeRegistry_Ellipoid.Test()["testStatus"])

    def testMergeRegistry_EllipticalCone(self):
        self.assertTrue(T417_MergeRegistry_EllipticalCone.Test()["testStatus"])

    def testMergeRegistry_EllipticalParaboloid(self):
        self.assertTrue(T418_MergeRegistry_Paraboloid.Test()["testStatus"])

    def testMergeRegistry_Hyperboloid(self):
        self.assertTrue(T419_MergeRegistry_Hyperboloid.Test()["testStatus"])

    def testMergeRegistry_Tet(self):
        self.assertTrue(T420_MergeRegistry_Tet.Test()["testStatus"])

    def testMergeRegistry_ExtrudedSolid(self):
        self.assertTrue(T421_MergeRegistry_ExtrudedSolid.Test()["testStatus"])

    def testMergeRegistry_TwistedBox(self):
        self.assertTrue(T422_MergeRegistry_TwistedBox.Test()["testStatus"])

    def testMergeRegistry_TwistedTrap(self):
        self.assertTrue(T423_MergeRegistry_TwistedTrap.Test()["testStatus"])

    def testMergeRegistry_TwistedTrd(self):
        self.assertTrue(T424_MergeRegistry_TwistedTrd.Test()["testStatus"])

    def testMergeRegistry_TwistedTubs(self):
        self.assertTrue(T425_MergeRegistry_TwistedTubs.Test()["testStatus"])

    def testMergeRegistry_GenericTrap(self):
        self.assertTrue(T426_MergeRegistry_GenericTrap.Test()["testStatus"])

    def testMergeRegistry_Union(self):
        self.assertTrue(T428_MergeRegistry_Union.Test()["testStatus"])

    def testMergeRegistry_Subtraction(self):
        self.assertTrue(T429_MergeRegistry_Subtraction.Test()["testStatus"])

    def testMergeRegistry_Intersection(self):
        self.assertTrue(T430_MergeRegistry_Intersection.Test()["testStatus"])

    def testMergeRegistry_MultiUnion(self):
        self.assertTrue(T431_MergeRegistry_MultiUnion.Test()["testStatus"])

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
