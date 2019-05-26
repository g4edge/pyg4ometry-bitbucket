#!/opt/local/bin/python

from freecad import FreecadLoadingTests
from python  import PythonTests
from python  import PythonDefineTests
from python  import PythonAuthoringTests
from gdml    import GdmlLoadTests
from stl     import StlLoadingTests

import unittest as _unittest
import logging as _log

logger = _log.getLogger()
logger.disabled = True

if __name__ == '__main__':
    _unittest.main(verbosity=2)
