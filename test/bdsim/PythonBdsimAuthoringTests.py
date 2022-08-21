import unittest as _unittest

from pyg4ometry.bdsim import Sampler as _Sampler
from pyg4ometry.bdsim import ScoringMesh as _ScoringMesh

class PythonBdsimAuthoringTests(_unittest.TestCase) :
    def test_PythonBdsim_T001_Sampler(self) :
        s = _Sampler("sampler1",[0,0,0],[0,0,0],"circular",[1,2,3,4])

        try :
            s = _Sampler("sampler1", [0, 0, 0], [0, 0, 0], "circular", [1, 2, 3, 4, 5])
        except ValueError :
            pass


    def test_PythonBdsim_T002_ScoringMesh(self):
        s = _ScoringMesh("mesh1",[0,0,0],[0,0,0],"E",[10,10,10],[150,150])

if __name__ == '__main__':
    _unittest.main(verbosity=2)

