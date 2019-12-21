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