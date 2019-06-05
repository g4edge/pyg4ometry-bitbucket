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

    kXAxis = 1
    kYAxis = 2
    kZAxis = 3
    kRho   = 4
    kPhi   = 5

    def __init__(self, name, logicalVolume, motherVolume, axis, nreplicas, 
                 width, offset = 0, registry = None, addRegistry=True) : 
        # super(ReplicaVolume, self).__init__([0,0,0],[0,0,0],logicalVolume,name,motherVolume, registry, addRegistry)

        self.logicalVolume       = logicalVolume
        self.motherVolume        = motherVolume
        self.motherVolume.add(self)
        self.axis                = axis
        self.nreplicas           = nreplicas
        self.width               = width
        self.offset              = offset
        
        if addRegistry : 
            registry.addPhysicalVolume(self)
        
        # Only the replica transforms are required
        self.replicaTransforms = self.createReplicaTransforms()

    def createReplicaTransforms(self) : 

        transforms = []
        for v in _np.arange(self.offset, self.offset+self.nreplicas*self.width,self.width) : 
            print v 

    def checkOverlap(self) :
        pass

    def __repr__(self) :
        return ""
