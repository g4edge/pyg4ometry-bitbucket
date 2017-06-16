#!/usr/bin/env python
import unittest
import pyfluka
from pyfluka import vector
import numpy as np
import os.path as _path
import pygdml as _pgydml

INP_PATH = _path.dirname(_path.abspath(__file__)) + "/test_input/"

class TestPLA(unittest.TestCase):
    pass

class TestRCC(unittest.TestCase):
    pass

class TestREC(unittest.TestCase):
    pass

class TestRPP(unittest.TestCase):
    pass

class TestSPH(unittest.TestCase):
    pass

class TestTRC(unittest.TestCase):
    pass

class TestXCC(unittest.TestCase):
    pass

class TestXEC(unittest.TestCase):
    pass

class TestXYP(unittest.TestCase):
    pass

class TestXZP(unittest.TestCase):
    def setUp(self):
        self.model = pyfluka.model.Model(INP_PATH + "XZP.inp")

    def test_crude_rescale(self):
        region = self.model.regions['min']
        boolean = region.evaluate(optimise=False)
        extent = boolean._extent()
        self.assertEqual(extent.centre, vector.Three(10000., 10000., 10000.))
        self.assertEqual(extent.length, vector.Three(400., 200., 400.))

    def test_rescaled_mesh(self):
        region = self.model.regions['min']

        unopt = region.evaluate(optimise=False)
        opt = region.evaluate(optimise=True)

        unopt_extent = unopt._extent()
        opt_extent = opt._extent()
        self.assertEqual(unopt_extent, opt_extent)

    def test_minimisation(self):
        region = self.model.regions['min']

        unopt = region.evaluate(optimise=False)
        opt = region.evaluate(optimise=True)

        unopt_extent = unopt._extent()
        opt_extent = opt._extent()

        areless = []
        for opt_solid, unopt_solid in zip(
                opt.gdml_primitives(),
                unopt.gdml_primitives()):
            areless.append(solid_less_than(opt_solid, unopt_solid))
        self.assertTrue(any(areless))


class PLAMinimisation(unittest.TestCase):
    pass

class TestYCC(unittest.TestCase):
    pass

class TestYEC(unittest.TestCase):
    pass

class TestYZP(unittest.TestCase):
    pass

class TestZCC(unittest.TestCase):
    pass

class TestZEC(unittest.TestCase):
    pass

def solid_less_than(solid1, solid2):
    try:
        return (solid1.pX < solid2.pX
                or solid1.pY < solid2.pY
                or solid1.pZ < solid2.pZ)
    except AttributeError:
        pass

    try:
        return solid1.pDz < solid2.pDz
    except AttributeError:
        pass

    return None


if __name__ == '__main__':
    unittest.main()
