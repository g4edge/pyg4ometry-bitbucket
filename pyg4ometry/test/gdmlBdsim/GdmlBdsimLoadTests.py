import unittest as _unittest
import os as _os

import pyg4ometry

def localPath(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)

def localFile(filename) :
    return _os.path.join(_os.path.dirname(__file__), filename)

def gdmlBdsimLoadTest(filename, vis = False, interactive=False):
    filepath = localPath(filename)

    # Loading
    reader = pyg4ometry.gdml.Reader(filepath)
    registry = reader.getRegistry()

    # World logical
    worldLogical = registry.getWorldVolume()

    # test extent of physical volume
    extentBB = worldLogical.extent(includeBoundingSolid=True)

    # Visualisation
    v = None
    if vis :
        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(registry.getWorldVolume())
        v.addAxes(pyg4ometry.visualisation.axesFromExtents(extentBB)[0])
        v.view(interactive=interactive)

    # Render writer
    rw = pyg4ometry.visualisation.RenderWriter()
    rw.addLogicalVolumeRecursive(worldLogical)
    rw.write(localFile(_os.path.basename(filename).split(".")[0]+"_renderWriter"))

    return {"logicalVolume":worldLogical,"registy":registry, "vtkViewer":v, "renderWriter":rw}


class GdmlBdsimLoadTests(_unittest.TestCase) :
    def test_GdmlBdsimLoad_001_001_Layout(self):
        ret = gdmlBdsimLoadTest("001_001_layout.gdml")

if __name__ == '__main__':
    _unittest.main(verbosity=2)
