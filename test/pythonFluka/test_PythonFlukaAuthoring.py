from random import random
import numpy as np
import pytest as _pytest

from pyg4ometry.fluka.fluka_registry import RotoTranslationStore, FlukaRegistry
from pyg4ometry.fluka.directive import rotoTranslationFromTra2

from . import T001_RPP
from . import T002_BOX
from . import T003_SPH
from . import T004_RCC
from . import T005_REC
from . import T006_TRC
from . import T007_ELL
from . import T008_RAW
from . import T008_WED
from . import T009_ARB
from . import T010_XYP
from . import T010_XZP
from . import T010_YZP
from . import T011_PLA
from . import T012_XCC
from . import T012_YCC
from . import T012_ZCC
from . import T013_XEC
from . import T013_YEC
from . import T013_ZEC
from . import T014_QUA

from . import T051_expansion
from . import T052_translation
from . import T090_lattice

from . import T101_region_one_body
from . import T102_region_intersection_two_bodies
from . import T103_region_subtraction_two_bodies
from . import T103_region_subtraction_two_bodies_RCC
from . import T104_region_union_two_zones
from . import T104_region_union_two_zones_2
from . import T105_region_subzone_subtraction
from . import T106_region_subzone_subtraction_with_union
from . import T107_region_union_with_reused_bodies

from . import T201_RPP_coplanar
from . import T202_BOX_coplanar
from . import T203_SPH_coplanar
from . import T204_RCC_coplanar
from . import T205_REC_coplanar
from . import T206_TRC_coplanar
from . import T207_ELL_coplanar
from . import T208_RAW_coplanar
from . import T208_WED_coplanar
from . import T209_ARB_coplanar
from . import T210_PLA_coplanar
from . import T210_XYP_coplanar
from . import T210_XZP_coplanar
from . import T210_YZP_coplanar
from . import T212_XCC_coplanar
from . import T212_YCC_coplanar
from . import T212_ZCC_coplanar
from . import T213_XEC_coplanar
from . import T213_YEC_coplanar
from . import T213_ZEC_coplanar
from . import T214_QUA_coplanar

from . import T401_RPP_expansion
from . import T402_BOX_expansion
from . import T403_SPH_expansion
from . import T404_RCC_expansion
from . import T405_REC_expansion
from . import T406_TRC_expansion
from . import T407_ELL_expansion
from . import T408_RAW_expansion
from . import T408_WED_expansion
from . import T409_ARB_expansion
from . import T410_XYP_expansion
from . import T410_XZP_expansion
from . import T410_YZP_expansion
from . import T411_PLA_expansion
from . import T412_XCC_expansion
from . import T412_YCC_expansion
from . import T412_ZCC_expansion
from . import T413_XEC_expansion
from . import T413_YEC_expansion
from . import T413_ZEC_expansion
from . import T414_QUA_expansion
from . import T501_RPP_translation
from . import T502_BOX_translation
from . import T503_SPH_translation
from . import T504_RCC_translation
from . import T505_REC_translation
from . import T506_TRC_translation
from . import T507_ELL_translation
from . import T508_RAW_translation
from . import T508_WED_translation
from . import T509_ARB_translation
from . import T510_XYP_translation
from . import T510_XZP_translation
from . import T510_YZP_translation
from . import T511_PLA_translation
from . import T512_XCC_translation
from . import T512_YCC_translation
from . import T512_ZCC_translation
from . import T513_XEC_translation
from . import T513_YEC_translation
from . import T513_ZEC_translation
from . import T514_QUA_translation

from . import T601_RPP_rototranslation
from . import T602_BOX_rototranslation
from . import T603_SPH_rototranslation
from . import T604_RCC_rototranslation
from . import T605_REC_rototranslation
from . import T606_TRC_rototranslation
from . import T607_ELL_rototranslation
from . import T608_RAW_rototranslation
from . import T608_WED_rototranslation
from . import T609_ARB_rototranslation
from . import T610_XYP_rototranslation
from . import T610_XZP_rototranslation
from . import T610_YZP_rototranslation
from . import T611_PLA_rototranslation
from . import T612_XCC_rototranslation
from . import T612_YCC_rototranslation
from . import T612_ZCC_rototranslation
from . import T613_XEC_rototranslation
from . import T613_YEC_rototranslation
from . import T613_ZEC_rototranslation
from . import T614_QUA_rototranslation

from . import T710_XYP_XZP_YZP_minimisation
from . import T711_PLA_minimisation
from . import T712_XCC_minimisation
from . import T712_YCC_minimisation
from . import T712_ZCC_minimisation
from . import T713_XEC_minimisation
from . import T713_YEC_minimisation
from . import T713_ZEC_minimisation

from . import T801_filter_redundant_halfspaces
from . import T803_material_element

from . import T901_cube_from_XYP_XZP_YZP
from . import T902_cube_from_six_PLAs

def test_PythonFluka_T001_RPP():
    T001_RPP.Test(False, False)

def test_PythonFluka_T002_BOX():
    T002_BOX.Test(False, False)

def test_PythonFluka_T003_SPH():
    T003_SPH.Test(False, False)

def test_PythonFluka_T004_RCC():
    T004_RCC.Test(False, False)

def test_PythonFluka_T005_REC():
    T005_REC.Test(False, False)

def test_PythonFluka_T006_TRC():
    T006_TRC.Test(False, False)

def test_PythonFluka_T007_ELL():
    T007_ELL.Test(False, False)

def test_PythonFluka_T008_RAW():
    T008_RAW.Test(False, False)

def test_PythonFluka_T008_WED():
    T008_WED.Test(False, False)

def test_PythonFluka_T009_ARB():
    T009_ARB.Test(False, False)

def test_PythonFluka_T010_XYP():
    T010_XYP.Test(False, False)

def test_PythonFluka_T010_XZP():
    T010_XZP.Test(False, False)

def test_PythonFluka_T010_YZP():
    T010_YZP.Test(False, False)

def test_PythonFluka_T011_PLA():
    T011_PLA.Test(False, False)

def test_PythonFluka_T012_XCC():
    T012_XCC.Test(False, False)

def test_PythonFluka_T012_YCC():
    T012_YCC.Test(False, False)

def test_PythonFluka_T012_ZCC():
    T012_ZCC.Test(False, False)

def test_PythonFluka_T013_XEC():
    T013_XEC.Test(False, False)

def test_PythonFluka_T013_YEC():
    T013_YEC.Test(False, False)

def test_PythonFluka_T013_ZEC():
    T013_ZEC.Test(False, False)

def test_PythonFluka_T014_QUA():
    T014_QUA.Test(False, False)

def test_PythonFluka_T051_expansion():
    T051_expansion.Test(False, False)

def test_PythonFluka_T052_translation():
    T052_translation.Test(False, False)

def test_PythonFluka_T090_lattice():
    T090_lattice.Test(False, False)


# 1111111111
def test_PythonFluka_T101_region_one_body():
    T101_region_one_body.Test(False, False)

def test_PythonFluka_T102_region_intersection_two_bodies():
    T102_region_intersection_two_bodies.Test(False, False)

def test_PythonFluka_T103_region_subtraction_two_bodies():
    T103_region_subtraction_two_bodies.Test(False, False)

def test_PythonFluka_T103_region_subtraction_two_bodies_RCC():
    T103_region_subtraction_two_bodies_RCC.Test(False, False)

def test_PythonFluka_T104_region_union_two_zones():
    T104_region_union_two_zones.Test(False, False)

def test_PythonFluka_T104_region_union_two_zones_2():
    T104_region_union_two_zones_2.Test(False, False)

def test_PythonFluka_T105_region_subzone_subtraction():
    T105_region_subzone_subtraction.Test(False, False)

def test_PythonFluka_T106_region_subzone_subtraction_with_union():
    T106_region_subzone_subtraction_with_union.Test(False, False)

def test_PythonFluka_T107_region_union_with_reused_bodies():
    T107_region_union_with_reused_bodies.Test(False, False)


# 2222222222
def test_PythonFluka_T201_RPP_coplanar():
    T201_RPP_coplanar.Test(False, False)

def test_PythonFluka_T202_BOX_coplanar():
    T202_BOX_coplanar.Test(False, False)

def test_PythonFluka_T203_SPH_coplanar():
    T203_SPH_coplanar.Test(False, False)

def test_PythonFluka_T204_RCC_coplanar():
    T204_RCC_coplanar.Test(False, False)

def test_PythonFluka_T205_REC_coplanar():
    T205_REC_coplanar.Test(False, False)

def test_PythonFluka_T206_TRC_coplanar():
    T206_TRC_coplanar.Test(False, False)

def test_PythonFluka_T207_ELL_coplanar():
    T207_ELL_coplanar.Test(False, False)

def test_PythonFluka_T208_RAW_coplanar():
    T208_RAW_coplanar.Test(False, False)

def test_PythonFluka_T208_WED_coplanar():
    T208_WED_coplanar.Test(False, False)

def test_PythonFluka_T209_ARB_coplanar():
    T209_ARB_coplanar.Test(False, False)

def test_PythonFluka_T210_PLA_coplanar():
    T210_PLA_coplanar.Test(False, False)

def test_PythonFluka_T210_XYP_coplanar():
    T210_XYP_coplanar.Test(False, False)

def test_PythonFluka_T210_XZP_coplanar():
    T210_XZP_coplanar.Test(False, False)

def test_PythonFluka_T210_YZP_coplanar():
    T210_YZP_coplanar.Test(False, False)

def test_PythonFluka_T212_XCC_coplanar():
    T212_XCC_coplanar.Test(False, False)

def test_PythonFluka_T212_YCC_coplanar():
    T212_YCC_coplanar.Test(False, False)

def test_PythonFluka_T212_ZCC_coplanar():
    T212_ZCC_coplanar.Test(False, False)

def test_PythonFluka_T213_XEC_coplanar():
    T213_XEC_coplanar.Test(False, False)

def test_PythonFluka_T213_YEC_coplanar():
    T213_YEC_coplanar.Test(False, False)

def test_PythonFluka_T213_ZEC_coplanar():
    T213_ZEC_coplanar.Test(False, False)

def test_PythonFluka_T214_QUA_coplanar():
    T214_QUA_coplanar.Test(False, False)

# 4444444444
def test_PythonFluka_T401_RPP_expansion():
    T401_RPP_expansion.Test(False, False)

def test_PythonFluka_T402_BOX_expansion():
    T402_BOX_expansion.Test(False, False)

def test_PythonFluka_T403_SPH_expansion():
    T403_SPH_expansion.Test(False, False)

def test_PythonFluka_T404_RCC_expansion():
    T404_RCC_expansion.Test(False, False)

def test_PythonFluka_T405_REC_expansion():
    T405_REC_expansion.Test(False, False)

def test_PythonFluka_T406_TRC_expansion():
    T406_TRC_expansion.Test(False, False)

def test_PythonFluka_T407_ELL_expansion():
    T407_ELL_expansion.Test(False, False)

def test_PythonFluka_T408_RAW_expansion():
    T408_RAW_expansion.Test(False, False)

def test_PythonFluka_T408_WED_expansion():
    T408_WED_expansion.Test(False, False)

def test_PythonFluka_T409_ARB_expansion():
    T409_ARB_expansion.Test(False, False)

def test_PythonFluka_T410_XYP_expansion():
    T410_XYP_expansion.Test(False, False)

def test_PythonFluka_T410_XZP_expansion():
    T410_XZP_expansion.Test(False, False)

def test_PythonFluka_T410_YZP_expansion():
    T410_YZP_expansion.Test(False, False)

def test_PythonFluka_T411_PLA_expansion():
    T411_PLA_expansion.Test(False, False)

def test_PythonFluka_T412_XCC_expansion():
    T412_XCC_expansion.Test(False, False)

def test_PythonFluka_T412_YCC_expansion():
    T412_YCC_expansion.Test(False, False)

def test_PythonFluka_T412_ZCC_expansion():
    T412_ZCC_expansion.Test(False, False)

def test_PythonFluka_T413_XEC_expansion():
    T413_XEC_expansion.Test(False, False)

def test_PythonFluka_T413_YEC_expansion():
    T413_YEC_expansion.Test(False, False)

def test_PythonFluka_T413_ZEC_expansion():
    T413_ZEC_expansion.Test(False, False)

def test_PythonFluka_T414_QUA_expansion():
    T414_QUA_expansion.Test(False, False)

def test_PythonFluka_T501_RPP_translation():
    T501_RPP_translation.Test(False, False)

def test_PythonFluka_T502_BOX_translation():
    T502_BOX_translation.Test(False, False)

def test_PythonFluka_T503_SPH_translation():
    T503_SPH_translation.Test(False, False)

def test_PythonFluka_T504_RCC_translation():
    T504_RCC_translation.Test(False, False)

def test_PythonFluka_T505_REC_translation():
    T505_REC_translation.Test(False, False)

def test_PythonFluka_T506_TRC_translation():
    T506_TRC_translation.Test(False, False)

def test_PythonFluka_T507_ELL_translation():
    T507_ELL_translation.Test(False, False)

def test_PythonFluka_T508_RAW_translation():
    T508_RAW_translation.Test(False, False)

def test_PythonFluka_T508_WED_translation():
    T508_WED_translation.Test(False, False)

def test_PythonFluka_T509_ARB_translation():
    T509_ARB_translation.Test(False, False)

def test_PythonFluka_T510_XYP_translation():
    T510_XYP_translation.Test(False, False)

def test_PythonFluka_T510_XZP_translation():
    T510_XZP_translation.Test(False, False)

def test_PythonFluka_T510_YZP_translation():
    T510_YZP_translation.Test(False, False)

def test_PythonFluka_T511_PLA_translation():
    T511_PLA_translation.Test(False, False)

def test_PythonFluka_T512_XCC_translation():
    T512_XCC_translation.Test(False, False)

def test_PythonFluka_T512_YCC_translation():
    T512_YCC_translation.Test(False, False)

def test_PythonFluka_T512_ZCC_translation():
    T512_ZCC_translation.Test(False, False)

def test_PythonFluka_T513_XEC_translation():
    T513_XEC_translation.Test(False, False)

def test_PythonFluka_T513_YEC_translation():
    T513_YEC_translation.Test(False, False)

def test_PythonFluka_T513_ZEC_translation():
    T513_ZEC_translation.Test(False, False)

def test_PythonFluka_T514_QUA_translation():
    T514_QUA_translation.Test(False, False)


# 6666666666
def test_PythonFluka_T601_RPP_rototranslation():
    T601_RPP_rototranslation.Test(False, False)

def test_PythonFluka_T602_BOX_rototranslation():
    T602_BOX_rototranslation.Test(False, False)

def test_PythonFluka_T603_SPH_rototranslation():
    T603_SPH_rototranslation.Test(False, False)

def test_PythonFluka_T604_RCC_rototranslation():
    T604_RCC_rototranslation.Test(False, False)

def test_PythonFluka_T605_REC_rototranslation():
    T605_REC_rototranslation.Test(False, False)

def test_PythonFluka_T606_TRC_rototranslation():
    T606_TRC_rototranslation.Test(False, False)

def test_PythonFluka_T607_ELL_rototranslation():
    T607_ELL_rototranslation.Test(False, False)

def test_PythonFluka_T608_RAW_rototranslation():
    T608_RAW_rototranslation.Test(False, False)

def test_PythonFluka_T608_WED_rototranslation():
    T608_WED_rototranslation.Test(False, False)

def test_PythonFluka_T609_ARB_rototranslation():
    T609_ARB_rototranslation.Test(False, False)

def test_PythonFluka_T610_XYP_rototranslation():
    T610_XYP_rototranslation.Test(False, False)

def test_PythonFluka_T610_XZP_rototranslation():
    T610_XZP_rototranslation.Test(False, False)

def test_PythonFluka_T610_YZP_rototranslation():
    T610_YZP_rototranslation.Test(False, False)

def test_PythonFluka_T611_PLA_rototranslation():
    T611_PLA_rototranslation.Test(False, False)

def test_PythonFluka_T612_XCC_rototranslation():
    T612_XCC_rototranslation.Test(False, False)

def test_PythonFluka_T612_YCC_rototranslation():
    T612_YCC_rototranslation.Test(False, False)

def test_PythonFluka_T612_ZCC_rototranslation():
    T612_ZCC_rototranslation.Test(False, False)

def test_PythonFluka_T613_XEC_rototranslation():
    T613_XEC_rototranslation.Test(False, False)

def test_PythonFluka_T613_YEC_rototranslation():
    T613_YEC_rototranslation.Test(False, False)

def test_PythonFluka_T613_ZEC_rototranslation():
    T613_ZEC_rototranslation.Test(False, False)

def test_PythonFluka_T614_QUA_rototranslation():
    T614_QUA_rototranslation.Test(False, False)


# 7777777777
def test_PythonFluka_T710_XYP_XZP_YZP_minimisation():
    T710_XYP_XZP_YZP_minimisation.Test(False, False)

def test_PythonFluka_T711_PLA_minimisation():
    T711_PLA_minimisation.Test(False, False)

def test_PythonFluka_T712_XCC_minimisation():
    T712_XCC_minimisation.Test(False, False)

def test_PythonFluka_T712_YCC_minimisation():
    T712_YCC_minimisation.Test(False, False)

def test_PythonFluka_T712_ZCC_minimisation():
    T712_ZCC_minimisation.Test(False, False)

def test_PythonFluka_T713_XEC_minimisation():
    T713_XEC_minimisation.Test(False, False)

def test_PythonFluka_T713_YEC_minimisation():
    T713_YEC_minimisation.Test(False, False)

def test_PythonFluka_T713_ZEC_minimisation():
    T713_ZEC_minimisation.Test(False, False)


# 8888888888
def test_PythonFluka_T801_filter_redundant_halfspaces():
    T801_filter_redundant_halfspaces.Test(False, False)

def test_PythonFluka_T803_material_element():
    T803_material_element.Test(False, False)


# 9999999999
def test_PythonFluka_T901_cube_from_XYP_XZP_YZP():
    T901_cube_from_XYP_XZP_YZP.Test(False, False)

def test_PythonFluka_T902_cube_from_six_PLAs():
    T902_cube_from_six_PLAs.Test(False, False)


def test_PythonFluka_empyRegistry():

    import pyg4ometry.convert as convert
    from pyg4ometry.fluka import FlukaRegistry

    freg = FlukaRegistry()
    try :
        greg = convert.fluka2Geant4(freg)
    except ValueError :
        pass


def _makeRotoTranslation( name="rppTRF"):
    angle = random() * np.pi
    rtrans = rotoTranslationFromTra2(name,
                                     [[angle, angle, angle],
                                      [0, 0, 20]])
    return name, rtrans

def _makeStore():
    return RotoTranslationStore()

def test_storeInit():
    _makeStore()

def test_gettingRotoTranslation():
    name, rtrans = _makeRotoTranslation()
    store = _makeStore()
    store[name] = rtrans
    r = store[name]

def test_RotoTranslation_fails_setting_with_wrong_name():
    name, rtrans = _makeRotoTranslation()
    store = _makeStore()
    with _pytest.raises(ValueError):
        store["asdasd"] = rtrans

def test_RotoTranslation_fails_without_rotoTranslation():
    name, rtrans = _makeRotoTranslation()
    store = _makeStore()
    with _pytest.raises(TypeError):
        store[name] = "something"

def test_store_len():
    name, rtrans = _makeRotoTranslation()
    store = _makeStore()
    assert(len(store), 0)
    store[name] = rtrans
    assert(len(store), 1)

def test_store_del():
    name, rtrans = _makeRotoTranslation()
    store = _makeStore()
    assert(len(store), 0)
    store[name] = rtrans
    assert(len(store), 1)
    del store[name]
    assert(len(store), 0)

def test_addRotoTranslation():
    name1, rtrans1 = _makeRotoTranslation(name="rtrans1")
    name2, rtrans2 = _makeRotoTranslation(name="rtrans2")
    name3, rtrans3 = _makeRotoTranslation(name="rtrans3")
    name4, rtrans4 = _makeRotoTranslation(name="rtrans4")
    name5, rtrans5 = _makeRotoTranslation(name="rtrans5")

    store = _makeStore()

    store.addRotoTranslation(rtrans1)
    store.addRotoTranslation(rtrans2)
    assert(rtrans1.transformationIndex, 2000)
    assert(rtrans2.transformationIndex, 3000)
    del store[name1]
    store.addRotoTranslation(rtrans3)
    assert(rtrans3.transformationIndex, 4000)

    assert(store.allTransformationIndices(), [3000, 4000])

    rtrans4.transformationIndex = 9000
    store.addRotoTranslation(rtrans4)
    assert(rtrans4.transformationIndex, 9000)

    rtrans5.transformationIndex = 9000
    with _pytest.raises(KeyError):
        store.addRotoTranslation(rtrans5)
