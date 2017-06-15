import pyfluka

sph1 = pyfluka.bodies.SPH("sph1", [0.0, 0.0, 0.0, 5.0])
sph2 = pyfluka.bodies.SPH("sph2", [2.5, 0.0, 0.0, 5.0])
sph3 = pyfluka.bodies.SPH("sph3", [5.0, 0.0, 0.0, 5.0])

zone1 = pyfluka.bodies.Zone(('+', sph1))
zone2 = pyfluka.bodies.Zone(('+', sph2))
zone3 = pyfluka.bodies.Zone(('+', sph3))

region = pyfluka.bodies.Region("union", [zone1, zone2, zone3])

region.view()
