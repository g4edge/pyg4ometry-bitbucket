import unittest as _unittest

import pyg4ometry.geant4 as _g4
import pyg4ometry.stl as _stl

import logging as _log
import os as _os

logger = _log.getLogger()
logger.disabled = True

def LoadStl(fileName) : 
    reg = _g4.Registry()
    r = _stl.Reader(fileName)    
    l = r.logicalVolume("test","G4_Cu",reg)
        
    return True,l

def _pj(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

class StlTests(_unittest.TestCase) :
    def testLoadStlDog(self) :
        ret,l = LoadStl(_pj("dog.stl"))
        self.assertTrue(ret)
                
    def testLoadStlDragon(self) :
        self.assertTrue(LoadStl(_pj("dragon.stl")))

    def testLoadStlRobot(self) :
        self.assertTrue(LoadStl(_pj("robot.stl")))

    def testLoadStlTeapot(self) :
        self.assertTrue(LoadStl(_pj("utahteapot.stl")))
            
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
