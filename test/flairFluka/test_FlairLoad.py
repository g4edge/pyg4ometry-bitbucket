import os as _os

import pyg4ometry.fluka as _fluka
import pyg4ometry.visualisation as _vi
import pyg4ometry.gdml as _gdml
from pyg4ometry.convert import fluka2Geant4 as _fluka2Geant4
import pyg4ometry.geant4.solid

def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

def flairLoadWriteTest(fileName, vis=True, interactive=False,
                       quadricRegionAABBs=None):
    r = _fluka.Reader(_pj(fileName))

    greg = _fluka2Geant4(r.flukaregistry, quadricRegionAABBs=quadricRegionAABBs)

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

    return r.flukaregistry, greg

def test_FlairLoad_T001_RPP():
    flairLoadWriteTest("001_RPP.inp", False, False)

def test_FlairLoad_T002_BOX():
    flairLoadWriteTest("002_BOX.inp", False, False)

def test_FlairLoad_T003_SPH():
    flairLoadWriteTest("003_SPH.inp", False, False)

def test_FlairLoad_T004_RCC():
    flairLoadWriteTest("004_RCC.inp", False, False)

def test_FlairLoad_T005_REC():
    flairLoadWriteTest("005_REC.inp", False, False)

def test_FlairLoad_T006_TRC():
    flairLoadWriteTest("006_TRC.inp", False, False)

def test_FlairLoad_T007_ELL():
    flairLoadWriteTest("007_ELL.inp", False, False)

def test_FlairLoad_T009_ARB():
    flairLoadWriteTest("009_ARB.inp", False, False)

def test_FlairLoad_T009_ARB_cube_anticlockwise():
    flairLoadWriteTest("009_ARB_cube_anticlockwise.inp", False, False)

def test_FlairLoad_T009_ARB_cube_clockwise():
    flairLoadWriteTest("009_ARB_cube_clockwise.inp", False, False)

def test_FlairLoad_T011_XYP():
    flairLoadWriteTest("011_XYP.inp", False, False)

def test_FlairLoad_T012_XZP():
    flairLoadWriteTest("012_XZP.inp", False, False)

def test_FlairLoad_T013_YZP():
    flairLoadWriteTest("013_YZP.inp", False, False)

def test_FlairLoad_T014_PLA():
    flairLoadWriteTest("014_PLA.inp", False, False)

def test_FlairLoad_T015_XCC():
    flairLoadWriteTest("015_XCC.inp", False, False)

def test_FlairLoad_T016_YCC():
    flairLoadWriteTest("016_YCC.inp", False, False)

def test_FlairLoad_T017_ZCC():
    flairLoadWriteTest("017_ZCC.inp", False, False)

def test_FlairLoad_T018_XEC():
    flairLoadWriteTest("018_XEC.inp", False, False)

def test_FlairLoad_T019_YEC():
    flairLoadWriteTest("019_YEC.inp", False, False)

def test_FlairLoad_T020_ZEC():
    flairLoadWriteTest("020_ZEC.inp", False, False)

def test_FlairLoad_T021_QUA():
    quaAABB = {"QUA_REG": _fluka.AABB([-150., 100., 0],
                                      [150., 200., 1000.])}
    flairLoadWriteTest("021_QUA.inp", False, False,
                       quadricRegionAABBs=quaAABB)

def test_FlairLoad_T050_RPP_Translate():
    flairLoadWriteTest("050_RPP_Translate.inp", False, False)

def test_FlairLoad_T051_RPP_Expansion():
    flairLoadWriteTest("051_RPP_Expansion.inp", False, False)

def test_FlairLoad_T052_RPP_RotDefi():
    flairLoadWriteTest("052_RPP_RotDefi.inp", False, False)

def test_FlairLoad_T053_RPP_RotDefi2():
    flairLoadWriteTest("053_RPP_RotDefi2.inp", False, False)

def test_FlairLoad_T054_RPP_TranslateExpansionRotDefi():
    flairLoadWriteTest("054_RPP_TranslateExpansionRotDefi.inp", False, False)

def test_FlairLoad_T100_Multiple():
    flairLoadWriteTest("100_Multiple.inp", False, False)

def test_FlairLoad_T101_Intersection():
    flairLoadWriteTest("101_Intersection.inp", False, False)

def test_FlairLoad_T102_Difference():
    flairLoadWriteTest("102_Difference.inp", False, False)

def test_FlairLoad_T103_Union():
    flairLoadWriteTest("103_Union.inp", False, False)

def test_FlairLoad_T104_Union():
    flairLoadWriteTest("104_shift_cylinders.inp", False, False)

def test_FlairLoad_T301_RPP_transform():
    flairLoadWriteTest("301_RPP_transform.inp", False, False)

def test_FlairLoad_T302_BOX_transform():
    flairLoadWriteTest("302_BOX_transform.inp", False, False)

def test_FlairLoad_T303_SPH_transform():
    flairLoadWriteTest("303_SPH_transform.inp", False, False)

def test_FlairLoad_T304_RCC_transform():
    flairLoadWriteTest("304_RCC_transform.inp", False, False)

def test_FlairLoad_T305_REC_transform():
    flairLoadWriteTest("305_REC_transform.inp", False, False)

def test_FlairLoad_T306_TRC_transform():
    flairLoadWriteTest("306_TRC_transform.inp", False, False)

def test_FlairLoad_T307_ELL_transform():
    flairLoadWriteTest("307_ELL_transform.inp", False, False)

def test_FlairLoad_T308_RAW_transform():
    flairLoadWriteTest("308_RAW_transform.inp", False, False)

def test_FlairLoad_T308_WED_transform():
    flairLoadWriteTest("308_WED_transform.inp", False, False)

def test_FlairLoad_T309_ARB_transform():
    flairLoadWriteTest("309_ARB_transform.inp", False, False)

def test_FlairLoad_T310_XYP_transform():
    flairLoadWriteTest("310_XYP_transform.inp", False, False)

def test_FlairLoad_T310_XZP_transform():
    flairLoadWriteTest("310_XZP_transform.inp", False, False)

def test_FlairLoad_T310_YZP_transform():
    flairLoadWriteTest("310_YZP_transform.inp", False, False)

def test_FlairLoad_T311_PLA_transform():
    flairLoadWriteTest("311_PLA_transform.inp", False, False)

def test_FlairLoad_T312_XCC_transform():
    flairLoadWriteTest("312_XCC_transform.inp", False, False)

def test_FlairLoad_T312_YCC_transform():
    flairLoadWriteTest("312_YCC_transform.inp", False, False)

def test_FlairLoad_T312_ZCC_transform():
    flairLoadWriteTest("312_ZCC_transform.inp", False, False)

def test_FlairLoad_T313_XEC_transform():
    flairLoadWriteTest("313_XEC_transform.inp", False, False)

def test_FlairLoad_T313_YEC_transform():
    flairLoadWriteTest("313_YEC_transform.inp", False, False)

def test_FlairLoad_T313_ZEC_transform():
    flairLoadWriteTest("313_ZEC_transform.inp", False, False)

def test_FlairLoad_T314_QUA_transform():
    quaAABB = {"QUA_REG": _fluka.AABB([-190., 40., 0], [50., 200., 1000.])}
    flairLoadWriteTest("314_QUA_transform.inp", False, False,
                       quadricRegionAABBs=quaAABB)

def test_FlairLoad_T320_cube_from_halfspaces_transform():
    flairLoadWriteTest("320_cube_from_halfspaces_transform.inp", False, False)

def test_FlairLoad_T321_cube_from_plas_transform():
    flairLoadWriteTest("321_cube_from_plas_transform.inp", False, False)

def test_FlairLoad_T514_QUA_expansion():
    quaAABB = {"QUA_REG": _fluka.AABB([-70., 50., 0], [70., 100., 500.])}
    flairLoadWriteTest("514_QUA_expansion.inp", False, False,
                       quadricRegionAABBs=quaAABB)

def test_FlairLoad_T514_QUA_translation():
    quaAABB = {"QUA_REG": _fluka.AABB([-150., 100., -1000.],
                                      [150., 200., 0.])}
    flairLoadWriteTest("514_QUA_translation.inp", False, False,
                       quadricRegionAABBs=quaAABB)

def test_FlairLoad_T514_QUA_rototranslation():
    quaAABB = {"QUA_REG": _fluka.AABB([-190., 40., 0], [50., 200., 1000.])}
    flairLoadWriteTest("514_QUA_rototranslation.inp", False, False,
                       quadricRegionAABBs=quaAABB)

def test_FlairLoad_T514_QUA_coplanar():
    quaAABB = {"OUTER": _fluka.AABB([-200., 0., 0.], [200, 200, 1100]),
               "INNER": _fluka.AABB([-100., 50., 250], [100., 150., 850.])}
    flairLoadWriteTest("514_QUA_coplanar.inp", False, False,
                       quadricRegionAABBs=quaAABB)

def test_FlairLoad_T601_filter_redundant_halfspaces():
    flairLoadWriteTest("601_filter_redundant_halfspaces.inp", False, False)

def test_FlairLoad_T701_LATTICE():
    flairLoadWriteTest("701_LATTICE.inp", False, False)

def test_FlairLoad_T702_LATTICE():
    flairLoadWriteTest("702_LATTICE.inp", False, False)

def test_FlairLoad_T703_LATTICE():
    flairLoadWriteTest("703_LATTICE.inp", False, False)

def test_FlairLoad_T801_nested_expansion():
    flairLoadWriteTest("801_nested_expansion.inp", False, False)

def test_FlairLoad_T802_nested_translation():
    flairLoadWriteTest("802_nested_translation.inp", False, False)

def test_FlairLoad_T803_nested_transform():
    flairLoadWriteTest("803_nested_transform.inp", False, False)

def test_FlairLoad_T804_recursive_transform():
    flairLoadWriteTest("804_recursive_transform.inp", False, False)

def test_FlairLoad_T805_inverse_transform():
    flairLoadWriteTest("805_inverse_transform.inp", False, False)

def test_FlairLoad_T806_combined_translat_transform():
    flairLoadWriteTest("806_combined_translat_transform.inp", False, False)

def test_FlairLoad_T901_preprocessor_if():
    freg, greg = flairLoadWriteTest("901_preprocessor_if.inp", False, False)
    solids = greg.solidDict
    assert(isinstance(solids["bb1_s"], pyg4ometry.geant4.solid.Cons))

def test_FlairLoad_T902_preprocessor_elif():
    freg, greg = flairLoadWriteTest("902_preprocessor_elif.inp",
                                    False, False)
    solids = greg.solidDict
    assert(isinstance(solids["bb1_s"], pyg4ometry.geant4.solid.Box))

def test_FlairLoad_T903_preprocessor_else():
    freg, greg = flairLoadWriteTest("903_preprocessor_else.inp",
                                    False, False)
    solids = greg.solidDict
    assert(isinstance(solids["bb1_s"], pyg4ometry.geant4.solid.Tubs))

def test_FlairLoad_T904_preprocessor_include():
    flairLoadWriteTest("904_preprocessor_include.inp", False, False)

def test_FlairLoad_T905_preprocessor_nested_if():
    freg, greg = flairLoadWriteTest("905_preprocessor_nested_if.inp",
                       False, False)
    solids = greg.solidDict
    assert(isinstance(solids["bb1_s"], pyg4ometry.geant4.solid.Cons))

def test_FlairLoad_T906_preprocessor_nested_elif():
    freg, greg = flairLoadWriteTest("906_preprocessor_nested_elif.inp",
                                    False, False)
    solids = greg.solidDict
    assert(isinstance(solids["bb1_s"], pyg4ometry.geant4.solid.Box))

def test_FlairLoad_T907_preprocessor_nested_else():
    freg, greg = flairLoadWriteTest("907_preprocessor_nested_else.inp",
                                    False, False)
    solids = greg.solidDict
    assert(isinstance(solids["bb1_s"], pyg4ometry.geant4.solid.Box))

def test_FlairLoad_T908_preprocessor_define():
    flairLoadWriteTest("908_preprocessor_define.inp", False, False)

def test_FlairLoad_Tex_geometry():
    flairLoadWriteTest("ex-geometry.inp", False, False)

def test_FlairLoad_Tex_Scoring():
    flairLoadWriteTest("ex_Scoring.inp", False, False)

def test_FlairLoad_Texample_running():
    flairLoadWriteTest("example_running.inp", False, False)

def test_FlairLoad_Texample_score():
    flairLoadWriteTest("example_score.inp", False, False)

def test_FlairLoad_TmanualSimpleFileFixed():
    flairLoadWriteTest("manualSimpleFileFixed.inp", False, False)

def test_FlairLoad_TmanualSimpleFileFree():
    flairLoadWriteTest("manualSimpleFileFree.inp", False, False)

#def test_FlairLoad_TcorrectorDipole():
#    flairLoadWriteTest("corrector-dipole.inp", False, False)

