import unittest as _unittest

import pyg4ometry.geant4 as _g4
import pyg4ometry.freecad as _fc

import logging as _log
import os as _os

#logger = _log.getLogger()
#logger.disabled = True

def LoadFreecad(fileName) : 
    r = _fc.Reader(fileName) 
    r.convertFlat()
    
    return True

def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

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
