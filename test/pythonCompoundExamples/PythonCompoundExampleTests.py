import unittest as _unittest

import pyg4ometry

from . import DipoleCbpm
from . import VacuumSystems
from . import Support

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonCompoundExampleTests(_unittest.TestCase) :
    def test_CavityBpm(self) :
        DipoleCbpm.Test(False,False)

    def test_SphericalChamber(self):
        VacuumSystems.Test(False,False)

    def test_SupportTable(self):
        Support.Test(False,False)

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
