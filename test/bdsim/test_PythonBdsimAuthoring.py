from pyg4ometry.bdsim import Sampler as _Sampler
from pyg4ometry.bdsim import ScoringMesh as _ScoringMesh

def test_PythonBdsim_T001_Sampler() :
    s = _Sampler("sampler1",[0,0,0],[0,0,0],"circular",[1,2,3,4])

    try :
        s = _Sampler("sampler1", [0, 0, 0], [0, 0, 0], "circular", [1, 2, 3, 4, 5])
    except ValueError :
        pass

def test_PythonBdsim_T002_ScoringMesh():
    s = _ScoringMesh("mesh1",[0,0,0],[0,0,0],"E",[10,10,10],[150,150])


