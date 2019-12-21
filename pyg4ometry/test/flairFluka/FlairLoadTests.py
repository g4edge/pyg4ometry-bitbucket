import unittest as _unittest

import os as _os

import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi
import pyg4ometry.gdml as _gdml
from pyg4ometry.convert import fluka2Geant4 as _fluka2Geant4


def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

def flairLoadWriteTest(fileName, vis=True, interactive=False) :
    r = _fluka.Reader(_pj(fileName))

    greg = _fluka2Geant4(r.flukaregistry)

    wlv = greg.getWorldVolume()

    if vis:
        v = _vi.VtkViewer()
        v.addAxes(length=20)
        wlv.checkOverlaps()
        v.addLogicalVolume(wlv)
        v.view(interactive)

    w = _gdml.Writer()
    w.addDetector(greg)

    gdmlFileName = fileName.replace(".inp", ".gdml")
    gmadFileName  = fileName.replace(".inp", ".gmad")

    w.write(_os.path.join(_os.path.dirname(__file__), gdmlFileName))
    w.writeGmadTester(_os.path.join(_os.path.dirname(__file__),gmadFileName),gdmlFileName)

class FlairLoadTests(_unittest.TestCase) :
    def test_FlairLoad_T001_RPP(self):
        flairLoadWriteTest("001_RPP.inp",True,False)

    def test_FlairLoad_T002_BOX(self):
        flairLoadWriteTest("002_BOX.inp",True,False)

    def test_FlairLoad_T003_SPH(self):
        flairLoadWriteTest("003_SPH.inp",True,False)

    def test_FlairLoad_T004_RCC(self):
        flairLoadWriteTest("004_RCC.inp",True,False)

    def test_FlairLoad_T005_REC(self):
        flairLoadWriteTest("005_REC.inp",True,False)

    def test_FlairLoad_T006_TRC(self):
        flairLoadWriteTest("006_TRC.inp",True,False)

    def test_FlairLoad_T007_ELL(self):
        flairLoadWriteTest("007_ELL.inp",True,False)

    def test_FlairLoad_T011_XYP(self):
        flairLoadWriteTest("011_XYP.inp",True,False)

    def test_FlairLoad_T012_XZP(self):
        flairLoadWriteTest("012_XZP.inp",True,False)

    def test_FlairLoad_T013_YZP(self):
        flairLoadWriteTest("013_YZP.inp",True,False)

    def test_FlairLoad_T014_PLA(self):
        flairLoadWriteTest("014_PLA.inp",True,False)

    def test_FlairLoad_T015_XCC(self):
        flairLoadWriteTest("015_XCC.inp",True,False)

    def test_FlairLoad_T016_YCC(self):
        flairLoadWriteTest("016_YCC.inp",True,False)

    def test_FlairLoad_T017_ZCC(self):
        flairLoadWriteTest("017_ZCC.inp",True,False)

    def test_FlairLoad_T018_XEC(self):
        flairLoadWriteTest("018_XEC.inp",True,False)

    def test_FlairLoad_T019_YEC(self):
        flairLoadWriteTest("019_YEC.inp",True,False)

    def test_FlairLoad_T020_ZEC(self):
        flairLoadWriteTest("020_ZEC.inp",True,False)

    def test_FlairLoad_T021_QUA(self):
        flairLoadWriteTest("021_QUA.inp", True, False)

    def test_FlairLoad_T050_RPP_Translate(self):
        flairLoadWriteTest("050_RPP_Translate.inp",True,False)

    def test_FlairLoad_T051_RPP_Expansion(self):
        flairLoadWriteTest("051_RPP_Expansion.inp",True,False)

    def test_FlairLoad_T052_RPP_RotDefi(self):
        flairLoadWriteTest("052_RPP_RotDefi.inp",True,False)

    def test_FlairLoad_T053_RPP_RotDefi2(self):
        flairLoadWriteTest("053_RPP_RotDefi2.inp",True,False)

    def test_FlairLoad_T054_RPP_TranslateExpansionRotDefi(self):
        flairLoadWriteTest("054_RPP_TranslateExpansionRotDefi.inp",True,False)

    def test_FlairLoad_T100_Multiple(self):
        flairLoadWriteTest("100_Multiple.inp",True,False)

    def test_FlairLoad_T101_Intersection(self):
        flairLoadWriteTest("101_Intersection.inp",True,False)

    def test_FlairLoad_T102_Difference(self):
        flairLoadWriteTest("102_Difference.inp",True,False)

    def test_FlairLoad_T103_Union(self):
        flairLoadWriteTest("103_Union.inp",True,False)
