import pyg4ometry as _pyg4ometry
import random as _random
import timeit as _timeit
import numpy as _np
import matplotlib.pyplot as _plt

import time as _time


def cube(center=[0, 0, 0], radius=1):
    c = _pyg4ometry.pycgal.geom.Vector(0, 0, 0)
    r = [1, 1, 1]
    if isinstance(center, list): c = _pyg4ometry.pycgal.geom.Vector(center)
    if isinstance(radius, list):
        r = radius
    else:
        r = [radius, radius, radius]

    polygons = list([_pyg4ometry.pycgal.geom.Polygon(
        list([_pyg4ometry.pycgal.geom.Vertex(
            _pyg4ometry.pycgal.geom.Vector(
                c.x + r[0] * (2 * bool(i & 1) - 1),
                c.y + r[1] * (2 * bool(i & 2) - 1),
                c.z + r[2] * (2 * bool(i & 4) - 1)
            )
        ) for i in v[0]])) for v in [
        [[0, 4, 6, 2], [-1, 0, 0]],
        [[1, 3, 7, 5], [+1, 0, 0]],
        [[0, 1, 5, 4], [0, -1, 0]],
        [[2, 6, 7, 3], [0, +1, 0]],
        [[0, 2, 3, 1], [0, 0, -1]],
        [[4, 5, 7, 6], [0, 0, +1]]
    ]])

    c1 = _pyg4ometry.pycgal.core.CSG.fromPolygons(polygons)

    return c1

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

def test_T001_PycgalTiming_Union():

    m1 = cube([0,0,0],1)


    n = 1000
    data = _np.zeros((n,3))

    for i in range(0,n,1):
        xr = (3*(_random.random()-0.5))
        yr = (3*(_random.random()-0.5))
        zr = (3*(_random.random()-0.5))

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        m2 = cube([0, 0, 0],_random.random())
        ra = 360*_random.random()

        # m2.rotate([xd,yd,zd],ra)
        m2.translate([xr,yr,zr])

        def wrappedUnion():
            t0 = _time.time()
            mr = m1.union(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt = wrappedUnion()

        data[i,0] = i
        data[i,1] = float(m1.getNumberPolys())
        data[i,2] = dt
        print(i,data[i,1],dt)

    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)


def test_T002_pycgalTiming_Intersection():

    m1 = cube([0,0,0],1)

    n = 1000
    data = _np.zeros((n,3))

    for i in range(0,n,1):
        xr = 2*(_random.random()-0.5)
        yr = 2*(_random.random()-0.5)
        zr = 2*(_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2 = cube([0, 0, 0], 1)
        m2.translate([xr,yr,zr])
        # m2.rotate([xd,yd,zd],ra)

        def wrappedIntersection():
            t0 = _time.time()
            mr = m1.intersect(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt  = wrappedIntersection()

        data[i,0] = i
        data[i,1] = float(m1.getNumberPolys())
        data[i,2] = dt
        print(i,data[i,1],dt)

    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)


def test_T003_pycgal_Timing_Difference():
    m1 = cube([0,0,0],50)

    n = 1000
    data = _np.zeros((n,3))

    for i in range(0,n,1):

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2 = cube([0, 0, 0], 1)
        m2.translate([100*(_random.random()-0.5),100*(_random.random()-0.5),100*(_random.random()-0.5)])
        m2.rotate([xd,yd,zd],ra)

        def wrappedSubtraction():
            t0 = _time.time()
            mr = m1.subtract(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt = wrappedSubtraction()

        data[i,0] = i
        data[i,1] = float(m1.getNumberPolys())
        data[i,2] = dt
        print(i,data[i,1],dt)


    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)
