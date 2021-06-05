import pyg4ometry
import numpy as _np

def HepDetector() :
    pass


def SiBarrelTracker() :
    reg = pyg4ometry.geant4.Registry()

    worldBox      = pyg4ometry.geant4.solid.Box("worldBox",10000,10000,10000,reg,"mm")
    worldLv       = pyg4ometry.geant4.LogicalVolume(worldBox,"G4_Galactic","worldLv",reg)

    siTrackerTubs = pyg4ometry.geant4.solid.Tubs("siTrackerTubs",100,500,1650,0,2*_np.pi,reg,"mm","rad")
    siTrackerLv   = pyg4ometry.geant4.LogicalVolume(siTrackerTubs,"G4_Galactic","siTrackerLv",reg)
    siTrackerPv   = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,0],siTrackerLv,"siTrackerPv",worldLv,reg)

    siTrackerModuleAv = SiTrackerBarrelModule(reg=reg)

    siTrackerLayer1Av = SiTrackerBarrelLayer(name = "barrelAv1", moduleAv=siTrackerModuleAv, radius = 0.15, nAzimuth = 15, reg = reg)
    siTrackerLayer1Pv = pyg4ometry.geant4.PhysicalVolume([_np.pi/2.0,0,0],[0,0,0],siTrackerLayer1Av,"siTrackerLayer1Pv",siTrackerLv, reg)

    siTrackerLayer2Av = SiTrackerBarrelLayer(name = "barrelAv2", moduleAv=siTrackerModuleAv, radius = 0.30, nAzimuth = int(0.3/0.15*15), reg = reg)
    siTrackerLayer2Pv = pyg4ometry.geant4.PhysicalVolume([_np.pi/2.0,0,0],[0,0,0],siTrackerLayer2Av,"siTrackerLayer2Pv",siTrackerLv, reg)

    siTrackerLayer3Av = SiTrackerBarrelLayer(name = "barrelAv3", moduleAv=siTrackerModuleAv, radius = 0.45, nAzimuth = int(0.45/0.15*15), reg = reg)
    siTrackerLayer3Pv = pyg4ometry.geant4.PhysicalVolume([_np.pi/2.0,0,0],[0,0,0],siTrackerLayer3Av,"siTrackerLayer3Pv",siTrackerLv, reg)

    v = pyg4ometry.visualisation.VtkViewer()
    v.addLogicalVolume(worldLv)
    v.view()

    # gdml output
    reg.setWorld("worldLv")
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg)
    w.write("SiTracker.gdml")

def SiTrackerBarrelLayer(name = "barrelAv", moduleAv = None,
                         length = 1.6, radius = 0.25, sensorSize= 0.08, nAzimuth = 25, tiltAngleDeg = 11,
                         reg = None) :

    if reg is None :
        reg = pyg4ometry.geant4.Registry()

    tiltAngleRad = pyg4ometry.transformation.deg2rad(tiltAngleDeg)

    sitbmLv = moduleAv

    barrelAv = pyg4ometry.geant4.AssemblyVolume(name,reg,True)

    nLength = int(length/(2*sensorSize))

    for i in range(0,nLength, 1) :
        z = i*2*sensorSize- length/2.0 + sensorSize

        for j in range(0,nAzimuth,1) :
            phi = 2*_np.pi/nAzimuth*j
            modulePv = pyg4ometry.geant4.PhysicalVolume([0, phi+_np.pi/2+tiltAngleRad, 0],
                                                        [radius*_np.cos(phi), z, radius*_np.sin(phi),"m"],
                                                         sitbmLv,
                                                        name+"_modulePv"+str(i)+"_"+str(j),
                                                        barrelAv, reg)

    return barrelAv

def SiTrackerBarrelModule(sensorSize = 0.08, sensorGap = 3e-3,pcbLength = 0.015, pcbGap = 0.005, tiltAngleDeg = 5, reg = None) :

    if reg is None :
        reg = pyg4ometry.geant4.Registry()

    tiltAngleRad = pyg4ometry.transformation.deg2rad(tiltAngleDeg)

    moduleAv = pyg4ometry.geant4.AssemblyVolume("barrelModuleAv",reg,True)

    sensorLv = SiTrackerBarrelSensor(sensorSize = sensorSize,
                                     sensorThickness = 300e-6,
                                     nstrip = 512,
                                     reg = reg)
    sensorPv1 = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,-sensorSize/2, sensorGap/2, "m"], sensorLv,"sensorBarrelPv1",moduleAv,reg)
    sensorPv2 = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0, sensorSize/2, sensorGap/2, "m"], sensorLv,"sensorBarrelPv1",moduleAv,reg)
    sensorPv3 = pyg4ometry.geant4.PhysicalVolume([0,0,tiltAngleRad],[-sensorSize/2*_np.sin(tiltAngleRad),-sensorSize/2*_np.cos(tiltAngleRad),-sensorGap/2, "m"], sensorLv,"sensorPv1",moduleAv,reg)
    sensorPv4 = pyg4ometry.geant4.PhysicalVolume([0,0,tiltAngleRad],[ sensorSize/2*_np.sin(tiltAngleRad), sensorSize/2*_np.cos(tiltAngleRad),-sensorGap/2, "m"], sensorLv,"sensorPv1",moduleAv,reg)

    pcbSolid  = pyg4ometry.geant4.solid.Box("pcbSolid",sensorSize, pcbLength, 2e-3, reg, "m")
    pcbLv     = pyg4ometry.geant4.LogicalVolume(pcbSolid,"G4_Si","pcbLV",reg,True)
    pcbPv     = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,-pcbLength/2, pcbGap, "m"], pcbLv,"sensorPv1",moduleAv,reg)

    return moduleAv

def SiTrackerBarrelSensor(sensorSize = 0.05, sensorThickness = 300e-6, nstrip = 512, reg = None) :
    if reg is None :
        reg = pyg4ometry.geant4.Registry()

    sensor   = pyg4ometry.geant4.solid.Box("sensorBarrrelSolid",sensorSize, sensorSize, sensorThickness,reg, "m", True)
    sensorLv = pyg4ometry.geant4.LogicalVolume(sensor,"G4_Si","sensorBarrelLV",reg,True)

    return sensorLv

def SiTrackerEndcapLayer(innerRadius = 0.3, outerRadius = 0.56, nPetal = 20, phiPetal = 0.6) :
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