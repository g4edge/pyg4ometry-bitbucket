import pyg4ometry

from . import DipoleCbpm
from . import VacuumSystems
from . import Support

def test_CavityBpm() :
    DipoleCbpm.Test(False,False)

def test_SphericalChamber():
    VacuumSystems.Test(False,False)

def test_SupportTable():
    Support.Test(False,False)

