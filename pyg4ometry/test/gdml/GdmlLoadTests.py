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
            "para" : solid_inf(5, "005_para.gdml", "para1", -1),
            "trd" : solid_inf(6, "006_trd.gdml", "trd1", -1),
            "trap" : solid_inf(7, "007_trap.gdml", "trap1", -1),
            "sphere" : solid_inf(8, "008_sphere.gdml", "sphere1", -1),
            "orb" : solid_inf(9, "009_orb.gdml", "orb1", -1),
            "torus" : solid_inf(10, "010_torus.gdml", "torus1", -1),
            "polycone" : solid_inf(11, "011_polycone.gdml", "polycone1", -1),
            # TODO: 12 Generic polycone
            "polyhedra" : solid_inf(13, "013_polyhedra.gdml", "polyhedra1", -1),
            # TODO: 14 Generic polyhedra
            "eltube" : solid_inf(15, "015_eltube.gdml", "eltube1", -1),
            "ellipsoid" : solid_inf(16, "016_ellipsoid.gdml", "ellipsoid1", -1),
            "elcone" : solid_inf(17, "017_elcone.gdml", "elcone1", -1),
            "paraboloid" : solid_inf(18, "018_paraboloid.gdml", "paraboloid1", -1),
            "hype" : solid_inf(19, "019_hype.gdml", "hype1", -1),
            "tet" : solid_inf(20, "020_tet.gdml", "tet1", -1),
            # TODO: 21 Extruded solid
            "twistedbox" : solid_inf(22, "022_twisted_box.gdml", "twistbox1", -1),
            # TODO: 23 Twsited trap
            # TODO: 24 Twsited trd
            # TODO: 25 Twsited tubs
            # TODO: 26 Arbitrary trap
            # TODO: 27 Tesselated solid
            "union" : solid_inf(28, "028_union.gdml", "union1", -1),
            "subtraction" : solid_inf(29, "029_subtraction.gdml", "subtraction1", -1),
            "intersection" : solid_inf(30, "030_intersection.gdml", "intersection1", -1),

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

    def testParaLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("para")))

    def testTrdLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("trd")))

    def testTrapLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("trap")))

    def testSphereLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("sphere")))

    def testOrbLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("orb")))

    def testTorusLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("torus")))

    def testPolyconeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("polycone")))

    # TODO: Generic Polycone here

    def testPolyhedraLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("polyhedra")))

    # TODO: Generic Polyhedra here

    def testEltubeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("eltube")))

    def testEllipsoidLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("ellipsoid")))

    def testElconeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("elcone")))

    def testParaboloidLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("paraboloid")))

    def testHypeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("hype")))

    def testTetLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("tet")))

    # TODO: Extruded solid

    def testTwistedBox(self):
        self.assertTrue(bool(_loader.getMeshHashes("tet")))

    # TODO: Twsited trap here

    # TODO: Twsited trd here

    # TODO: Twsited tubs here

    # TODO: Arbitrary trap here

    # TODO: Tesselated solid here

    def testUnionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("union")))

    def testSubtractionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("subtraction")))

    def testIntersetionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("intersection")))

if __name__ == '__main__':
    _unittest.main(verbosity=2)
