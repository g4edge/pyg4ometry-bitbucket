import pyg4ometry as _pyg4
import os as _os
import numpy as _np

def Test(vis=True, interactive=True):

    reg = _pyg4.geant4.Registry()
    radius1 = 7
    radius2 = 9
    t = _pyg4.geant4.solid.CutTubs("t1", radius1, radius2, 50, 0, 2 * _np.pi, [0, 0, -1], [0, 0, 1], reg)

    stlFileName = _os.path.join(_os.path.dirname(__file__), "T721_featureExtract_cutTubs.stl")
    datFileName = stlFileName.replace("stl","dat")
    _pyg4.convert.pycsgMeshToStl(t.mesh(),stlFileName)

    p1 = _pyg4.features.algos.Plane([0,0,0],[0,0,1])
    r = _pyg4.features.extract(stlFileName, circumference=2*_np.pi*8, planes=[p1], outputFileName=datFileName, bViewer=vis)

    fd = _pyg4.features.algos.FeatureData()
    fd.readFile(datFileName)

    return True

if __name__ == "__main__":
    Test()