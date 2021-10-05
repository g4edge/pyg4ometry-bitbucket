import unittest as _unittest
import testtools as _testtools
import numpy as _np

import pyg4ometry

from . import T700_ComparisonMaterial
from . import T701_ComparisonSolid
from . import T702_ComparisonLogicalVolume
from . import T703_ComparisonPhysicalVolume
from . import T704_ComparisonAssemblyVolume
from . import T705_ComparisonReplicaVolume
from . import T706_ComparisonDivisionVolume
from . import T707_ComparisonParameterisedVolume

import logging as _log

#logger = _log.getLogger()
#logger.disabled = True

class PythonComparisonTests(_unittest.TestCase):
    def test_PythonComparison_T700_ComparisonMaterial(self):
        self.assertTrue(T700_ComparisonMaterial.Test())

    def test_PythonComparison_T701_ComparisonSolid(self):
        self.assertTrue(T701_ComparisonSolid.Test())

    def test_PythonComparison_T702_ComparisonLogicalVolume(self):
        self.assertTrue(T702_ComparisonLogicalVolume.Test())

    def test_PythonComparison_T703_ComparisonPhysicalVolume(self):
        self.assertTrue(T703_ComparisonPhysicalVolume.Test())

    def test_PythonComparison_T704_ComparisonAssemblyVolume(self):
        self.assertTrue(T704_ComparisonAssemblyVolume.Test())

    def test_PythonComparison_T705_ComparisonReplicaVolume(self):
        self.assertTrue(T705_ComparisonReplicaVolume.Test())

    def test_PythonComparison_T706_ComparisonDivisionVolume(self):
        self.assertTrue(T706_ComparisonDivisionVolume.Test())

    def test_PythonComparison_T707_ComparisonParameterisedVolume(self):
        self.assertTrue(T707_ComparisonParameterisedVolume.Test())

if __name__ == '__main__':
    _unittest.main(verbosity=2)
