import unittest as _unittest

import T001_RPP
import T002_BOX
import T003_SPH
import T004_RCC
import T005_REC
import T006_TRC
import T007_ELL
import T008_RAW
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
import T053_roto_translation
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
import T209_ARB_coplanar
import T210_PLA_coplanar
import T212_XCC_coplanar
import T213_XEC_coplanar
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
import T409_ARB_expansion
import T410_XYP_expansion
import T411_PLA_expansion
import T412_XCC_expansion
import T413_XEC_expansion
import T414_QUA_expansion

import T501_RPP_translation
import T502_BOX_translation
import T503_SPH_translation
import T504_RCC_translation
import T505_REC_translation
import T506_TRC_translation
import T507_ELL_translation
import T508_RAW_translation
import T509_ARB_translation
import T510_XYP_translation
import T511_PLA_translation
import T512_XCC_translation
import T513_XEC_translation
import T514_QUA_translation


class PythonFlukaAuthoringTests(_unittest.TestCase) :
    def test_PythonFluka_T001_RPP(selT104_region_union_two_zones_2f):
        T001_RPP.Test(True,False)

    def test_PythonFluka_T002_BOX(self):
        T002_BOX.Test(True,False)

    def test_PythonFluka_T003_SPH(self):
        T003_SPH.Test(True,False)

    def test_PythonFluka_T004_RCC(self):
        T004_RCC.Test(True,False)

    def test_PythonFluka_T005_REC(self):
        T005_REC.Test(True,False)

    def test_PythonFluka_T006_TRC(self):
        T006_TRC.Test(True,False)

    def test_PythonFluka_T007_ELL(self):
        T007_ELL.Test(True,False)

    def test_PythonFluka_T008_RAW(self):
        T008_RAW.Test(True,False)

    #def test_PythonFluka_T009_ARB(self):
    #    T009_ARB.Test(True,False)

    def test_PythonFluka_T010_XYP(self):
        T010_XYP.Test(True,False)

    def test_PythonFluka_T010_XZP(self):
        T010_XZP.Test(True,False)

    def test_PythonFluka_T010_YZP(self):
        T010_YZP.Test(True,False)

    def test_PythonFluka_T011_PLA(self):
        T011_PLA.Test(True,False)

    def test_PythonFluka_T012_XCC(self):
        T012_XCC.Test(True,False)

    def test_PythonFluka_T012_YCC(self):
        T012_YCC.Test(True,False)

    def test_PythonFluka_T012_ZCC(self):
        T012_ZCC.Test(True,False)

    def test_PythonFluka_T013_XEC(self):
        T013_XEC.Test(True, False)

    def test_PythonFluka_T013_YEC(self):
        T013_YEC.Test(True, False)

    def test_PythonFluka_T013_ZEC(self):
        T013_ZEC.Test(True, False)

    def test_PythonFluka_T014_QUA(self):
        T014_QUA.Test(True,False)

    def test_PythonFluka_T051_expansion(self):
        T051_expansion.Test(True,False)

    def test_PythonFluka_T052_translation(self):
        T052_translation.Test(True,False)

    def test_PythonFluka_T053_roto_translation(self):
        T053_roto_translation.Test(True,False)

    def test_PythonFluka_T090_lattice(self):
        T090_lattice.Test(True,False)

    def test_PythonFluka_T101_region_one_body(self):
        T101_region_one_body.Test(True,False)

    def test_PythonFluka_T102_region_intersection_two_bodies(self):
        T102_region_intersection_two_bodies.Test(True,False)

    def test_PythonFluka_T103_region_subtraction_two_bodies(self):
        T103_region_subtraction_two_bodies.Test(True,False)

    def test_PythonFluka_T103_region_subtraction_two_bodies_RCC(self):
        T103_region_subtraction_two_bodies_RCC.Test(True,False)

    def test_PythonFluka_T104_region_union_two_zones(self):
        T104_region_union_two_zones.Test(True,False)

    def test_PythonFluka_T104_region_union_two_zones_2(self):
        T104_region_union_two_zones_2.Test(True,False)

    def test_PythonFluka_T105_region_subzone_subtraction(self):
        T105_region_subzone_subtraction.Test(True,False)

    def test_PythonFluka_T106_region_subzone_subtraction_with_union(self):
        T106_region_subzone_subtraction_with_union.Test(True,False)

    def test_PythonFluka_T107_region_union_with_reused_bodies(self):
        T107_region_union_with_reused_bodies.Test(True,False)

    def test_PythonFluka_T201_RPP_coplanar(self):
        T201_RPP_coplanar.Test(True,False)

    def test_PythonFluka_T202_BOX_coplanar(self):
        T202_BOX_coplanar.Test(True,False)

    def test_PythonFluka_T203_SPH_coplanar(self):
        T203_SPH_coplanar.Test(True,False)

    def test_PythonFluka_T204_RCC_coplanar(self):
        T204_RCC_coplanar.Test(True,False)

    def test_PythonFluka_T205_REC_coplanar(self):
        T205_REC_coplanar.Test(True,False)

    def test_PythonFluka_T206_TRC_coplanar(self):
        T206_TRC_coplanar.Test(True,False)

    def test_PythonFluka_T207_ELL_coplanar(self):
        T207_ELL_coplanar.Test(True,False)

    #def test_PythonFluka_T208_RAW_coplanar(self):
    #    T208_RAW_coplanar.Test(True,False)

    #def test_PythonFluka_T209_ARB_coplanar(self):
    #    T209_ARB_coplanar.Test(True,False)

    def test_PythonFluka_T210_PLA_coplanar(self):
        T210_PLA_coplanar.Test(True,False)

    def test_PythonFluka_T212_XCC_coplanar(self):
        T212_XCC_coplanar.Test(True,False)

    def test_PythonFluka_T213_XEC_coplanar(self):
        T213_XEC_coplanar.Test(True,False)

    #def test_PythonFluka_T214_QUA_coplanar(self):
    #    T214_QUA_coplanar.Test(True,False)

    def test_PythonFluka_T301_disjoint_union(self):
        T301_disjoint_union.Test(True,False)

    def test_PythonFluka_T302_disjoint_union_overlapping_bounding_boxes(self):
        T302_disjoint_union_overlapping_bounding_boxes.Test(True,False)

    def test_PythonFluka_T303_disjoint_union_complex(self):
        T303_disjoint_union_complex.Test(True,False)

    def test_PythonFluka_T304_disjoint_union_not_disjoint(self):
        T304_disjoint_union_not_disjoint.Test(True,False)

    def test_PythonFluka_T401_RPP_expansion(self):
        T401_RPP_expansion.Test(True,False)

    def test_PythonFluka_T402_BOX_expansion(self):
        T402_BOX_expansion.Test(True,False)

    def test_PythonFluka_T403_SPH_expansion(self):
        T403_SPH_expansion.Test(True,False)

    def test_PythonFluka_T404_RCC_expansion(self):
        T404_RCC_expansion.Test(True,False)

    def test_PythonFluka_T405_REC_expansion(self):
        T405_REC_expansion.Test(True,False)

    def test_PythonFluka_T406_TRC_expansion(self):
        T406_TRC_expansion.Test(True,False)

    def test_PythonFluka_T407_ELL_expansion(self):
        T407_ELL_expansion.Test(True,False)

    def test_PythonFluka_T408_RAW_expansion(self):
        T408_RAW_expansion.Test(True,False)

    def test_PythonFluka_T409_ARB_expansion(self):
        T409_ARB_expansion.Test(True,False)

    def test_PythonFluka_T410_XYP_expansion(self):
        T410_XYP_expansion.Test(True,False)

    def test_PythonFluka_T411_PLA_expansion(self):
        T411_PLA_expansion.Test(True,False)

    def test_PythonFluka_T412_XCC_expansion(self):
        T412_XCC_expansion.Test(True,False)

    def test_PythonFluka_T413_XEC_expansion(self):
        T413_XEC_expansion.Test(True,False)

    def test_PythonFluka_T414_QUA_expansion(self):
        T414_QUA_expansion.Test(True,False)

    def test_PythonFluka_T501_RPP_translation(self):
        T501_RPP_translation.Test(True,False)

    def test_PythonFluka_T502_BOX_translation(self):
        T502_BOX_translation.Test(True,False)

    def test_PythonFluka_T503_SPH_translation(self):
        T503_SPH_translation.Test(True,False)

    def test_PythonFluka_T504_RCC_translation(self):
        T504_RCC_translation.Test(True,False)

    def test_PythonFluka_T505_REC_translation(self):
        T505_REC_translation.Test(True,False)

    def test_PythonFluka_T506_TRC_translation(self):
        T506_TRC_translation.Test(True,False)

    def test_PythonFluka_T507_ELL_translation(self):
        T507_ELL_translation.Test(True,False)

    def test_PythonFluka_T508_RAW_translation(self):
        T508_RAW_translation.Test(True,False)

    def test_PythonFluka_T509_ARB_translation(self):
        T509_ARB_translation.Test(True,False)

    def test_PythonFluka_T510_XYP_translation(self):
        T510_XYP_translation.Test(True,False)

    def test_PythonFluka_T511_PLA_translation(self):
        T511_PLA_translation.Test(True,False)

    def test_PythonFluka_T512_XCC_translation(self):
        T512_XCC_translation.Test(True,False)

    def test_PythonFluka_T513_XEC_translation(self):
        T513_XEC_translation.Test(True,False)

    def test_PythonFluka_T514_QUA_translation(self):
        T514_QUA_translation.Test(True,False)

    def test_PythonFluka_empyRegistry(self):

        import pyg4ometry.convert as convert
        from pyg4ometry.fluka import FlukaRegistry

        freg = FlukaRegistry()
        try :
            greg = convert.fluka2Geant4(freg)
        except ValueError :
            pass

if __name__ == '__main__':
    _unittest.main(verbosity=2)
