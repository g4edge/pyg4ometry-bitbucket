import unittest

import pyg4ometry.convert as convert
import pyg4ometry.visualisation as vi
from pyg4ometry.fluka.body import *
from pyg4ometry.fluka.fluka_registry import FlukaBodyStore, HalfSpaceStore
from pyg4ometry.fluka import Transform

class FlukaBodyStore(unittest.TestCase):
    def setUp(self):
        self.halfspaces = HalfSpaceStore()
        # self.aTransform =

    def testXZPCaching(self):
        xzp = XZP("xzp1", 10)
        self.halfspaces.addBody(xzp)




def main():
    store = FlukaBodyStore()

    # rpp = RPP("rpp1", 0, 10, 0, 10,

    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
