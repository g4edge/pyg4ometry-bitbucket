import unittest as _unittest

import T001_Box
import T002_Tubs
import T003_CutTubs
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

import logging as _log

logger = _log.getLogger()
logger.disabled = True

class PythonAuthoringTests(_unittest.TestCase) :
    def testBox(self) :
        self.assertTrue(T001_Box.Test())

    def testTubs(self) :
        self.assertTrue(T002_Tubs.Test())

    def testCutTubs(self) :
        self.assertTrue(T003_CutTubs.Test())

    def testCons(self) :
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
        self.assertTrue(T012_GenericPolycone.Test())

    def testPolyhedra(self) :
        self.assertTrue(T013_Polyhedra.Test())

    def testGenericPolyhedra(self) : 
        self.assertTrue(T014_GenericPolyhedra.Test())

    def testEllipticalTube(self) : 
        self.assertTrue(T015_EllipticalTube.Test())

    def testEllipsoid(self) : 
        self.assertTrue(T016_Ellipsoid.Test())

    def testEllipticalCone(self) : 
        self.assertTrue(T017_EllipticalCone.Test())

    def testParaboloid(self) : 
        self.assertTrue(T018_Paraboloid.Test())


if __name__ == '__main__':
    _unittest.main(verbosity=2)        
