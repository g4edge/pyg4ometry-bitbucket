import pyg4ometry as _pyg4
import os as _os
import numpy as _np

def Test(vis=True, interactive=True):

    reg = _pyg4.geant4.Registry()
    radius1 = 7
    radius2 = 9
    theta = 0.25
    rho = 500

    s = theta*rho
    d = _np.sin(theta/2.)*rho*2

    n1 = [_np.cos(_np.pi/2-theta/2.0),0,-_np.sin(_np.pi/2-theta/2.0)]
    n2 = [_np.cos(_np.pi/2-theta/2.0),0, _np.sin(_np.pi/2-theta/2.0)]

    print(n1)
    print(n2)

    t = _pyg4.geant4.solid.CutTubs("t1", radius1, radius2, d, 0, 2 * _np.pi,n1,n2,reg)

    stlFileName = _os.path.join(_os.path.dirname(__file__), "T721_featureExtract_cutTubs.stl")
    datFileName = stlFileName.replace("stl","dat")
    _pyg4.convert.pycsgMeshToStl(t.mesh(),stlFileName)

    p1 = _pyg4.features.algos.Plane([0,0,0],[0,0,1])
    r = _pyg4.features.extract(stlFileName, angle = 45, circumference=2*_np.pi*8, planes=[p1], outputFileName=datFileName, bViewer=vis)

    fd = _pyg4.features.algos.FeatureData()
    fd.readFile(datFileName)

    return True

if __name__ == "__main__":
    Test()