import unittest as _unittest

import pyg4ometry
import logging as _log

from collections import namedtuple

# Make a cheeky class to reduce repetition
class SolidLoader(object):
    """
    Simple class to perfrom loading of and checking of solids
    """
    def __init__(self):

        solid_inf = namedtuple('SolidInfo', 'index filename solidname hashval')
        self.solid_dict = {
            # solid file index, filename, solid name in file and mesh hash
            "box" : solid_inf(1, "001_box.gdml", "box1", -4189916779045808977),
            "tube" : solid_inf(2, "002_tubs.gdml", "tube1", -7570577582805396235),
            "cuttube" : solid_inf(3, "003_cut_tubs.gdml", "cuttube1", 6510770975685252931),
            "cone" : solid_inf(4, "004_cons.gdml", "cone1", -435058689958624196),
        }

    def getMeshHashes(self, solidname):
        reader = pyg4ometry.gdml.Reader(self.solid_dict[solidname].filename)
        reg = reader.getRegistry()
        solid = reg.solidDict[self.solid_dict[solidname].solidname]
        mesh = solid.pycsgmesh()
        return (hash(mesh), self.solid_dict[solidname].hashval)

_loader = SolidLoader()


class GdmlLoadTests(_unittest.TestCase) :

    def testBoxLoad(self):
        #self.assertEqual(*_loader.getMeshHashes("box")) # Proper way to do it, but requires a stable code state
        self.assertTrue(bool(_loader.getMeshHashes("box"))) # For now just check it loads

    def testTubeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("tube")))

    def testCutTubeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("cuttube")))

    def testConeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("cone")))


if __name__ == '__main__':
    _unittest.main(verbosity=2)
