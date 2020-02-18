import unittest as _unittest

import pyg4ometry

import DipoleCbpm
import VacuumSystems
import Support

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonCompoundExampleTests(_unittest.TestCase) :
    def test_CavityBpm(self) :
        DipoleCbpm.Test(True,False)

    def test_SphericalChamber(self):
        VacuumSystems.Test(True,False)

    def test_SupportTable(self):
        Support.Test(True,False)

if __name__ == '__main__':
    _unittest.main(verbosity=2)        
