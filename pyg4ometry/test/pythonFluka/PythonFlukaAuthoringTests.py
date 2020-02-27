import unittest as _unittest
from random import random
import numpy as np

from pyg4ometry.fluka.fluka_registry import RotoTranslationStore, FlukaRegistry
from pyg4ometry.fluka.directive import rotoTranslationFromTra2

import T001_RPP
import T002_BOX
import T003_SPH
import T004_RCC
import T005_REC
import T006_TRC
import T007_ELL
import T008_RAW
import T008_WED
import T009_ARB
import T010_XYP
import T010_XZP
import T010_YZP
import T011_PLA
import T012_XCC
import T012_YCC
import T012_ZCC
import T013_XEC
import T013_YEC
import T013_ZEC
import T014_QUA

import T051_expansion
import T052_translation
import T090_lattice

import T101_region_one_body
import T102_region_intersection_two_bodies
import T103_region_subtraction_two_bodies
import T103_region_subtraction_two_bodies_RCC
import T104_region_union_two_zones
import T104_region_union_two_zones_2
import T105_region_subzone_subtraction
import T106_region_subzone_subtraction_with_union
import T107_region_union_with_reused_bodies

import T201_RPP_coplanar
import T202_BOX_coplanar
import T203_SPH_coplanar
import T204_RCC_coplanar
import T205_REC_coplanar
import T206_TRC_coplanar
import T207_ELL_coplanar
import T208_RAW_coplanar
import T208_WED_coplanar
import T209_ARB_coplanar
import T210_PLA_coplanar
import T210_XYP_coplanar
import T210_XZP_coplanar
import T210_YZP_coplanar
import T212_XCC_coplanar
import T212_YCC_coplanar
import T212_ZCC_coplanar
import T213_XEC_coplanar
import T213_YEC_coplanar
import T213_ZEC_coplanar
import T214_QUA_coplanar

import T301_disjoint_union
import T302_disjoint_union_overlapping_bounding_boxes
import T303_disjoint_union_complex
import T304_disjoint_union_not_disjoint

import T401_RPP_expansion
import T402_BOX_expansion
import T403_SPH_expansion
import T404_RCC_expansion
import T405_REC_expansion
import T406_TRC_expansion
import T407_ELL_expansion
import T408_RAW_expansion
import T408_WED_expansion
import T409_ARB_expansion
import T410_XYP_expansion
import T410_XZP_expansion
import T410_YZP_expansion
import T411_PLA_expansion
import T412_XCC_expansion
import T412_YCC_expansion
import T412_ZCC_expansion
import T413_XEC_expansion
import T413_YEC_expansion
import T413_ZEC_expansion
import T414_QUA_expansion
import T501_RPP_translation
import T502_BOX_translation
import T503_SPH_translation
import T504_RCC_translation
import T505_REC_translation
import T506_TRC_translation
import T507_ELL_translation
import T508_RAW_translation
import T508_WED_translation
import T509_ARB_translation
import T510_XYP_translation
import T510_XZP_translation
import T510_YZP_translation
import T511_PLA_translation
import T512_XCC_translation
import T512_YCC_translation
import T512_ZCC_translation
import T513_XEC_translation
import T513_YEC_translation
import T513_ZEC_translation
import T514_QUA_translation

import T601_RPP_rototranslation
import T602_BOX_rototranslation
import T603_SPH_rototranslation
import T604_RCC_rototranslation
import T605_REC_rototranslation
import T606_TRC_rototranslation
import T607_ELL_rototranslation
import T608_RAW_rototranslation
import T608_WED_rototranslation
import T609_ARB_rototranslation
import T610_XYP_rototranslation
import T610_XZP_rototranslation
import T610_YZP_rototranslation
import T611_PLA_rototranslation
import T612_XCC_rototranslation
import T612_YCC_rototranslation
import T612_ZCC_rototranslation
import T613_XEC_rototranslation
import T613_YEC_rototranslation
import T613_ZEC_rototranslation
import T614_QUA_rototranslation

import T710_XYP_XZP_YZP_minimisation
import T711_PLA_minimisation
import T712_XCC_minimisation
import T712_YCC_minimisation
import T712_ZCC_minimisation
import T713_XEC_minimisation
import T713_YEC_minimisation
import T713_ZEC_minimisation

import T801_filter_redundant_halfspaces
import T802_materialMap

import T901_cube_from_XYP_XZP_YZP
import T902_cube_from_six_PLAs

class PythonFlukaAuthoringTests(_unittest.TestCase) :

    def test_PythonFluka_T001_RPP(self):
        T001_RPP.Test(True, False)

    def test_PythonFluka_T002_BOX(self):
        T002_BOX.Test(True, False)

    def test_PythonFluka_T003_SPH(self):
        T003_SPH.Test(True, False)

    def test_PythonFluka_T004_RCC(self):
        T004_RCC.Test(True, False)

    def test_PythonFluka_T005_REC(self):
        T005_REC.Test(True, False)

    def test_PythonFluka_T006_TRC(self):
        T006_TRC.Test(True, False)

    def test_PythonFluka_T007_ELL(self):
        T007_ELL.Test(True, False)

    def test_PythonFluka_T008_RAW(self):
        T008_RAW.Test(True, False)

    def test_PythonFluka_T008_WED(self):
        T008_WED.Test(True, False)

    def test_PythonFluka_T009_ARB(self):
        T009_ARB.Test(True, False)

    def test_PythonFluka_T010_XYP(self):
        T010_XYP.Test(True, False)

    def test_PythonFluka_T010_XZP(self):
        T010_XZP.Test(True, False)

    def test_PythonFluka_T010_YZP(self):
        T010_YZP.Test(True, False)

    def test_PythonFluka_T011_PLA(self):
        T011_PLA.Test(True, False)

    def test_PythonFluka_T012_XCC(self):
        T012_XCC.Test(True, False)

    def test_PythonFluka_T012_YCC(self):
        T012_YCC.Test(True, False)

    def test_PythonFluka_T012_ZCC(self):
        T012_ZCC.Test(True, False)

    def test_PythonFluka_T013_XEC(self):
        T013_XEC.Test(True, False)

    def test_PythonFluka_T013_YEC(self):
        T013_YEC.Test(True, False)

    def test_PythonFluka_T013_ZEC(self):
        T013_ZEC.Test(True, False)

    def test_PythonFluka_T014_QUA(self):
        T014_QUA.Test(True, False)

    def test_PythonFluka_T051_expansion(self):
        T051_expansion.Test(True, False)

    def test_PythonFluka_T052_translation(self):
        T052_translation.Test(True, False)

    def test_PythonFluka_T090_lattice(self):
        T090_lattice.Test(True, False)


    # 1111111111
    def test_PythonFluka_T101_region_one_body(self):
        T101_region_one_body.Test(True, False)

    def test_PythonFluka_T102_region_intersection_two_bodies(self):
        T102_region_intersection_two_bodies.Test(True, False)

    def test_PythonFluka_T103_region_subtraction_two_bodies(self):
        T103_region_subtraction_two_bodies.Test(True, False)

    def test_PythonFluka_T103_region_subtraction_two_bodies_RCC(self):
        T103_region_subtraction_two_bodies_RCC.Test(True, False)

    def test_PythonFluka_T104_region_union_two_zones(self):
        T104_region_union_two_zones.Test(True, False)

    def test_PythonFluka_T104_region_union_two_zones_2(self):
        T104_region_union_two_zones_2.Test(True, False)

    def test_PythonFluka_T105_region_subzone_subtraction(self):
        T105_region_subzone_subtraction.Test(True, False)

    def test_PythonFluka_T106_region_subzone_subtraction_with_union(self):
        T106_region_subzone_subtraction_with_union.Test(True, False)

    def test_PythonFluka_T107_region_union_with_reused_bodies(self):
        T107_region_union_with_reused_bodies.Test(True, False)


    # 2222222222
    def test_PythonFluka_T201_RPP_coplanar(self):
        T201_RPP_coplanar.Test(True, False)

    def test_PythonFluka_T202_BOX_coplanar(self):
        T202_BOX_coplanar.Test(True, False)

    def test_PythonFluka_T203_SPH_coplanar(self):
        T203_SPH_coplanar.Test(True, False)

    def test_PythonFluka_T204_RCC_coplanar(self):
        T204_RCC_coplanar.Test(True, False)

    def test_PythonFluka_T205_REC_coplanar(self):
        T205_REC_coplanar.Test(True, False)

    def test_PythonFluka_T206_TRC_coplanar(self):
        T206_TRC_coplanar.Test(True, False)

    def test_PythonFluka_T207_ELL_coplanar(self):
        T207_ELL_coplanar.Test(True, False)

    def test_PythonFluka_T208_RAW_coplanar(self):
        T208_RAW_coplanar.Test(True, False)

    def test_PythonFluka_T208_WED_coplanar(self):
        T208_WED_coplanar.Test(True, False)

    def test_PythonFluka_T209_ARB_coplanar(self):
        T209_ARB_coplanar.Test(True, False)

    def test_PythonFluka_T210_PLA_coplanar(self):
        T210_PLA_coplanar.Test(True, False)

    def test_PythonFluka_T210_XYP_coplanar(self):
        T210_XYP_coplanar.Test(True, False)

    def test_PythonFluka_T210_XZP_coplanar(self):
        T210_XZP_coplanar.Test(True, False)

    def test_PythonFluka_T210_YZP_coplanar(self):
        T210_YZP_coplanar.Test(True, False)

    def test_PythonFluka_T212_XCC_coplanar(self):
        T212_XCC_coplanar.Test(True, False)

    def test_PythonFluka_T212_YCC_coplanar(self):
        T212_YCC_coplanar.Test(True, False)

    def test_PythonFluka_T212_ZCC_coplanar(self):
        T212_ZCC_coplanar.Test(True, False)

    def test_PythonFluka_T213_XEC_coplanar(self):
        T213_XEC_coplanar.Test(True, False)

    def test_PythonFluka_T213_YEC_coplanar(self):
        T213_YEC_coplanar.Test(True, False)

    def test_PythonFluka_T213_ZEC_coplanar(self):
        T213_ZEC_coplanar.Test(True, False)

    def test_PythonFluka_T214_QUA_coplanar(self):
        T214_QUA_coplanar.Test(True, False)


    # 3333333333
    def test_PythonFluka_T301_disjoint_union(self):
        T301_disjoint_union.Test(True, False)

    def test_PythonFluka_T302_disjoint_union_overlapping_bounding_boxes(self):
        T302_disjoint_union_overlapping_bounding_boxes.Test(True, False)

    def test_PythonFluka_T303_disjoint_union_complex(self):
        T303_disjoint_union_complex.Test(True, False)

    def test_PythonFluka_T304_disjoint_union_not_disjoint(self):
        T304_disjoint_union_not_disjoint.Test(True, False)


    # 4444444444
    def test_PythonFluka_T401_RPP_expansion(self):
        T401_RPP_expansion.Test(True, False)

    def test_PythonFluka_T402_BOX_expansion(self):
        T402_BOX_expansion.Test(True, False)

    def test_PythonFluka_T403_SPH_expansion(self):
        T403_SPH_expansion.Test(True, False)

    def test_PythonFluka_T404_RCC_expansion(self):
        T404_RCC_expansion.Test(True, False)

    def test_PythonFluka_T405_REC_expansion(self):
        T405_REC_expansion.Test(True, False)

    def test_PythonFluka_T406_TRC_expansion(self):
        T406_TRC_expansion.Test(True, False)

    def test_PythonFluka_T407_ELL_expansion(self):
        T407_ELL_expansion.Test(True, False)

    def test_PythonFluka_T408_RAW_expansion(self):
        T408_RAW_expansion.Test(True, False)

    def test_PythonFluka_T408_WED_expansion(self):
        T408_WED_expansion.Test(True, False)

    def test_PythonFluka_T409_ARB_expansion(self):
        T409_ARB_expansion.Test(True, False)

    def test_PythonFluka_T410_XYP_expansion(self):
        T410_XYP_expansion.Test(True, False)

    def test_PythonFluka_T410_XZP_expansion(self):
        T410_XZP_expansion.Test(True, False)

    def test_PythonFluka_T410_YZP_expansion(self):
        T410_YZP_expansion.Test(True, False)

    def test_PythonFluka_T411_PLA_expansion(self):
        T411_PLA_expansion.Test(True, False)

    def test_PythonFluka_T412_XCC_expansion(self):
        T412_XCC_expansion.Test(True, False)

    def test_PythonFluka_T412_YCC_expansion(self):
        T412_YCC_expansion.Test(True, False)

    def test_PythonFluka_T412_ZCC_expansion(self):
        T412_ZCC_expansion.Test(True, False)

    def test_PythonFluka_T413_XEC_expansion(self):
        T413_XEC_expansion.Test(True, False)

    def test_PythonFluka_T413_YEC_expansion(self):
        T413_YEC_expansion.Test(True, False)

    def test_PythonFluka_T413_ZEC_expansion(self):
        T413_ZEC_expansion.Test(True, False)

    def test_PythonFluka_T414_QUA_expansion(self):
        T414_QUA_expansion.Test(True, False)

    def test_PythonFluka_T501_RPP_translation(self):
        T501_RPP_translation.Test(True, False)

    def test_PythonFluka_T502_BOX_translation(self):
        T502_BOX_translation.Test(True, False)

    def test_PythonFluka_T503_SPH_translation(self):
        T503_SPH_translation.Test(True, False)

    def test_PythonFluka_T504_RCC_translation(self):
        T504_RCC_translation.Test(True, False)

    def test_PythonFluka_T505_REC_translation(self):
        T505_REC_translation.Test(True, False)

    def test_PythonFluka_T506_TRC_translation(self):
        T506_TRC_translation.Test(True, False)

    def test_PythonFluka_T507_ELL_translation(self):
        T507_ELL_translation.Test(True, False)

    def test_PythonFluka_T508_RAW_translation(self):
        T508_RAW_translation.Test(True, False)

    def test_PythonFluka_T508_WED_translation(self):
        T508_WED_translation.Test(True, False)

    def test_PythonFluka_T509_ARB_translation(self):
        T509_ARB_translation.Test(True, False)

    def test_PythonFluka_T510_XYP_translation(self):
        T510_XYP_translation.Test(True, False)

    def test_PythonFluka_T510_XZP_translation(self):
        T510_XZP_translation.Test(True, False)

    def test_PythonFluka_T510_YZP_translation(self):
        T510_YZP_translation.Test(True, False)

    def test_PythonFluka_T511_PLA_translation(self):
        T511_PLA_translation.Test(True, False)

    def test_PythonFluka_T512_XCC_translation(self):
        T512_XCC_translation.Test(True, False)

    def test_PythonFluka_T512_YCC_translation(self):
        T512_YCC_translation.Test(True, False)

    def test_PythonFluka_T512_ZCC_translation(self):
        T512_ZCC_translation.Test(True, False)

    def test_PythonFluka_T513_XEC_translation(self):
        T513_XEC_translation.Test(True, False)

    def test_PythonFluka_T513_YEC_translation(self):
        T513_YEC_translation.Test(True, False)

    def test_PythonFluka_T513_ZEC_translation(self):
        T513_ZEC_translation.Test(True, False)

    def test_PythonFluka_T514_QUA_translation(self):
        T514_QUA_translation.Test(True, False)


    # 6666666666
    def test_PythonFluka_T601_RPP_rototranslation(self):
        T601_RPP_rototranslation.Test(True, False)

    def test_PythonFluka_T602_BOX_rototranslation(self):
        T602_BOX_rototranslation.Test(True, False)

    def test_PythonFluka_T603_SPH_rototranslation(self):
        T603_SPH_rototranslation.Test(True, False)

    def test_PythonFluka_T604_RCC_rototranslation(self):
        T604_RCC_rototranslation.Test(True, False)

    def test_PythonFluka_T605_REC_rototranslation(self):
        T605_REC_rototranslation.Test(True, False)

    def test_PythonFluka_T606_TRC_rototranslation(self):
        T606_TRC_rototranslation.Test(True, False)

    def test_PythonFluka_T607_ELL_rototranslation(self):
        T607_ELL_rototranslation.Test(True, False)

    def test_PythonFluka_T608_RAW_rototranslation(self):
        T608_RAW_rototranslation.Test(True, False)

    def test_PythonFluka_T608_WED_rototranslation(self):
        T608_WED_rototranslation.Test(True, False)

    def test_PythonFluka_T609_ARB_rototranslation(self):
        T609_ARB_rototranslation.Test(True, False)

    def test_PythonFluka_T610_XYP_rototranslation(self):
        T610_XYP_rototranslation.Test(True, False)

    def test_PythonFluka_T610_XZP_rototranslation(self):
        T610_XZP_rototranslation.Test(True, False)

    def test_PythonFluka_T610_YZP_rototranslation(self):
        T610_YZP_rototranslation.Test(True, False)

    def test_PythonFluka_T611_PLA_rototranslation(self):
        T611_PLA_rototranslation.Test(True, False)

    def test_PythonFluka_T612_XCC_rototranslation(self):
        T612_XCC_rototranslation.Test(True, False)

    def test_PythonFluka_T612_YCC_rototranslation(self):
        T612_YCC_rototranslation.Test(True, False)

    def test_PythonFluka_T612_ZCC_rototranslation(self):
        T612_ZCC_rototranslation.Test(True, False)

    def test_PythonFluka_T613_XEC_rototranslation(self):
        T613_XEC_rototranslation.Test(True, False)

    def test_PythonFluka_T613_YEC_rototranslation(self):
        T613_YEC_rototranslation.Test(True, False)

    def test_PythonFluka_T613_ZEC_rototranslation(self):
        T613_ZEC_rototranslation.Test(True, False)

    def test_PythonFluka_T614_QUA_rototranslation(self):
        T614_QUA_rototranslation.Test(True, False)


    # 7777777777
    def test_PythonFluka_T710_XYP_XZP_YZP_minimisation(self):
        T710_XYP_XZP_YZP_minimisation.Test(True, False)

    def test_PythonFluka_T711_PLA_minimisation(self):
        T711_PLA_minimisation.Test(True, False)

    def test_PythonFluka_T712_XCC_minimisation(self):
        T712_XCC_minimisation.Test(True, False)

    def test_PythonFluka_T712_YCC_minimisation(self):
        T712_YCC_minimisation.Test(True, False)

    def test_PythonFluka_T712_ZCC_minimisation(self):
        T712_ZCC_minimisation.Test(True, False)

    def test_PythonFluka_T713_XEC_minimisation(self):
        T713_XEC_minimisation.Test(True, False)

    def test_PythonFluka_T713_YEC_minimisation(self):
        T713_YEC_minimisation.Test(True, False)

    def test_PythonFluka_T713_ZEC_minimisation(self):
        T713_ZEC_minimisation.Test(True, False)


    # 8888888888
    def test_PythonFluka_T801_filter_redundant_halfspaces(self):
        T801_filter_redundant_halfspaces.Test(True, False)

    def test_PythonFluka_T802_materialMap(self):
        T802_materialMap.Test(True, False)


    # 9999999999
    def test_PythonFluka_T901_cube_from_XYP_XZP_YZP(self):
        T901_cube_from_XYP_XZP_YZP.Test(True, False)

    def test_PythonFluka_T902_cube_from_six_PLAs(self):
        T902_cube_from_six_PLAs.Test(True, False)


    def test_PythonFluka_empyRegistry(self):

        import pyg4ometry.convert as convert
        from pyg4ometry.fluka import FlukaRegistry

        freg = FlukaRegistry()
        try :
            greg = convert.fluka2Geant4(freg)
        except ValueError :
            pass


class RotoTranslationStoreTests(_unittest.TestCase):
    def _makeRotoTranslation(self, name="rppTRF"):
        angle = random() * np.pi
        rtrans = rotoTranslationFromTra2(name,
                                         [[angle, angle, angle],
                                          [0, 0, 20]])
        return name, rtrans

    def _makeStore(self):
        return RotoTranslationStore()

    def test_storeInit(self):
        self._makeStore()

    def test_gettingRotoTranslation(self):
        name, rtrans = self._makeRotoTranslation()
        store = self._makeStore()
        store[name] = rtrans
        r = store[name]

    def test_RotoTranslation_fails_setting_with_wrong_name(self):
        name, rtrans = self._makeRotoTranslation()
        store = self._makeStore()
        with self.assertRaises(ValueError):
            store["asdasd"] = rtrans

    def test_RotoTranslation_fails_without_rotoTranslation(self):
        name, rtrans = self._makeRotoTranslation()
        store = self._makeStore()
        with self.assertRaises(TypeError):
            store[name] = "something"

    def test_store_len(self):
        name, rtrans = self._makeRotoTranslation()
        store = self._makeStore()
        self.assertEqual(len(store), 0)
        store[name] = rtrans
        self.assertEqual(len(store), 1)

    def test_store_del(self):
        name, rtrans = self._makeRotoTranslation()
        store = self._makeStore()
        self.assertEqual(len(store), 0)
        store[name] = rtrans
        self.assertEqual(len(store), 1)
        del store[name]
        self.assertEqual(len(store), 0)

    def test_addRotoTranslation(self):
        name1, rtrans1 = self._makeRotoTranslation(name="rtrans1")
        name2, rtrans2 = self._makeRotoTranslation(name="rtrans2")
        name3, rtrans3 = self._makeRotoTranslation(name="rtrans3")
        name4, rtrans4 = self._makeRotoTranslation(name="rtrans4")
        name5, rtrans5 = self._makeRotoTranslation(name="rtrans5")

        store = self._makeStore()

        store.addRotoTranslation(rtrans1)
        store.addRotoTranslation(rtrans2)
        self.assertEqual(rtrans1.transformationIndex, 2000)
        self.assertEqual(rtrans2.transformationIndex, 3000)
        del store[name1]
        store.addRotoTranslation(rtrans3)
        self.assertEqual(rtrans3.transformationIndex, 4000)

        self.assertEqual(store.allTransformationIndices(), [3000, 4000])

        rtrans4.transformationIndex = 9000
        store.addRotoTranslation(rtrans4)
        self.assertEqual(rtrans4.transformationIndex, 9000)

        rtrans5.transformationIndex = 9000
        with self.assertRaises(KeyError):
            store.addRotoTranslation(rtrans5)



if __name__ == '__main__':
    _unittest.main(verbosity=2)
