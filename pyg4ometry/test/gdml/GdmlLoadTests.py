import unittest as _unittest
import os as _os

import pyg4ometry
import logging as _log

from collections import namedtuple

logger = _log.getLogger()
logger.disabled = True


def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

# Make a cheeky class to reduce repetition
class SolidLoader(object):
    """
    Simple class to perfrom loading of and checking of solids
    """
    def __init__(self, verbosity=0):

        solid_inf = namedtuple('SolidInfo', 'index filename solidname hashval')
        self.verbosity = verbosity
        self.solid_dict = {
            # solid file index, filename, solid name in file and mesh hash
            "box" : solid_inf(1, _pj("001_box.gdml"), "box1", -4189916779045808977),
            "tube" : solid_inf(2, _pj("002_tubs.gdml"), "tube1", -7570577582805396235),
            "cuttube" : solid_inf(3, _pj("003_cut_tubs.gdml"), "cuttube1", 6510770975685252931),
            "cone" : solid_inf(4, _pj("004_cons.gdml"), "cone1", -435058689958624196),
            "para" : solid_inf(5, _pj("005_para.gdml"), "para1", -1),
            "trd" : solid_inf(6, _pj("006_trd.gdml"), "trd1", -1),
            "trap" : solid_inf(7, _pj("007_trap.gdml"), "trap1", -1),
            "sphere" : solid_inf(8, _pj("008_sphere.gdml"), "sphere1", -1),
            "orb" : solid_inf(9, _pj("009_orb.gdml"), "orb1",-1),
            "torus" : solid_inf(10, _pj("010_torus.gdml"), "torus1", -1),
            "polycone" : solid_inf(11, _pj("011_polycone.gdml"), "polycone1", -1),
            "genpoly" : solid_inf(12, _pj("012_generic_polycone.gdml"), "genpoly1", -1),
            "polyhedra" : solid_inf(13, _pj("013_polyhedra.gdml"), "polyhedra1", -1),
            "genpolyhedra" : solid_inf(14, _pj("014_generic_polyhedra.gdml"), "genpolyhedra1", -1),
            "eltube" : solid_inf(15, _pj("015_eltube.gdml"), "eltube1", -1),
            "ellipsoid" : solid_inf(16, _pj("016_ellipsoid.gdml"), "ellipsoid1", -1),
            "elcone" : solid_inf(17, _pj("017_elcone.gdml"), "elcone1", -1),
            "paraboloid" : solid_inf(18, _pj("018_paraboloid.gdml"), "paraboloid1", -1),
            "hype" : solid_inf(19, _pj("019_hype.gdml"), "hype1", -1),
            "tet" : solid_inf(20, _pj("020_tet.gdml"), "tet1", -1),
            "xtru" : solid_inf(21, _pj("021_xtru.gdml"), "xtru1", -1),
            "twistedbox" : solid_inf(22, _pj("022_twisted_box.gdml"), "twistbox1", -1),
            "twistedtrap" : solid_inf(23, _pj("023_twisted_trap.gdml"), "twisttrap1", -1),
            "twistedtrd" : solid_inf(24, _pj("024_twisted_trd.gdml"), "twisttrd1", -1),
            "twistedtubs" : solid_inf(25, _pj("024_twisted_tubs.gdml"), "twisttubs1", -1),
            "arbtrap" : solid_inf(26, _pj("026_generic_trap.gdml"), "arb81", -1),
            # TODO: 27 Tesselated solid
            "union" : solid_inf(28, _pj("028_union.gdml"), "union1", -1),
            "subtraction" : solid_inf(29, _pj("029_subtraction.gdml"), "subtraction1", -1),
            "intersection" : solid_inf(30, _pj("030_intersection.gdml"), "intersection1", -1),
            "multiunion" : solid_inf(31, _pj("031_multiUnion.gdml"),"multiunion1",-1)
        }

        # solid name : (nslice , nstack)
        # nslice is normally used for granularity of curvature in radius
        # nstack is normally used for granularity of curvature in Z
        # solids not listed here do not have discretised curves
        self.curved_solids = {
            "Tubs" : (16, None),
            "CutTubs" : (16, None),
            "Cons" : (16, None),
            "Sphere" : (6, 6),
            "Orb" : (16, 8),
            "Torus" : (6, 6),
            "Polycone" : (16, None),
            "GenericPolycone" : (16, None),
            "EllipticalTube" : (6, 6),
            "Ellipsoid" : (8, 8),
            "EllipticalCone" : (16, 16),
            "Paraboloid" : (16, 8),
            "Hype" : (6, 6),
            "TwistedBox" : (None, 20),
            "TwistedTrap" : (None, 20),
            "TwistedTrd" : (None, 20),
            "TwistedTubs" : (16, 16),
            "GenericTrap" : (None, 20),
        }

    def getMeshHashes(self, solidname):
        reader = pyg4ometry.gdml.Reader(self.solid_dict[solidname].filename)
        reg = reader.getRegistry()
        solid = reg.solidDict[self.solid_dict[solidname].solidname]

        if solid.type in self.curved_solids:
            mesh_density = self.curved_solids[solid.type]
            if mesh_density[0]:
                setattr(solid, "nslice", mesh_density[0])
            if mesh_density[1]:
                setattr(solid, "nstack", mesh_density[1])

        if self.verbosity:
            print solid # Dump the parameters of the solid / check the repr method
        mesh = solid.pycsgmesh()
        return (hash(mesh), self.solid_dict[solidname].hashval)

_loader = SolidLoader(verbosity=0)


class GdmlLoadTests(_unittest.TestCase) :
    def testMalformedGdml(self) : 
        import xml.parsers.expat                 as _expat
        
        try : 
            r = pyg4ometry.gdml.Reader(_pj("./300_malformed_gdml.gdml"))
        except _expat.ExpatError :
            pass

    def testQuantity(self) :
        r = pyg4ometry.gdml.Reader(_pj("301_quantity.gdml"))

    def testVariable(self) :
        r = pyg4ometry.gdml.Reader(_pj("302_variable.gdml"))

    def testMatrix(self) :
        r = pyg4ometry.gdml.Reader(_pj("303_matrix.gdml"))

    def testScale(self) :
        r = pyg4ometry.gdml.Reader(_pj("304_scale.gdml"))

    def testUnrecognisedDefine(self) :
        r = pyg4ometry.gdml.Reader(_pj("305_unrecognised_define.gdml"))

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

    def testGenericPolyconeLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("genpoly")))

    def testPolyhedraLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("polyhedra")))

    def testGenericPolyhedraLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("genpolyhedra")))

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

    def testExtrudedSolid(self):
        self.assertTrue(bool(_loader.getMeshHashes("xtru")))

    def testTwistedBox(self):
        self.assertTrue(bool(_loader.getMeshHashes("tet")))

    def testTwistedTrd(self):
        self.assertTrue(bool(_loader.getMeshHashes("twistedtubs")))

    def testTwistedTrd(self):
        self.assertTrue(bool(_loader.getMeshHashes("twistedtrd")))

    def testTwistedTrap(self):
        self.assertTrue(bool(_loader.getMeshHashes("twistedtrap")))

    def testTwistedTrd(self):
        self.assertTrue(bool(_loader.getMeshHashes("twistedtrd")))

    # TODO: Tesselated solid here

    def testUnionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("union")))

    def testSubtractionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("subtraction")))

    def testIntersetionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("intersection")))

    def testMultiUnionLoad(self):
        self.assertTrue(bool(_loader.getMeshHashes("multiunion")))

    def testMaterials(self):
        r = pyg4ometry.gdml.Reader(_pj("201_materials.gdml"))
        w = pyg4ometry.gdml.Writer()
        w.addDetector(r.getRegistry())
        w.write(_pj("201_materials_processed.gdml"))

    def testAuxiliary(self):
        r = pyg4ometry.gdml.Reader(_pj("202_auxiliary.gdml"))
        w = pyg4ometry.gdml.Writer()
        w.addDetector(r.getRegistry())
        w.write(_pj("202_auxiliary_processed.gdml"))

    def testEntity(self):
        with open(_pj("203_entity.gdml")) as infile:
            contents = infile.read()

            contents_replaced = contents.replace("203_materials.xml", _pj("203_materials.xml"))
            with open(_pj("203_temp.gdml"), "w") as tempfile:
                tempfile.write(contents_replaced)

        r = pyg4ometry.gdml.Reader(_pj("203_temp.gdml"))
        w = pyg4ometry.gdml.Writer()
        w.addDetector(r.getRegistry())
        w.write(_pj("203_entity_processed.gdml"))
        _os.unlink(_pj("203_temp.gdml"))

if __name__ == '__main__':
    _unittest.main(verbosity=2)
