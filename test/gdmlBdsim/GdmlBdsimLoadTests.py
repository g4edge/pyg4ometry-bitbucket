import os as _os
from os import path as _path
import unittest as _unittest

import pyg4ometry
import pyg4ometry.convert as _convert
import pyg4ometry.fluka as _fluka


def localPath(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

def localFile(filename) :
    return _os.path.join(_os.path.dirname(__file__), filename)

def gdmlBdsimLoadTest(filename, vis = False, interactive=False, reduceNISTMaterialsToPredefined=False):
    filepath = localPath(filename)

    # Loading
    reader = pyg4ometry.gdml.Reader(filepath, reduceNISTMaterialsToPredefined=reduceNISTMaterialsToPredefined)
    registry = reader.getRegistry()

    worldLogical = registry.getWorldVolume()

    # test extent of physical volume
    extentBB = worldLogical.extent(includeBoundingSolid=True)

    # Visualisation
    v = None
    if vis :
        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(worldLogical)
        v.setRandomColours()
        v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)

    # Fluka writer
    freg = _convert.geant4Reg2FlukaReg(registry)

    w = _fluka.Writer()
    w.addDetector(freg)
    w.write(_path.join(_os.path.dirname(__file__),_path.basename(filename).split(".")[0]+".inp"))

    # flair output file
    f = _fluka.Flair(_path.basename(filename).split(".")[0]+".inp",extentBB)
    f.write(_path.join(_path.dirname(__file__),_path.basename(filename).split(".")[0]+".flair"))

    # Render writer
    rw = pyg4ometry.visualisation.RenderWriter()
    rw.addLogicalVolumeRecursive(worldLogical)
    rw.write(localFile(_os.path.basename(filename).split(".")[0]+"_renderWriter"))

    return {"logicalVolume":worldLogical,"registy":registry, "vtkViewer":v, "renderWriter":rw}


class GdmlBdsimLoadTests(_unittest.TestCase):
    def test_GdmlBdsimLoad_001_001_Layout(self):
        ret = gdmlBdsimLoadTest("001_001_layout.gdml")

    def test_GdmlBdsimLoad_001_002_One_Of_Each(self):
        ret = gdmlBdsimLoadTest("001_002_one_of_each.gdml")

    def test_Gdml_reduceNISTMaterialsToPredefined(self):
        ret = gdmlBdsimLoadTest("001_005_beamline_transform.gdml", reduceNISTMaterialsToPredefined=True)

if __name__ == '__main__':
    _unittest.main(verbosity=2)
