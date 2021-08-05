import unittest as _unittest
import numpy as _np
import os as _os

import ROOT as _ROOT
import pyg4ometry as _pyg4ometry

def gdml2ROOT(gdmlFileName, rootFileName):
    tgm = _ROOT.TGeoManager.Import(_os.path.join(_os.path.dirname(__file__),gdmlFileName))
    tgm.Export(_os.path.join(_os.path.dirname(__file__),rootFileName))

def loadROOTFile(rootFileName):
    r = _pyg4ometry.io.ROOT.Reader(_os.path.join(_os.path.dirname(__file__),rootFileName))
    return r

def deleteROOTFile(rootFileName):
    _os.remove(_os.path.join(_os.path.dirname(__file__),rootFileName))

def visGeometry(wl, vis = False, interactive = False):
    extentBB = wl.extent(includeBoundingSolid=True)

    if vis:
        v = _pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(wl)
        v.addAxes(_pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)
        return v

class ROOTTests(_unittest.TestCase) :

    # #############################
    #
    # #############################
    def test_ROOT_T001Box(self,  vis = False, interactive = False):
        gdml2ROOT("T001_Box.gdml","T001_Box.root")
        r = loadROOTFile("T001_Box.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        deleteROOTFile("T001_Box.root")

    def test_ROOT_T002Tubs(self,  vis = False, interactive = False):
        gdml2ROOT("T002_Tubs.gdml","T002_Tubs.root")
        r = loadROOTFile("T002_Tubs.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        deleteROOTFile("T002_Tubs.root")

    def test_ROOT_T003CutTubs(self,  vis = False, interactive = False):
        gdml2ROOT("T003_CutTubs.gdml","T003_CutTubs.root")
        r = loadROOTFile("T003_CutTubs.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        deleteROOTFile("T003_CutTubs.root")

    def test_ROOT_T004Cons(self,  vis = False, interactive = False):
        gdml2ROOT("T004_Cons.gdml","T004_Cons.root")
        r = loadROOTFile("T004_Cons.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        deleteROOTFile("T004_Cons.root")

    def test_ROOT_T005Para(self,  vis = False, interactive = False):
        gdml2ROOT("T005_Para.gdml","T005_Para.root")
        r = loadROOTFile("T005_Para.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        deleteROOTFile("T005_Para.root")

    def test_ROOT_T006Trd(self,  vis = False, interactive = False):
        gdml2ROOT("T006_Trd.gdml","T006_Trd.root")
        r = loadROOTFile("T006_Trd.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T007Trap(self,  vis = False, interactive = False):
        gdml2ROOT("T007_Trap.gdml","T007_Trap.root")
        r = loadROOTFile("T007_Trap.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        deleteROOTFile("T007_Trap.root")

    def test_ROOT_T008Sphere(self,  vis = False, interactive = False):
        gdml2ROOT("T008_Sphere.gdml","T008_Sphere.root")
        r = loadROOTFile("T008_Sphere.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T009Orb(self,  vis = False, interactive = False):
        gdml2ROOT("T009_Orb.gdml","T009_Orb.root")
        r = loadROOTFile("T009_Orb.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T010Torus(self,  vis = False, interactive = False):
        gdml2ROOT("T010_Torus.gdml","T010_Torus.root")
        r = loadROOTFile("T010_Torus.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T011Polycone(self,  vis = False, interactive = False):
        gdml2ROOT("T011_Polycone.gdml","T011_Polycone.root")
        r = loadROOTFile("T011_Polycone.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    # Generic polycone does not exist in ROOT

    def test_ROOT_T013Polyhedra(self,  vis = False, interactive = False):
        gdml2ROOT("T013_Polyhedra.gdml","T013_Polyhedra.root")
        r = loadROOTFile("T013_Polyhedra.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    # Generic polyheda does not exist in ROOT

    def test_ROOT_T015EllipticalTube(self,  vis = False, interactive = False):
        gdml2ROOT("T015_EllipticalTube.gdml","T015_EllipticalTube.root")
        r = loadROOTFile("T015_EllipticalTube.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    # Ellipsoid used scaled and boolean
    def test_ROOT_T016Ellipsoid(self,  vis = False, interactive = False):
        gdml2ROOT("T016_Ellipsoid.gdml","T016_Ellipsoid.root")
        r = loadROOTFile("T016_Ellipsoid.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    # phi range does not exist for ROOT Cons
    def test_ROOT_T017EllipticalCone(self,  vis = False, interactive = False):
        gdml2ROOT("T017_EllipticalCone.gdml","T017_EllipticalCone.root")
        r = loadROOTFile("T017_EllipticalCone.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T018Paraboloid(self,  vis = False, interactive = False):
        gdml2ROOT("T018_Paraboloid.gdml","T018_Paraboloid.root")
        r = loadROOTFile("T018_Paraboloid.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T019Hyperboloid(self,  vis = False, interactive = False):
        gdml2ROOT("T019_Hyperboloid.gdml","T019_Hyperboloid.root")
        r = loadROOTFile("T019_Hyperboloid.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    # Tet does not exist

    def test_ROOT_T021ExtrudedSolid(self,  vis = False, interactive = False):
        gdml2ROOT("T021_ExtrudedSolid.gdml","T021_ExtrudedSolid.root")
        r = loadROOTFile("T021_ExtrudedSolid.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    # Twisted don't exist

    # Generic trap does not exist either

    def test_ROOT_T028Union(self,  vis = False, interactive = False):
        gdml2ROOT("T028_Union.gdml","T028_Union.root")
        r = loadROOTFile("T028_Union.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    def test_ROOT_T029Subtraction(self,  vis = False, interactive = False):
        gdml2ROOT("T029_Subtraction.gdml","T029_Subtraction.root")
        r = loadROOTFile("T029_Subtraction.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    def test_ROOT_T030Intersection(self,  vis = False, interactive = False):
        gdml2ROOT("T030_Intersection.gdml","T030_Intersection.root")
        r = loadROOTFile("T030_Intersection.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    # Multiunion does not exist
    #def test_ROOT_T031MultiUnion(self,  vis = False, interactive = False):
    #    gdml2ROOT("T031_MultiUnion.gdml","T031_MultiUnion.root")
    #    r = loadROOTFile("T031_MultiUnion.root")
    #    l = r.getRegistry().getWorldVolume()
    #    v = visGeometry(l, vis, interactive)
    #    return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    # Scaled cannot be read by ROOT?

    def test_ROOT_T033TessellatedSolid(self,  vis = False, interactive = False):
        gdml2ROOT("T033_TessellatedSolid.gdml","T033_TessellatedSolid.root")
        r = loadROOTFile("T033_TessellatedSolid.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}


    def test_ROOT_T101PhysicalLogical(self,  vis = False, interactive = False):
        gdml2ROOT("T101_physical_logical.gdml","T101_physical_logical.root")
        r = loadROOTFile("T101_physical_logical.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    def test_ROOT_T102OverlapNone(self,  vis = False, interactive = False):
        gdml2ROOT("T102_overlap_none.gdml","T102_overlap_none.root")
        r = loadROOTFile("T102_overlap_none.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    def test_ROOT_T103OverlapCopl(self,  vis = False, interactive = False):
        gdml2ROOT("T103_overlap_copl.gdml","T103_overlap_copl.root")
        r = loadROOTFile("T103_overlap_copl.root")
        visGeometry(r.getRegistry().getWorldVolume(), vis, interactive)

    def test_ROOT_T900LHT(self,  vis = False, interactive = False):
        gdml2ROOT("lht.gdml","lht.root")
        r = loadROOTFile("lht.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}

    def test_ROOT_T901BoxPlacement(self,  vis = False, interactive = False):
        gdml2ROOT("T001_geant4Box2Fluka.gdml","T001_geant4Box2Fluka.root")
        r = loadROOTFile("T001_geant4Box2Fluka.root")
        l = r.getRegistry().getWorldVolume()
        v = visGeometry(l, vis, interactive)
        return {"testStatus": True, "logicalVolume":l, "vtkViewer":v}