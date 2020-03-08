import unittest as _unittest

import pyg4ometry
import pyg4ometry.freecad as _fc

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
