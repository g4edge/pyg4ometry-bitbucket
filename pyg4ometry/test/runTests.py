#!/opt/local/bin/python

from freecadExamples        import FreecadLoadingTests
from pythonGeant4           import PythonTests
from pythonGeant4           import PythonDefineTests
from pythonGeant4           import PythonGeantAuthoringTests
from pythonCompoundExamples import PythonCompoundExampleTests
from gdml                   import GdmlLoadTests
from stl                    import StlLoadTests
from pythonFluka            import PythonFlukaAuthoringTests
from geant42Fluka           import Geant42FlukaConversionTests
from flairFluka             import FlairLoadTests
from bdsim                  import PythonBdsimAuthoringTests

import unittest as _unittest
import logging as _log

logger = _log.getLogger()
logger.disabled = True

if __name__ == '__main__':
    _unittest.main(verbosity=2)
