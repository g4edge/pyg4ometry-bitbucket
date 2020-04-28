import unittest as _unittest
import os as _os

import pyg4ometry.geant4 as _g4
import pyg4ometry.stl as _stl

import logging as _log
import os as _os

logger = _log.getLogger()
logger.disabled = True

def LoadStl(fileName) : 
    reg = _g4.Registry()
    r = _stl.Reader(fileName, registry=reg)
    s = r.getSolid()
        
    return True, s

def _pj(filename): # path join
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

class StlLoadTests(_unittest.TestCase) :
    def test_StlLoad_Dog(self) :
        ret,s = LoadStl(_pj("dog.stl"))
        self.assertTrue(ret)
                
    def test_StlLoad_Dragon(self) :
        self.assertTrue(LoadStl(_pj("dragon.stl")))

    # def test_StlLoad_Robot(self) :
    # robot.stl is in binary format
    #     self.assertTrue(LoadStl(_pj("robot.stl")))

    def test_StlLoad_Teapot(self) :
        self.assertTrue(LoadStl(_pj("utahteapot.stl")))

    def test_StlWrite_T001_Box(self):
        import pyg4ometry.test.pythonGeant4.T001_Box
        import pyg4ometry.visualisation.Convert
        import pyg4ometry.visualisation.Writer

        r = pyg4ometry.test.pythonGeant4.T001_Box.Test(False,False)
        lv = r['logicalVolume']
        m  = lv.daughterVolumes[0].logicalVolume.mesh.localmesh
        pd = pyg4ometry.visualisation.Convert.pycsgMeshToVtkPolyData(m)
        pyg4ometry.visualisation.Writer.writeVtkPolyDataAsSTLFile(_os.path.join(_os.path.dirname(__file__),"T001_Box.stl"),[pd])

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
