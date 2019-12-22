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

class PythonFlukaAuthoringTests(_unittest.TestCase) :
    def test_PythonFluka_T001_RPP(self):
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

    def test_PythonFluka_T009_ARB(self):
        T009_ARB.Test(True,False)

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