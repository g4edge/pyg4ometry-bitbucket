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

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
