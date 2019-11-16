import unittest as _unittest
import os as _os

import pyg4ometry
import logging as _log

import git as _git

from subprocess import Popen as _Popen, PIPE as _PIPE
from hashlib import md5 as _md5
from collections import OrderedDict as _OrderedDict

#logger = _log.getLogger()
#logger.disabled = True

def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

def pyg4ometryLoadWriteTest(filename, interactive=False):
    filepath = _pj(filename)

    # Loading
    reader = pyg4ometry.gdml.Reader(filepath)
    registry = reader.getRegistry()

    # Visualisation
    v = pyg4ometry.visualisation.VtkViewer()
    v.addLogicalVolume(registry.getWorldVolume())
    v.view(interactive=interactive)

    # Writing
    newFilename = filepath.replace(".gdml", "_processed.gdml")

    writer = pyg4ometry.gdml.Writer()
    writer.addDetector(registry)
    writer.write(newFilename)

    return registry, newFilename


def geant4LoadTest(filename, visualiser=False, physics=False, verbose=True):

    # check if GDML file has updated
    if not checkIfGdmlFileUpdated(filename) :
        return True

    print "geant4LoadTest> running G4"
    script_path = _pj("simple_G4_loader/build/simple_loader")
    if not _os.path.isfile(script_path):
        print "Geant4 test executable not found in {}, skip test.".format(script_path)
        return True

    proc = _Popen([script_path, _pj(filename), str(int(visualiser)), str(int(physics))],
                  stdout=_PIPE, stderr=_PIPE)
    outs, errs = proc.communicate()

    status = proc.returncode
    if status:
        if verbose:
            print "\nError! Geant4 load failed: \nOutput>>> {} \nErrors>>> {}".format(outs, errs)
        return False

    return True

def checkIfGdmlFileUpdated(filename) :
    filename    = _os.path.basename(filename)
    repo        = _git.Repo(_os.path.join(_os.path.dirname(__file__),"../../../"))
    head_commit = repo.head.commit
    diffs       = head_commit.diff(None)

    for d in diffs :
        if _os.path.basename(d.a_path).find(filename) != -1 :
            return True

    return False


# solid name : (nslice , nstack)
# nslice is normally used for granularity of curvature in radius
# nstack is normally used for granularity of curvature in Z
# solids not listed here do not have discretised curves
curved_solids = {
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

def computeGDMLFileChecksum(filename):
    with open(_pj(filename), "r") as gdml_file:
        contents = gdml_file.read()
    checksum = int(_md5(contents.encode()).hexdigest(), 16)

    return checksum

def loadChecksumTable():
    checksum_filepath = _pj("processed_file_checksums.dat")
    checksum_table = _OrderedDict()

    if _os.path.exists(checksum_filepath):
        with open(checksum_filepath, "r") as checksum_file:
            for line in checksum_file:
                sline = line.split()
                checksum_table[sline[0]] = int(sline[1])

    return checksum_table


def writeChecksumTable(checksum_table):
    checksum_filepath = _pj("processed_file_checksums.dat")
    with open(checksum_filepath, "w") as checksum_file:
        for filename, checksum in checksum_table.iteritems():
            checksum_file.write("{}\t{}\n".format(filename, checksum))


def validateProcessedFile(filename):
    checksum_table = loadChecksumTable()
    checksum = computeGDMLFileChecksum(filename)
    checksum = computeGDMLFileChecksum(filename)

    isValid = False
    # Handle missing cases by using get
    if checksum_table.get(filename, -1) == checksum:
        isValid = True
    else:
        isValid = geant4LoadTest(filename)
        if isValid:
            checksum_table[filename] = checksum
            writeChecksumTable(checksum_table)

    return isValid


def getSolidChecksum(solid):
    if solid.type in curved_solids:
        mesh_density = curved_solids[solid.type]
        if mesh_density[0]:
            setattr(solid, "nslice", mesh_density[0])
        if mesh_density[1]:
            setattr(solid, "nstack", mesh_density[1])

    checksum = hash(solid.pycsgmesh())
    return checksum

class GdmlLoadTests(_unittest.TestCase) :
    def testMalformedGdml(self):
        import xml.parsers.expat                 as _expat

        try :
            r = pyg4ometry.gdml.Reader(_pj("./300_malformed_gdml.gdml"))
        except _expat.ExpatError:
            pass

    def testQuantity(self):
        self.assertTrue(pyg4ometryLoadWriteTest("301_quantity.gdml"))

    def testVariable(self):
        self.assertTrue(pyg4ometryLoadWriteTest("302_variable.gdml"))

    def testMatrix(self):
        self.assertTrue(pyg4ometryLoadWriteTest("303_matrix.gdml"))

    def testScale(self):
        self.assertTrue(pyg4ometryLoadWriteTest("304_scale.gdml"))

    def testUnrecognisedDefine(self):
        self.assertTrue(pyg4ometryLoadWriteTest("305_unrecognised_define.gdml"))

    def testBoxLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("001_box.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["box1"]), -1)

    def testTubeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("002_tubs.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["tube1"]), -1)

    def testCutTubeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("003_cut_tubs.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["cuttube1"]), -1)

    def testConeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("004_cons.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["cone1"]), -1)

    def testParaLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("005_para.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["para1"]), -1)

    def testTrdLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("006_trd.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["trd1"]), -1)

    def testTrapLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("007_trap.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["trap1"]), -1)

    def testSphereLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("008_sphere.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["sphere1"]), -1)

    def testOrbLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("009_orb.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["orb1"]), -1)

    def testTorusLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("010_torus.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["torus1"]), -1)

    def testPolyconeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("011_polycone.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["polycone1"]), -1)

    def testGenericPolyconeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("012_generic_polycone.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["genpoly1"]), -1)

    def testPolyhedraLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("013_polyhedra.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["polyhedra1"]), -1)

    def testGenericPolyhedraLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("014_generic_polyhedra.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["genpolyhedra1"]), -1)

    def testEltubeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("015_eltube.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["eltube1"]), -1)

    def testEllipsoidLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("016_ellipsoid.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["ellipsoid"]), -1)

    def testElconeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("017_elcone.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["elcone1"]), -1)

    def testParaboloidLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("018_paraboloid.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["paraboloid1"]), -1)

    def testHypeLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("019_hype.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["hype1"]), -1)

    def testTetLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("020_tet.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["tet1"]), -1)

    def testExtrudedSolid(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("021_xtru.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["xtru1"]), -1)

    def testTwistedBox(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("022_twisted_box.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["twistbox1"]), -1)

    def testTwistedTrap(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("023_twisted_trap.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["twisttrap1"]), -1)

    def testTwistedTrd(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("024_twisted_trd.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["twisttrd1"]), -1)

    def testTwistedTubs(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("025_twisted_tube.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["twisttube1"]), -1)

    def testGenericTrap(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("026_generic_trap.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["arb81"]), -1)

    def testTessellatedSolid(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("027_tesselated.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["tessellated"]), -1)

    def testUnionLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("028_union.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["union1"]), -1)

    def testSubtractionLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("029_subtraction.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["subtraction1"]), -1)

    def testIntersetionLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("030_intersection.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["intersection1"]), -1)

    def testMultiUnionLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("031_multiUnion.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["multiunion1"]), -1)

    def testScaledLoad(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("032_scaled.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))
        #self.assertEqual(getSolidChecksum(registry.solidDict["box1Scaled"]), -1)

    def testMaterials(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("201_materials.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testOpticalSurfaces(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("150_opticalsurfaces.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testDivisionVolume_box_x(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("124_division_box_x.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_box_y(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("125_division_box_y.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_box_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("126_division_box_z.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_tubs_rho(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("127_division_tubs_rho.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_tubs_phi(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("128_division_tubs_phi.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_tubs_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("129_division_tubs_z.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_cons_rho(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("130_division_cons_rho.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_cons_phi(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("131_division_cons_phi.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_cons_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("132_division_cons_z.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_trd_x(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("133_division_trd_x.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_trd_y(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("134_division_trd_y.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_trd_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("135_division_trd_z.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_para_x(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("136_division_para_x.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename))  # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_para_y(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("137_division_para_y.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_para_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("138_division_para_z.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_polycone_rho(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("139_division_polycone_rho.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_polycone_phi(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("140_division_polycone_phi.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_polycone_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("141_division_polycone_z.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_polyhedra_rho(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("142_division_polyhedra_rho.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_polyhedra_phi(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("143_division_polyhedra_phi.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename))   # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testDivisionVolume_polyhedra_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("144_division_polyhedra_z.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "division":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testReplicaVolume_x(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("106_replica_x.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "replica":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testReplicaVolume_y(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("107_replica_y.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "replica":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testReplicaVolume_z(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("108_replica_z.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "replica":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testReplicaVolume_phi(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("109_replica_phi.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "replica":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testReplicaVolume_rho(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("110_replica_rho.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "replica":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_box(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("111_parameterised_box.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_tube(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("112_parameterised_tube.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_cone(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("113_parameterised_cone.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_orb(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("114_parameterised_orb.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_sphere(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("115_parameterised_sphere.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename)) # Faulty in Geant4

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_torus(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("116_parameterised_torus.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_hype(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("117_parameterised_hype.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_para(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("118_parameterised_para.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_trd(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("119_parameterised_trd.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_trap(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("120_parameterised_trap.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_polycone(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("121_parameterised_polycone.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_polyhedron(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("122_parameterised_polyhedron.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid
        #self.assertEqual(getSolidChecksum(solid), -1)

    def testParameterisedVolume_ellipsoid(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("123_parameterised_ellipsoid.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

        for volname, volume in registry.physicalVolumeDict.iteritems():
            if volume.type == "parametrised":
                solid= volume.meshes[0].solid

    def testAuxiliary(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("202_auxiliary.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testEntity(self):
        # Need to process the GDML file to inject the absolute path to the entity file
        with open(_pj("203_entity.gdml")) as infile:
            contents = infile.read()

            contents_replaced = contents.replace("203_materials.xml", _pj("203_materials.xml"))
            with open(_pj("203_temp.gdml"), "w") as tempfile:
                tempfile.write(contents_replaced)

        registry, writtenFilename = pyg4ometryLoadWriteTest("203_temp.gdml")
        _os.unlink(_pj("203_temp.gdml"))
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testChargeExhangeMC(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/ChargeExchangeMC/lht.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Overlaps in the original file

    def testG01assembly(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/assembly.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Overlaps in the original file

    def testG01auxiliary(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/auxiliary.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01axes(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/axes.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Overlaps in the original file

    def testG01divisionvol(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/divisionvol.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01mat_nist(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/mat_nist.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01multiUnion(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/multiUnion.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01pTube(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/pTube.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01parameterized(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/parameterized.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01replicated(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/replicated.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01scale(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/scale.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01solids(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/solids.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG01tess(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G01/tess.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG02test(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G02/test.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testG04auxiliary(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/G04/auxiliary.gdml")
        self.assertTrue(geant4LoadTest(writtenFilename))

    def testPar02FullDetector(self):
        registry, writtenFilename = pyg4ometryLoadWriteTest("../gdmlG4examples/Par02/Par02FullDetector.gdml")
        #self.assertTrue(geant4LoadTest(writtenFilename)) # Overlaps in the orignal file

if __name__ == '__main__':
    _unittest.main(verbosity=2)
