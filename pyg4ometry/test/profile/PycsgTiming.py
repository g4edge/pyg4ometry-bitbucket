import pyg4ometry
import random as _random
import timeit as _timeit
import numpy as _np


def test_T001_PycsgTiming_Union():
    reg = pyg4ometry.geant4.Registry()

    s = pyg4ometry.geant4.solid.Box("box1", 100, 100, 100, reg, "mm", False)

    m1 = s.pycsgmesh()
    m2 = s.pycsgmesh()

    for i in range(0,50,1):
        xr = (_random.random()-0.5)
        yr = (_random.random()-0.5)
        zr = (_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2.translate([0,0,0])
        m2.rotate([xd,yd,zd],ra)
        mi = m1.union(m2)
        m1 = mi

        print(i,len(m1.polygons))

    v = pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(mi)
    v.view(interactive=True)


def test_T002_pycsgTiming_Intersection():
    reg = pyg4ometry.geant4.Registry()

    s = pyg4ometry.geant4.solid.Box("box1", 100, 100, 100, reg, "mm", False)

    m1 = s.pycsgmesh()
    m2 = s.pycsgmesh()

    for i in range(0,50,1):
        xr = (_random.random()-0.5)
        yr = (_random.random()-0.5)
        zr = (_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2.translate([0,0,0])
        m2.rotate([xd,yd,zd],ra)
        mi = m1.intersect(m2)
        m1 = mi

        print(i,len(m1.polygons))

    v = pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(mi)
    v.view(interactive=True)


def test_T003_pycsg_Timing_Difference():
    reg = pyg4ometry.geant4.Registry()

    s1 = pyg4ometry.geant4.solid.Box("box1", 2, 2, 2, reg, "mm", False)
    s2 = pyg4ometry.geant4.solid.Box("box2", 1, 1, 1, reg, "mm", False)

    m1 = s1.pycsgmesh()
    m2 = s2.pycsgmesh()

    for i in range(0,50,1):

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2 = s2.pycsgmesh()
        m2.translate([0,0,0])
        m2.rotate([xd,yd,zd],ra)
        ms = m1.subtract(m2)
        m1 = ms

        print(i,len(m1.polygons))

    v = pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(ms)
    v.view(interactive=True)
