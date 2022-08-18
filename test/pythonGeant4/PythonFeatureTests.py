import unittest as _unittest
import testtools as _testtools

from . import T720_featureExtract
from . import T721_featureExtract_cutTubs

class PythonFeatureTests(_unittest.TestCase):
    def test_PythonFeature_T720_featureExtract(self):
        self.assertTrue(T720_featureExtract.Test(False,False))

    def test_PythonFeature_T710_featureExtract_cutTubs(self):
        self.assertTrue(T721_featureExtract_cutTubs.Test(False,False))