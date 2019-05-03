from python import PythonAuthoringTests, PythonDefineTests
from gdml import GdmlLoadTests

import unittest as _unittest
import logging as _log

logger = _log.getLogger()
logger.disabled = True

if __name__ == '__main__':
    _unittest.main(verbosity=0)



