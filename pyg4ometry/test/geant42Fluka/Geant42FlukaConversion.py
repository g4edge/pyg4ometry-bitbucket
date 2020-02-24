import unittest as _unittest

import T001_geant4Box2Fluka
import T002_geant4Tubs2Fluka
import T003_geant4CutTubs2Fluka
import T015_geant4EllipticalTube2Fluka

class Geant42FlukaConversionTests(_unittest.TestCase) :
    def test_Geant42FlukaConversion_T001_Box(self) :
        T001_geant4Box2Fluka.Test(False,False)

    def test_Geant42FlukaConversion_T002_Tubs(self):
        T002_geant4Tubs2Fluka.Test(False,False)

    def test_Geant42FlukaConversion_T003_CutTubs(self):
        T003_geant4CutTubs2Fluka.Test(False,False)

    def test_Geant42FlukaConversion_T015_EllipticalTube(self):
        T015_geant4EllipticalTube2Fluka.Test(False,False)

if __name__ == '__main__':
    _unittest.main(verbosity=2)
