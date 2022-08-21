import pyg4ometry as _pyg4ometry
import random as _random
import time as _time
import numpy as _np
import matplotlib.pyplot as _plt

def plotData(data):
    _plt.subplot(2,2,1)
    _plt.plot(data[:,0],data[:,1],"o")
    _plt.xlabel("$N_{\\rm subtraction}$")
    _plt.ylabel("$N_{\\rm polygon}$")

    _plt.subplot(2,2,2)
    _plt.plot(data[:,0],data[:,2],"o")
    _plt.xlabel("$N_{\\rm subtraction}$")
    _plt.ylabel("$\\Delta t/s $")

    _plt.subplot(2,2,3)
    _plt.plot(data[:,1],data[:,2],"o")
    _plt.xlabel("$N_{\\rm poly}$")
    _plt.ylabel("$\\Delta t/s $")

def test_T001_Timing_Union(nOperation = 50, fileName = "T001_Timing_Union"):

    reg = _pyg4ometry.geant4.Registry()
    s1 = _pyg4ometry.geant4.solid.Box("box1", 1, 1, 1, reg, "mm", False)

    m1 = s1.mesh()

    data = _np.zeros((nOperation,3))

    f = open(fileName+"_"+str(_pyg4ometry.config.meshing)+".dat","w")

    for i in range(0,nOperation,1):
        xr = 3*(_random.random()-0.5)
        yr = 3*(_random.random()-0.5)
        zr = 3*(_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        s2 = _pyg4ometry.geant4.solid.Box("box2",
                                          2*_random.random(),
                                          2*_random.random(),
                                          2*_random.random(), reg, "mm", False)
        m2 = s2.mesh()
        m2.rotate([xd,yd,zd],ra)
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

        timingLine = str(i)+" "+str(int(data[i,1]))+" "+str(dt)
        print(timingLine)
        f.write(timingLine+"\n")

    f.close()
    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)


def test_T002_Timing_Intersection(nOperation = 50, fileName = "T002_Timing_Intersection"):

    reg = _pyg4ometry.geant4.Registry()
    s1 = _pyg4ometry.geant4.solid.Box("box1", 1, 1, 1, reg, "mm", False)
    s2 = _pyg4ometry.geant4.solid.Box("box2", 1, 1, 1, reg, "mm", False)

    m1 = s1.mesh()

    data = _np.zeros((nOperation,3))

    f = open(fileName+"_"+str(_pyg4ometry.config.meshing)+".dat","w")

    for i in range(0,nOperation,1):
        xr = 0.75*(_random.random()-0.5)
        yr = 0.75*(_random.random()-0.5)
        zr = 0.75*(_random.random()-0.5)

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2 = s1.mesh()
        m2.translate([xr,yr,zr])
        m2.rotate([xd,yd,zd],ra)

        def wrappedIntersection():
            t0 = _time.time()
            mr = m1.intersect(m2)
            t1 = _time.time()
            return mr, t1-t0

        m1, dt  = wrappedIntersection()

        data[i,0] = i
        data[i,1] = float(m1.getNumberPolys())
        data[i,2] = dt

        timingLine = str(i)+" "+str(int(data[i,1]))+" "+str(dt)
        print(timingLine)
        f.write(timingLine+"\n")

    f.close()
    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)


def test_T003_Timing_Difference(nOperation = 50, fileName = "T003_Timing_Difference"):
    reg = _pyg4ometry.geant4.Registry()
    s1 = _pyg4ometry.geant4.solid.Box("box1",100,100,100, reg, "mm", False)
    s2 = _pyg4ometry.geant4.solid.Box("box1",  1,  1,  1, reg, "mm", False)

    m1 = s1.mesh()

    data = _np.zeros((nOperation,3))

    f = open(fileName+"_"+str(_pyg4ometry.config.meshing)+".dat","w")

    for i in range(0,nOperation,1):

        xd = _random.random()
        yd = _random.random()
        zd = _np.sqrt(xd**2+yd**2)
        ra = 360*_random.random()

        m2 = s2.mesh()
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

        timingLine = str(i)+" "+str(int(data[i,1]))+" "+str(dt)
        print(timingLine)
        f.write(timingLine+"\n")

    f.close()
    plotData(data)

    v = _pyg4ometry.visualisation.VtkViewer()
    v.addMeshSimple(m1)
    v.view(interactive=True)

def ComparisionPlot(timingFile1, timingFile2) :
    data1 = _np.loadtxt(timingFile1)
    data2 = _np.loadtxt(timingFile2)

    fig = _plt.figure(1)

    _plt.subplot(2,2,1)
    _plt.semilogy(data1[:,0],data1[:,1],"-")
    _plt.semilogy(data2[:,0],data2[:,1],"-")
    _plt.xlabel("$N_{\\rm subtraction}$")
    _plt.ylabel("$N_{\\rm polygon}$")

    _plt.subplot(2,2,2)
    _plt.semilogy(data1[:,0],data1[:,2],"-")
    _plt.semilogy(data2[:,0],data2[:,2],"-")
    _plt.xlabel("$N_{\\rm subtraction}$")
    _plt.ylabel("$\\Delta t/s $")

    _plt.subplot(2,2,3)
    _plt.semilogy(data1[:,1],data2[:,1],"-")
    _plt.semilogy(data2[:,1],data2[:,2],"-")
    _plt.xlabel("$N_{\\rm poly}$")
    _plt.ylabel("$\\Delta t/s $")

    fig.tight_layout()