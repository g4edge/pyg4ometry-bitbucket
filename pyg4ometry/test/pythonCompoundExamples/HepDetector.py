import pyg4ometry
import numpy as _np

def HepDetector() :
    pass

def SiTrackerBarrelRing(radius = 0.25, sensorSize= 0.08, nAzimuth = 25, tiltAngleDeg = 11, reg = None) :

    if reg is None :
        reg = pyg4ometry.geant4.Registry()

    tiltAngleRad = pyg4ometry.transformation.deg2rad(tiltAngleDeg)

    sitbmLv = SiTrackerBarrelModule(sensorSize = sensorSize)

    barrelAv = pyg4ometry.geant4.AssemblyVolume("barrelAv",reg,True)

    for i in range(0,nAzimuth,1) :
        phi = 2*_np.pi/nAzimuth*i
        modulePv = pyg4ometry.geant4.PhysicalVolume([0, phi+_np.pi/2+tiltAngleRad, 0],
                                                    [radius*_np.cos(phi), 0, radius*_np.sin(phi),"m"],
                                                    sitbmLv,
                                                    "modulePv"+str(i),
                                                    barrelAv, reg)


    return barrelAv

def SiTrackerBarrelModule(sensorSize = 0.08, sensorGap = 3e-3,pcbLength = 0.015, pcbGap = 0.005, tiltAngleDeg = 5, reg = None) :

    if reg is None :
        reg = pyg4ometry.geant4.Registry()

    tiltAngleRad = pyg4ometry.transformation.deg2rad(tiltAngleDeg)

    moduleAv = pyg4ometry.geant4.AssemblyVolume("moduleAv",reg,True)

    sensorLv = SiTrackerBarrelSensor(sensorSize = sensorSize,
                                     sensorThickness = 300e-6,
                                     nstrip = 512,
                                     reg = reg)
    sensorPv1 = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,-sensorSize/2, sensorGap/2, "m"], sensorLv,"sensorPv1",moduleAv,reg)
    sensorPv2 = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0, sensorSize/2, sensorGap/2, "m"], sensorLv,"sensorPv1",moduleAv,reg)
    sensorPv3 = pyg4ometry.geant4.PhysicalVolume([0,0,tiltAngleRad],[-sensorSize/2*_np.sin(tiltAngleRad),-sensorSize/2*_np.cos(tiltAngleRad),-sensorGap/2, "m"], sensorLv,"sensorPv1",moduleAv,reg)
    sensorPv4 = pyg4ometry.geant4.PhysicalVolume([0,0,tiltAngleRad],[ sensorSize/2*_np.sin(tiltAngleRad), sensorSize/2*_np.cos(tiltAngleRad),-sensorGap/2, "m"], sensorLv,"sensorPv1",moduleAv,reg)

    pcbSolid  = pyg4ometry.geant4.solid.Box("pcbSolid",sensorSize, pcbLength, 2e-3, reg, "m")
    pcbLv     = pyg4ometry.geant4.LogicalVolume(pcbSolid,"G4_Si","pcbLV",reg,True)
    pcbPv     = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,-pcbLength/2, pcbGap, "m"], pcbLv,"sensorPv1",moduleAv,reg)

    return moduleAv

def SiTrackerBarrelSensor(sensorSize = 0.05, sensorThickness = 300e-6, nstrip = 512, reg = None) :
    if reg is None :
        reg = pyg4ometry.geant4.Registry()

    sensor = pyg4ometry.geant4.solid.Box("sensorSolid",sensorSize, sensorSize, sensorThickness,reg, "m", True)
    sensorLv = pyg4ometry.geant4.LogicalVolume(sensor,"G4_Si","sensorLV",reg,True)

    return sensorLv

def SiTrackerEndLayer(innerRadius = 0.3, outerRadius = 0.56, nPetal = 20, phiPetal = 0.6) :
    pass

def SiTrackerEndModule() :

    pass

def SiTrackerEndSensor(innerRadius = 0.3, outerRadius = 0.56) :
    pass

def FibreTracker() :
    pass

def Solenoid() :
    pass

def CalorimeterBarrel() :
    pass

def CalorimeterCap(innerRadius = 2, outerRadius = 2.5) :
    pass