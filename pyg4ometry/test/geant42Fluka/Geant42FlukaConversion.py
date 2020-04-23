import unittest as _unittest

import T001_geant4Box2Fluka
import T002_geant4Tubs2Fluka
import T003_geant4CutTubs2Fluka
import T004_geant4Cons2Fluka
import T005_geant4Para2Fluka
import T006_geant4Trd2Fluka
import T007_geant4Trap2Fluka
import T008_geant4Sphere2Fluka
import T009_geant4Orb2Fluka
import T010_geant4Torus2Fluka
import T011_geant4Polycone2Fluka
import T012_geant4GenericPolycone2Fluka
import T013_geant4Polyhedra2Fluka
import T014_geant4GenericPolyhedra2Fluka
import T015_geant4EllipticalTube2Fluka
import T016_geant4Ellipsoid2Fluka
import T017_geant4EllipticalCone2Fluka
import T018_geant4Paraboloid2Fluka
import T019_geant4Hyperboloid2Fluka
import T020_geant4Tet2Fluka
import T021_geant4ExtrudedSolid2Fluka
import T026_geant4GenericTrap2Fluka

import T028_geant4Union2Fluka
import T029_geant4Subtraction2Fluka
import T030_geant4Intersection2Fluka


class Geant42FlukaConversionTests(_unittest.TestCase) :
    def test_Geant42FlukaConversion_T001_Box(self) :
        T001_geant4Box2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T002_Tubs(self):
        T002_geant4Tubs2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T003_CutTubs(self):
        T003_geant4CutTubs2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T004_Cons(self):
        T004_geant4Cons2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T005_Para(self):
        T005_geant4Para2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T006_Tdr(self):
        T006_geant4Trd2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T007_Trap(self):
        T007_geant4Trap2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T008_Sphere(self):
        T008_geant4Sphere2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T009_Orb(self):
        T009_geant4Orb2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T010_Torus(self):
        T010_geant4Torus2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T011_Polycone(self):
        T011_geant4Polycone2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T012_GenericPolycone(self):
        T012_geant4GenericPolycone2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T013_Polyhedra(self):
        T013_geant4Polyhedra2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T014_GenericPolyhedra(self):
        T014_geant4GenericPolyhedra2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T015_EllipticalTube(self):
        T015_geant4EllipticalTube2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T016_Ellipsoid(self):
        T016_geant4Ellipsoid2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T017_EllipticalCone(self):
        T017_geant4EllipticalCone2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T018_Paraboloid(self):
        T018_geant4Paraboloid2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T019_Hyperboloid(self):
        T019_geant4Hyperboloid2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T020_Tet(self):
        T020_geant4Tet2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T021_ExtrudedSolid(self):
        T021_geant4ExtrudedSolid2Fluka.Test(False,False,True)

#    def test_Geant42FlukaConversion_T026_GenericTrap(self):
#        T026_geant4GenericTrap2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T028_Union(self):
        T028_geant4Union2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T029_Subtraction(self):
        T029_geant4Subtraction2Fluka.Test(False,False,True)

    def test_Geant42FlukaConversion_T030_Intersection(self):
        T030_geant4Intersection2Fluka.Test(False,False,True)

if __name__ == '__main__':
    _unittest.main(verbosity=2)
