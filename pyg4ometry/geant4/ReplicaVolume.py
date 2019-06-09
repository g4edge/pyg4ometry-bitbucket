import PhysicalVolume as _PhysicalVolume
import numpy as _np

class ReplicaVolume(_PhysicalVolume.PhysicalVolume) : 
    '''
    ReplicaVolume: G4PVReplica

    :param name: of physical volume 
    :param logical: volume to be placed
    :param mother: logical volume, 
    :param axis: kXAxis,kYAxis,kZAxis,kRho,kPhi
    :param ncopies: number of replicas
    :param width: spacing between replicas along axis
    :param offset: of grid
    '''

    class Axis :
        kXAxis = 1
        kYAxis = 2
        kZAxis = 3
        kRho   = 4
        kPhi   = 5

    def __init__(self, name, logicalVolume, motherVolume, axis, nreplicas, 
                 width, offset = 0, registry = None, addRegistry=True, wunit = "", ounit= "") : 

        self.type                = "replica"        
        self.name                = name
        self.logicalVolume       = logicalVolume
        self.motherVolume        = motherVolume
        self.motherVolume.add(self)
        self.axis                = axis

        self.nreplicas           = nreplicas
        self.width               = width
        self.offset              = offset
        self.wunit               = wunit
        self.ounit               = ounit

        if addRegistry : 
            registry.addPhysicalVolume(self)
        
        # Create replica meshes
        self.meshes = self.createReplicaMeshes()

    def createReplicaMeshes(self) : 
        
        nreplicas = int(self.nreplicas.eval())
        offset    = self.offset.eval()
        width     = self.width.eval()
        
        transforms = []
        for v in _np.arange(offset, offset+nreplicas*width,width) :
            pass

        return None

    def __repr__(self) :
        return 'Replica volume : '+self.name+' '+str(self.axis)+' '+str(self.nreplicas)+' '+str(self.offset)+' '+str(self.width)
