import unittest as _unittest

import pyg4ometry

import dipole_cbpm

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonCompoundExampleTests(_unittest.TestCase) :
    def test_CavityBpm(self) :
        dipole_cbpm.Test(True,False)
    
if __name__ == '__main__':
    _unittest.main(verbosity=2)        
