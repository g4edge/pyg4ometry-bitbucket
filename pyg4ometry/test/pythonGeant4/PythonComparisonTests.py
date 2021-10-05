import unittest as _unittest
import testtools as _testtools
import numpy as _np

import pyg4ometry

from . import T700_ComparisonMaterial

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonComparisonTests(_unittest.TestCase):

    def test_PythonComparison_T700_ComparisonMaterial(self):
        self.assertTrue(T700_ComparisonMaterial.Test())




if __name__ == '__main__':
    _unittest.main(verbosity=2)
