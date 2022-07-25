import pyg4ometry as _pyg4
import os as _os

def Test(vis=True, interactive=True):
    pathToStl  = _os.path.dirname(_pyg4.__file__)+"/test/stl/ST0372507_01_a.stl"
    p1 = _pyg4.features.algos.Plane([0,0,0],[1,0,0])
    p2 = _pyg4.features.algos.Plane([50, 0, 0], [1, 0, 0])
    r = _pyg4.features.extract(pathToStl,
                               planes=[p1,p2],
                               outputFileName=_os.path.join(_os.path.dirname(__file__), "T720_featureExtract.dat"),
                               bViewer=vis)

    return True

if __name__ == "__main__":
    Test()
