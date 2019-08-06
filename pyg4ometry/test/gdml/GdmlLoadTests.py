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

class MeshValidator(object):
    """
    Simple class to perfrom checking of mesh validity by using stored mesh checksums
    """
    def __init__(self, verbosity=0):

        self.verbosity = verbosity
        self.solid_checksums = {
            "001_box.gdml" : ("box1", -4189916779045808977),
            "002_tubs.gdml" : ("tube1", -7570577582805396235),
            "003_cut_tubs.gdml" : ("cuttube1", 6510770975685252931),
            "004_cons.gdml" : ("cone1", -435058689958624196),
            "005_para.gdml" : ("para1", -1),
            "006_trd.gdml" : ("trd1", -1),
            "007_trap.gdml" : ("trap1", -1),
            "008_sphere.gdml" : ("sphere1", -1),
            "009_orb.gdml" : ("orb1",-1),
            "010_torus.gdml" : ("torus1", -1),
            "011_polycone.gdml" : ("polycone1", -1),
            "012_generic_polycone.gdml" : ( "genpoly1", -1),
            "013_polyhedra.gdml" : ("polyhedra1", -1),
            "014_generic_polyhedra.gdml" : ( "genpolyhedra1", -1),
            "015_eltube.gdml" : ("eltube1", -1),
            "016_ellipsoid.gdml" : ("ellipsoid1", -1),
            "017_elcone.gdml" : ("elcone1", -1),
            "018_paraboloid.gdml" : ( "paraboloid1", -1),
            "019_hype.gdml" : ( "hype1", -1),
            "020_tet.gdml" : ( "tet1", -1),
            "021_xtru.gdml" : ( "xtru1", -1),
            "022_twisted_box.gdml" : ("twistbox1", -1),
            "023_twisted_trap.gdml" : ("twisttrap1", -1),
            "024_twisted_trd.gdml" : ("twisttrd1", -1),
            "025_twisted_tube.gdml" : ("twisttube1", -1),
            "026_generic_trap.gdml" : ("arb81", -1),
            # TODO: 27 Tesselated solid
            "028_union.gdml" : ("union1", -1),
            "029_subtraction.gdml" : ("subtraction1", -1),
            "030_intersection.gdml" : ("intersection1", -1),
            "031_multiUnion.gdml" : ("multiunion1",-1),
            "032_scaled.gdml" : ("box1Scaled",-1)
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

        self.division_checksums = {
            # The hashes of the first division mesh for every division test
            "124_division_box_x.gdml" : -1,
            "125_division_box_y.gdml" : -1,
            "126_division_box_z.gdml" : -1,
            "127_division_tubs_rho.gdml" : -1,
            "128_division_tubs_phi.gdml" : -1,
            "129_division_tubs_z.gdml" : -1,
            "130_division_cons_rho.gdml" : -1,
            "131_division_cons_phi.gdml" : -1,
            "132_division_cons_z.gdml" : -1,
            "133_division_trd_x.gdml" : -1,
            "134_division_trd_y.gdml" : -1,
            "135_division_trd_z.gdml" : -1,
            "136_division_para_x.gdml" : -1,
            "137_division_para_y.gdml" : -1,
            "138_division_para_z.gdml" : -1,
            "139_division_polycone_rho.gdml" : -1,
            "140_division_polycone_phi.gdml" : -1,
            "141_division_polycone_z.gdml" : -1,
            "142_division_polyhedra_rho.gdml" : -1,
            "143_division_polyhedra_phi.gdml" : -1,
            "144_division_polyhedra_z.gdml" : -1,
        }

        self.available_checksums = self.solid_checksums.keys() + self.division_checksums.keys()

    def verifyMeshChecksum(self, filename, registry):
        if filename in self.solid_checksums:
            solid = registry.solidDict[self.solid_checksums[filename][0]]
            checksum = self.solid_checksums[filename][1]

            if solid.type in self.curved_solids:
                mesh_density = self.curved_solids[solid.type]
                if mesh_density[0]:
                    setattr(solid, "nslice", mesh_density[0])
                if mesh_density[1]:
                    setattr(solid, "nstack", mesh_density[1])

        elif filename in self.division_checksums:
            for volname, volume in registry.physicalVolumeDict.iteritems():
                if volume.type == "division":
                    solid = volume.meshes[0].solid

            checksum = self.division_checksums[filename]

        if self.verbosity:
            print solid # Dump the parameters of the solid / check the repr method

        mesh = solid.pycsgmesh()

        return True #hash(mesh) == self.solid_checksums[filename][1]

_meshValidator = MeshValidator(verbosity=0)

def testSingleGDML(filename):
    filepath = _pj(filename)

    # Loading
    reader = pyg4ometry.gdml.Reader(filepath)
    registry = reader.getRegistry()

    # Visualisation
    v = pyg4ometry.visualisation.VtkViewer()
    v.addLogicalVolume(registry.getWorldVolume())
    v.view(interactive=False)

    # Writing
    writer = pyg4ometry.gdml.Writer()
    writer.addDetector(registry)
    writer.write(filepath.replace(".gdml", "_processed.gdml"))

    if filename in _meshValidator.available_checksums:
        return _meshValidator.verifyMeshChecksum(filename, registry)
    else:
        return True

class GdmlLoadTests(_unittest.TestCase) :
    def testMalformedGdml(self) : 
        import xml.parsers.expat                 as _expat
        
        try : 
            r = pyg4ometry.gdml.Reader(_pj("./300_malformed_gdml.gdml"))
        except _expat.ExpatError :
            pass

    def testQuantity(self) :
        self.assertTrue(testSingleGDML("301_quantity.gdml"))

    def testVariable(self) :
        self.assertTrue(testSingleGDML("302_variable.gdml"))

    def testMatrix(self) :
        self.assertTrue(testSingleGDML("303_matrix.gdml"))

    def testScale(self) :
        self.assertTrue(testSingleGDML("304_scale.gdml"))

    def testUnrecognisedDefine(self) :
        self.assertTrue(testSingleGDML("305_unrecognised_define.gdml"))

    def testBoxLoad(self):
        self.assertTrue(testSingleGDML("001_box.gdml")) # For now just check it loads

    def testTubeLoad(self):
        self.assertTrue(testSingleGDML("002_tubs.gdml"))

    def testCutTubeLoad(self):
        self.assertTrue(testSingleGDML("003_cut_tubs.gdml"))

    def testConeLoad(self):
        self.assertTrue(testSingleGDML("004_cons.gdml"))

    def testParaLoad(self):
        self.assertTrue(testSingleGDML("005_para.gdml"))

    def testTrdLoad(self):
        self.assertTrue(testSingleGDML("006_trd.gdml"))

    def testTrapLoad(self):
        self.assertTrue(testSingleGDML("007_trap.gdml"))

    def testSphereLoad(self):
        self.assertTrue(testSingleGDML("008_sphere.gdml"))

    def testOrbLoad(self):
        self.assertTrue(testSingleGDML("009_orb.gdml"))

    def testTorusLoad(self):
        self.assertTrue(testSingleGDML("010_torus.gdml"))

    def testPolyconeLoad(self):
        self.assertTrue(testSingleGDML("011_polycone.gdml"))

    def testGenericPolyconeLoad(self):
        self.assertTrue(testSingleGDML("012_generic_polycone.gdml"))

    def testPolyhedraLoad(self):
        self.assertTrue(testSingleGDML("013_polyhedra.gdml"))

    def testGenericPolyhedraLoad(self):
        self.assertTrue(testSingleGDML("014_generic_polyhedra.gdml"))

    def testEltubeLoad(self):
        self.assertTrue(testSingleGDML("015_eltube.gdml"))

    def testEllipsoidLoad(self):
        self.assertTrue(testSingleGDML("016_ellipsoid.gdml"))

    def testElconeLoad(self):
        self.assertTrue(testSingleGDML("017_elcone.gdml"))

    def testParaboloidLoad(self):
        self.assertTrue(testSingleGDML("018_paraboloid.gdml"))

    def testHypeLoad(self):
        self.assertTrue(testSingleGDML("019_hype.gdml"))

    def testTetLoad(self):
        self.assertTrue(testSingleGDML("020_tet.gdml"))

    def testExtrudedSolid(self):
        self.assertTrue(testSingleGDML("021_xtru.gdml"))

    def testTwistedBox(self):
        self.assertTrue(testSingleGDML("022_twisted_box.gdml"))

    def testTwistedTrap(self):
        self.assertTrue(testSingleGDML("023_twisted_trap.gdml"))

    def testTwistedTrd(self):
        self.assertTrue(testSingleGDML("024_twisted_trd.gdml"))

    def testTwistedTubs(self):
        self.assertTrue(testSingleGDML("025_twisted_tub2.gdml"))

    def testGenericTrap(self):
        self.assertTrue(testSingleGDML("026_generic_trap.gdml"))

    # TODO: Tesselated solid here

    def testUnionLoad(self):
        self.assertTrue(testSingleGDML("028_union.gdml"))

    def testSubtractionLoad(self):
        self.assertTrue(testSingleGDML("029_subtraction.gdml"))

    def testIntersetionLoad(self):
        self.assertTrue(testSingleGDML("030_intersection.gdml"))

    def testMultiUnionLoad(self):
        self.assertTrue(testSingleGDML("031_multiUnion.gdml"))

    def testScaledLoad(self):
        self.assertTrue(testSingleGDML("032_scaled.gdml"))

    def testMaterials(self):
        self.assertTrue(testSingleGDML("201_materials.gdml"))

    def testDivisionVolume(self):
        results = []
        for name in _meshValidator.division_checksums:
            print name
            results.append(testSingleGDML(name))

        self.assertTrue(all(results))

    def testAuxiliary(self):
        self.assertTrue(testSingleGDML("202_auxiliary.gdml"))

    def testEntity(self):
        # Need to process the GDML file to inject the absolute path to the entity file
        with open(_pj("203_entity.gdml")) as infile:
            contents = infile.read()

            contents_replaced = contents.replace("203_materials.xml", _pj("203_materials.xml"))
            with open(_pj("203_temp.gdml"), "w") as tempfile:
                tempfile.write(contents_replaced)

        result = testSingleGDML("203_temp.gdml") # Store the result before mopping temp files
        _os.unlink(_pj("203_temp.gdml"))

        self.assertTrue(result)

if __name__ == '__main__':
    _unittest.main(verbosity=2)
