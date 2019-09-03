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
        self.assertTrue(T001_Box.Test(vis=True))

    def testTubs(self) :
        self.assertTrue(T002_Tubs.Test())

    def testCutTubs(self) :
        self.assertTrue(T003_CutTubs.Test(False,T003_CutTubs.normal))
        self.assertTrue(T003_CutTubs.Test(False,T003_CutTubs.flat_ends))

    def testCons(self) :
        try : 
            T004_Cons.Test(False,T004_Cons.r1min_gt_r1max)
        except ValueError :
            pass

        try : 
            T004_Cons.Test(False,T004_Cons.r2min_gt_r2max)
        except ValueError : 
            pass

        try : 
            T004_Cons.Test(False,T004_Cons.dphi_gt_2pi)
        except ValueError : 
            pass

        self.assertTrue(T004_Cons.Test(False,T004_Cons.dphi_eq_2pi))
        self.assertTrue(T004_Cons.Test(False,T004_Cons.cone_up))
        self.assertTrue(T004_Cons.Test(False,T004_Cons.inner_cylinder))

        self.assertTrue(T004_Cons.Test())      
      
    def testPara(self) :
        self.assertTrue(T005_Para.Test())

    def testTrd(self) :
        self.assertTrue(T006_Trd.Test())

    def testTrap(self) :
        self.assertTrue(T007_Trap.Test())

    def testSphere(self) :
        self.assertTrue(T008_Sphere.Test())

    def testOrb(self) :
        self.assertTrue(T009_Orb.Test())

    def testTorus(self) :
        self.assertTrue(T010_Torus.Test())

    def testPolycone(self) :
        self.assertTrue(T011_Polycone.Test())

    def testGenericPolycone(self) :
        self.assertTrue(T012_GenericPolycone.Test(False,T012_GenericPolycone.normal))

        try : 
            T012_GenericPolycone.Test(False,T012_GenericPolycone.two_planes)
        except ValueError : 
            pass

    def testPolyhedra(self) :
        self.assertTrue(T013_Polyhedra.Test())

    def testGenericPolyhedra(self) : 
        self.assertTrue(T014_GenericPolyhedra.Test(False,T014_GenericPolyhedra.normal))

        try : 
            T014_GenericPolyhedra.Test(False,T014_GenericPolyhedra.two_planes)            
        except ValueError : 
            pass

    def testEllipticalTube(self) : 
        self.assertTrue(T015_EllipticalTube.Test())

    def testEllipsoid(self) : 
        self.assertTrue(T016_Ellipsoid.Test())

    def testEllipticalCone(self) : 
        self.assertTrue(T017_EllipticalCone.Test())
        
        try : 
            T017_EllipticalCone.Test(False,T017_EllipticalCone.zcut_outofrange)
        except ValueError : 
            pass

    def testParaboloid(self) : 
        self.assertTrue(T018_Paraboloid.Test())

    def testHyperboloid(self) : 
        self.assertTrue(T019_Hyperboloid.Test(False,T019_Hyperboloid.normal))
        self.assertTrue(T019_Hyperboloid.Test(False,T019_Hyperboloid.rmin_eq_zero))

        try : 
            T019_Hyperboloid.Test(False,T019_Hyperboloid.rmin_gt_rmax)            
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
        self.assertTrue(T030_Intersection.Test(False,T030_Intersection.normal))

        try : 
            T030_Intersection.Test(False,T030_Intersection.non_intersecting)            
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def testMultiUnion(self) : 
        self.assertTrue(T031_MultiUnion.Test(False,False))
        

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
