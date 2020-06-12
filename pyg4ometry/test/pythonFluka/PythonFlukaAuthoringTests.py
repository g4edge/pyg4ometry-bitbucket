import unittest as _unittest
from random import random
import numpy as np

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


class PythonFlukaAuthoringTests(_unittest.TestCase):

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

    def test_PythonFluka_T803_material_element(self):
        T803_material_element.Test(True, False)


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
