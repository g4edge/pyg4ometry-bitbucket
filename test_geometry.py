#!/usr/bin/env python
import unittest
import pyfluka
from pyfluka import vector
import numpy as np
from math import pi
import os.path as _path
import pygdml
import collections

INP_PATH = _path.dirname(_path.abspath(__file__)) + "/test_input/"

class TestPLA(unittest.TestCase):
    pass

class TestRCC(object):
    # Inherit from `object` so unittest doesn't think these are tests which
    # should be run

    @classmethod
    def setUpClass(cls):
        model = pyfluka.Model(INP_PATH + "RCC.INP")
        cls.region = model.regions[cls.region_name]

    def test_rescaled_mesh(self):
        unopt = self.region.evaluate(optimise=False)
        opt = self.region.evaluate(optimise=True)

        unopt_extent = unopt._extent()
        opt_extent = opt._extent()
        self.assertEqual(unopt_extent, opt_extent)

    def test_minimisation(self):
        unopt = self.region.evaluate(optimise=False)
        opt = self.region.evaluate(optimise=True)

        unopt_extent = unopt._extent()
        opt_extent = opt._extent()

        areless = []
        for opt_solid, unopt_solid in zip(
                opt.gdml_primitives(),
                unopt.gdml_primitives()):
            areless.append(solid_less_than(opt_solid, unopt_solid))
        self.assertTrue(any(areless))

def tubs_extent(radius, length, rotation, position):
    tubs = pygdml.Tubs("tubs", 0.0, radius, length * 0.5, 0.0, 2*pi)
    w = pygdml.Box("world", 1000, 1000, 1000)
    world_volume = pygdml.Volume([0, 0, 0], [0, 0, 0], w,
                                 "world-volume", None,
                                 1, False, "G4_NITROUS_OXIDE")
    rotation = [0.0, pi/2, 0]
    volume = pygdml.Volume(pygdml.reverse(rotation),
                           position,
                           tubs,
                           "",
                           world_volume,
                           1,
                           False,
                           "G4_Cu")
    # world_volume.setClip()
    mesh = world_volume.pycsgmesh()
    # viewer = pygdml.VtkViewer()
    # viewer.addSource(mesh)
    # viewer.view()
    extent =  pygdml.volume.pycsg_extent(mesh)

    _MeshInfo = collections.namedtuple("_MeshInfo", ['centre', 'min',
                                                     'max', 'length'])
    lower = vector.Three(extent[0].x, extent[0].y, extent[0].z)
    upper = vector.Three(extent[1].x, extent[1].y, extent[1].z)
    size = upper - lower
    centre = upper - size / 2
    return _MeshInfo(centre, lower, upper, size)


# These four tests for the four possible cases when rescaling an RCC:
# None:  Neither face lies on or within the resulting zone.
# Both:  Both faces lie on or within the resulting zone.
# One:  One face lies within or on the resulting zone.
# Other: Other faces lies within or on the resulting zone.

params = [('None', 'none', tubs_extent(50, 500, [0, pi/2, 0],
                                       [10000., 10000., 10000.])),
          ('Both', 'both', tubs_extent(50, 200.,
                                       [0, pi/2, 0],
                                       [10000., 10000., 10000.])),
          ('One', 'one', tubs_extent(50., 250., [0, pi/2, 0],
                                     [11250., 10000., 10000.])),
          ('Other', 'other', tubs_extent(50., 250., [0, pi/2, 0],
                                         [11250., 10000., 10000.]))]

for name, param, centre in params:
    cls_name = "TestRCC{}FacesIn".format(name)
    globals()[cls_name] = type(cls_name, (TestRCC, unittest.TestCase), {
        "region_name": param,
        "centre": 1,
        "length": 2
    })

class TestREC(unittest.TestCase):
    pass

class TestRPP(unittest.TestCase):
    pass

class TestSPH(unittest.TestCase):
    pass

class TestTRC(unittest.TestCase):
    pass

class TestXCC(unittest.TestCase):
    def setUp(self):
        self.model = pyfluka.model.Model(INP_PATH + "XCC.inp")

    def test_crude_rescale(self):
        region = self.model.regions['min']
        boolean = region.evaluate(optimise=False)
        extent = boolean._extent()
        self.assertEqual(extent.centre, vector.Three(10000., 10000., 10000.))
        self.assertEqual(extent.length, vector.Three(400., 300., 300.))

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


class TestXEC(unittest.TestCase):
    pass

class TestXYP(unittest.TestCase):
    def setUp(self):
        self.model = pyfluka.model.Model(INP_PATH + "XYP.inp")

    def test_crude_rescale(self):
        region = self.model.regions['min']
        boolean = region.evaluate(optimise=False)
        extent = boolean._extent()
        self.assertEqual(extent.centre, vector.Three(10000., 10000., 10000.))
        self.assertEqual(extent.length, vector.Three(400., 400., 200.))

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
    def setUp(self):
        self.model = pyfluka.model.Model(INP_PATH + "YCC.inp")

    def test_crude_rescale(self):
        region = self.model.regions['min']
        boolean = region.evaluate(optimise=False)
        extent = boolean._extent()
        self.assertEqual(extent.centre, vector.Three(10000., 10000., 10000.))
        self.assertEqual(extent.length, vector.Three(300., 400., 300.))

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


class TestYEC(unittest.TestCase):
    pass

class TestYZP(unittest.TestCase):
    def setUp(self):
        self.model = pyfluka.model.Model(INP_PATH + "YZP.inp")

    def test_crude_rescale(self):
        region = self.model.regions['min']
        boolean = region.evaluate(optimise=False)
        extent = boolean._extent()
        self.assertEqual(extent.centre, vector.Three(10000., 10000., 10000.))
        self.assertEqual(extent.length, vector.Three(200., 400., 400.))

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

class TestZCC(unittest.TestCase):
    def setUp(self):
        self.model = pyfluka.model.Model(INP_PATH + "ZCC.inp")

    def test_crude_rescale(self):
        region = self.model.regions['min']
        boolean = region.evaluate(optimise=False)
        extent = boolean._extent()
        self.assertEqual(extent.centre, vector.Three(10000., 10000., 10000.))
        self.assertEqual(extent.length, vector.Three(300., 300., 400.))

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
