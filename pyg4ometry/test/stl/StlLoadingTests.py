import unittest as _unittest

import pyg4ometry.geant4 as _g4
import pyg4ometry.stl as _stl

import logging as _log

logger = _log.getLogger()
logger.disabled = True

def LoadStl(fileName) : 
    reg = _g4.Registry()
    r = _stl.Reader(fileName)    
    l = r.logicalVolume("test",reg)
    
    return True

class StlTests(_unittest.TestCase) :
    def testLoadStlDog(self) :
        self.assertTrue(LoadStl("dog.stl"))

    def testLoadStlDragon(self) :
        self.assertTrue(LoadStl("dragon.stl"))

    def testLoadStlRobot(self) :
        self.assertTrue(LoadStl("robot.stl"))

    def testLoadStlTeapot(self) :
        self.assertTrue(LoadStl("utahteapot.stl"))

    
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
