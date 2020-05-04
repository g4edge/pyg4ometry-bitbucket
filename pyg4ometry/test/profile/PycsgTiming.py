import pyg4ometry as _pyg4ometry
import random as _random
import timeit as _timeit
import numpy as _np
import matplotlib.pyplot as _plt

import time as _time


def plotData(data):
    _plt.subplot(2,2,1)
    _plt.plot(data[:,0],data[:,1])
    _plt.xlabel("$N_{\\rm subtraction}$")
    _plt.ylabel("$N_{\\rm polygon}$")

    _plt.subplot(2,2,2)
    _plt.plot(data[:,0],data[:,2])
    _plt.xlabel("$N_{\\rm subtraction}$")
    _plt.ylabel("$\\Delta t/s $")


    _plt.subplot(2,2,3)
    _plt.plot(data[:,1],data[:,2])
    _plt.xlabel("$N_{\\rm poly}$")
    _plt.ylabel("$\\Delta t/s $")

def test_T001_PycsgTiming_Union():
    reg = _pyg4ometry.geant4.Registry()

    s = _pyg4ometry.geant4.solid.Box("box1", 100, 100, 100, reg, "mm", False)

    m1 = s.pycsgmesh()
    m2 = s.pycsgmesh()

    n = 50
    data = _np.zeros((n,3))

    for i in range(0,n,1):
        xr = (_random.random()-0.5)
        yr = (_random.random()-0.5)
        zr = (_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2.translate([0,0,0])
        m2.rotate([xd,yd,zd],ra)

        def wrappedUnion():
            t0 = _time.time()
            mr = m1.union(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt = wrappedUnion()

        data[i,0] = i
        data[i,1] = len(m1.polygons)
        data[i,2] = dt
        print(i,data[i,1],dt)

    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)


def test_T002_pycsgTiming_Intersection():
    reg = _pyg4ometry.geant4.Registry()

    s = _pyg4ometry.geant4.solid.Box("box1", 100, 100, 100, reg, "mm", False)

    m1 = s.pycsgmesh()
    m2 = s.pycsgmesh()

    n = 50
    data = _np.zeros((n,3))

    for i in range(0,n,1):
        xr = (_random.random()-0.5)
        yr = (_random.random()-0.5)
        zr = (_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2.translate([0,0,0])
        m2.rotate([xd,yd,zd],ra)

        def wrappedIntersection():
            t0 = _time.time()
            mr = m1.intersect(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt  = wrappedIntersection()

        data[i,0] = i
        data[i,1] = len(m1.polygons)
        data[i,2] = dt
        print(i,data[i,1],dt)

    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)


def test_T003_pycsg_Timing_Difference():
    reg = _pyg4ometry.geant4.Registry()

    s1 = _pyg4ometry.geant4.solid.Box("box1", 2, 2, 2, reg, "mm", False)
    s2 = _pyg4ometry.geant4.solid.Box("box2", 1, 1, 1, reg, "mm", False)

    m1 = s1.pycsgmesh()
    m2 = s2.pycsgmesh()

    n = 50
    data = _np.zeros((n,3))

    for i in range(0,n,1):

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2 = s2.pycsgmesh()
        m2.translate([0,0,0])
        m2.rotate([xd,yd,zd],ra)

        def wrappedSubtraction():
            t0 = _time.time()
            mr = m1.subtract(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt = wrappedSubtraction()

        data[i,0] = i
        data[i,1] = len(m1.polygons)
        data[i,2] = dt
        print(i,data[i,1],dt)


    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)
