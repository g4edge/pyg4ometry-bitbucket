import unittest
from math import pi

import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka.body import *
from pyg4ometry.fluka.fluka_registry import FlukaBodyStore
from pyg4ometry.fluka import Transform
from pyg4ometry.fluka.directive import (rotoTranslationFromTra2,
                                        rotoTranslationFromTBxyz)

class FlukaBodyStoreTests(unittest.TestCase):
    def setUp(self):
        self.bodystore = FlukaBodyStore()
        self.aTransform = Transform(
            rotoTranslation=rotoTranslationFromTra2(
                "roto", [[pi/4, pi/4, pi/4], [10, 10, 10]]))


class HalfSpaceCachingTests(FlukaBodyStoreTests):
    def testBodyStoreReturnsExistingHalfSpace(self):
        xzp1 = self.bodystore.make(XZP, "xzp1", 10)
        xzp2 = self.bodystore.make(XZP, "xzp2", 10)
        self.assertIs(xzp1, xzp2)

    def testHalfSpaceWithTransformIsReturned(self):
        xzp = self.bodystore.make(XZP, "xzp", 10, transform=self.aTransform)
        pla = self.bodystore.make(PLA, "pla",
                                  [-0.14644661,  0.85355339,  0.5       ],
                                  [-3.23223305, 18.83883476, 11.03553391])
        self.assertIs(xzp, pla)

    def testNewHalfSpaceIsReturnedIfDifferent(self):
        xzp = self.bodystore.make(XZP, "xzp", 10)
        xyp = self.bodystore.make(XYP, "xyp", 15)
        self.assertIsNot(xzp, xyp)

    def testNewHalfSpaceIsReturnedIfDifferingOnlyByTransform(self):
        xzp1 = self.bodystore.make(XZP, "xzp1", 10)
        xzp2 = self.bodystore.make(XZP, "xzp2", 10, transform=self.aTransform)
        self.assertIsNot(xzp1, xzp2)

class InfiniteCylinderCachingTests(FlukaBodyStoreTests):
    def testReturnsIdentical(self):
        xcc1 = self.bodystore.make(XCC, "xcc1", 0, 10, 5)
        xcc2 = self.bodystore.make(XCC, "xcc2", 0, 10, 5)
        self.assertIs(xcc1, xcc2)

    def testDoesntReturnIdenticalWhenDifferent(self):
        xcc1 = self.bodystore.make(XCC, "xcc1", 0, 10, 5)
        xcc2 = self.bodystore.make(XCC, "xcc2", 0, 10, 5,
                                   transform=self.aTransform)
        self.assertIsNot(xcc1, xcc2)

    def testReturnsIdenticalWhenAntiParallel(self):
        xcc1 = self.bodystore.make(XCC, "xcc1", 0, 10, 5)
        xcc2 = self.bodystore.make(
            XCC, "xcc2", 0, 10, 5,
            transform=rotoTranslationFromTBxyz("roto", [0, 0, pi]))
        self.assertIs(xcc1, xcc2)

    def testReturnsIdenticalWhenDifferentType(self):
        xcc = self.bodystore.make(XCC, "xcc", 0, 0, 5)        
        ycc = self.bodystore.make(
            YCC,
            "ycc",
            0, 0, 5,
            transform=rotoTranslationFromTBxyz("roto", [0, 0, pi/2]))
        self.assertIs(xcc, ycc)


if __name__ == '__main__':
    unittest.main(verbosity=2)
