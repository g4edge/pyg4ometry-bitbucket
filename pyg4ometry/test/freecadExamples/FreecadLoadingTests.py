import unittest as _unittest

import pyg4ometry
import pyg4ometry.gdml as _gd
import pyg4ometry.geant4 as _g4


import logging as _log
import os as _os

#logger = _log.getLogger()
#logger.disabled = True

def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

def LoadFreecad(fileName, interactive = False) :

    # Loading
    reader = pyg4ometry.freecad.Reader(fileName)

    # Convert
    reader.relabelModel()
    reader.convertFlat()
    registry = reader.getRegistry()

    # World logical
    worldLogical = registry.getWorldVolume()

    # test extent of physical volume
    extentBB = worldLogical.extent(includeBoundingSolid=True)

    # Visualisation
    v = pyg4ometry.visualisation.VtkViewer()
    v.addLogicalVolume(registry.getWorldVolume())
    v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
    v.view(interactive=interactive)

    # Writing
    if fileName.find("stp") != -1 :
        newFilename = fileName.replace(".stp", ".gdml")
    else :
        newFilename = fileName.replace(".step", ".gdml")

    writer = pyg4ometry.gdml.Writer()
    writer.addDetector(registry)
    writer.write(newFilename)

    return True

def LoadFreecad_withPlacement(fileName, interactive=False) :

    # Loading
    reader = pyg4ometry.freecad.Reader(fileName)

    # Get registry
    reg = reader.getRegistry()

    # Convert
    reader.relabelModel()
    reader.convertFlat()
    registry = reader.getRegistry()

    # CAD logical
    logical = registry.getWorldVolume()

    # test extent of physical volume
    extentBB = logical.extent(includeBoundingSolid=True)

    # create world
    # defines
    wx = _gd.Constant("wx", 2*(extentBB[1][0]-extentBB[0][0]), reg, True)
    wy = _gd.Constant("wy", 2*(extentBB[1][1]-extentBB[0][2]), reg, True)
    wz = _gd.Constant("wz", 2*(extentBB[1][2]-extentBB[0][2]), reg, True)
    wm = _g4.MaterialPredefined("G4_Galactic")

    ws = _g4.solid.Box("ws",wx,wy,wz, reg, "mm")
    wl = _g4.LogicalVolume(ws, wm, "wl", reg)
    bp = _g4.PhysicalVolume([0,0,0],reader.rootPlacement,logical, "cad_pv1", wl, reg)

    # Visualisation
    v = pyg4ometry.visualisation.VtkViewer()
    v.addLogicalVolume(wl)
    v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
    v.view(interactive=interactive)

    # Writing
    if fileName.find("stp") != -1 :
        newFilename = fileName.replace(".stp", ".gdml")
    else :
        newFilename = fileName.replace(".step", ".gdml")

    writer = pyg4ometry.gdml.Writer()
    writer.addDetector(registry)
    writer.write(newFilename)

    return True

class FreecadLoadingTests(_unittest.TestCase) :
    def test_Freecad_LoadBasicSolids(self) :
        self.assertTrue(LoadFreecad(_pj("01_BasicSolids.step")))

    def test_Freecad_LoadBooleanSolids(self) :
        self.assertTrue(LoadFreecad(_pj("02_BooleanSolids.step")))

    def test_Freecad_LoadSketchPadSolids(self) :
        self.assertTrue(LoadFreecad(_pj("03_SketchPad.step")))

    def test_Freecad_LoadSketchPadSolids(self) :
        self.assertTrue(LoadFreecad(_pj("04_Rubik.step")))

    def test_Freecad_LoadPlacement(self) :
        self.assertTrue(LoadFreecad(_pj("05_Placement.step")))
            
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
