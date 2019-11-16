import unittest as _unittest

import pyg4ometry

import dipole_cbpm

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonCompoundExampleTests(_unittest.TestCase) :
    def testCavityBpm(self) :         
        dipole_cbpm.dipole_cbpm()
    
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
