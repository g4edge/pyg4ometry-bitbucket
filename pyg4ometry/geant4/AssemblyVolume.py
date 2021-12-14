import pyg4ometry.transformation as _trans
from   pyg4ometry.visualisation import OverlapType as _OverlapType

import logging as   _log

class AssemblyVolume(object) : 
    '''AssemblyVolume : similar to a logical volume but does not have a sense of 
    shape, material or field
    :param name: of assembly volume
    :type name:        
    :param registry: 
    :type registry: 
    :param addRegistry: 
    :type addRegistry: bool
    '''

    def __init__(self, name, registry=None, addRegistry=True) :
        super(AssemblyVolume, self).__init__()
        self.type            = "assembly"
        self.name            = name 
        self.daughterVolumes = []
        self.registry = registry
        if addRegistry :
            registry.addLogicalVolume(self)

        self.overlapChecked = False
            
    def __repr__(self):
        return 'Logical volume : '+self.name

    def add(self, physicalVolume) :
        self.daughterVolumes.append(physicalVolume)

    def findLogicalByName(self, name):
        lv = []

        if self.name.find(name) != -1:
            lv.append(self)

        for d in self.daughterVolumes:
            l = d.logicalVolume.findLogicalByName(name)
            if len(l) != 0:
                lv.append(l)

        return lv

    def _getDaughterMeshes(self):
        """
        Get daughter meshes for overlap checking.
        return [daughterMesh,..],[daughterBoundingMesh,..][daughterName,...]
        """
        transformedMeshes = []
        transformedBoundingMeshes = []
        transformedMeshesNames = []
        for pv in self.daughterVolumes:
            # daughter could be one LV or could in turn be another assembly - either use a list
            m,bm,nm = [],[],[]
            dlv = pv.logicalVolume
            if type(dlv) is AssemblyVolume:
                m,bm,nm = dlv._getDaughterMeshes()
                nm = [self.name + "_" + pv.name + "_" + n for n in nm]
            else:
                # assume type is LogicalVolume
                m  = [dlv.mesh.localmesh.clone()]
                bm = [dlv.mesh.localboundingmesh.clone()]
                nm = [self.name + "_" + pv.name]

            aa = _trans.tbxyz2axisangle(pv.rotation.eval())
            s = None
            if pv.scale:
                s = pv.scale.eval()
            t = pv.position.eval()
            for mesh, boundingmesh, name in zip(m, bm, nm):
                # rotate
                mesh.rotate(aa[0], _trans.rad2deg(aa[1]))
                boundingmesh.rotate(aa[0], _trans.rad2deg(aa[1]))

                # scale
                if s:
                    mesh.scale(s)
                    boundingmesh.scale(s)

                    if s[0] * s[1] * s[2] == 1:
                        pass
                    elif s[0] * s[1] * s[2] == -1:
                        mesh = mesh.inverse()
                        boundingmesh.inverse()

                # translate
                mesh.translate(t)
                boundingmesh.translate(t)

                transformedMeshes.append(mesh)
                transformedBoundingMeshes.append(boundingmesh)
                transformedMeshesNames.append(name)

        return transformedMeshes, transformedBoundingMeshes, transformedMeshesNames

    def extent(self, includeBoundingSolid=True) :
        _log.info('AssemblyVolume.extent> %s ' % (self.name))

        vMin = [1e99,1e99,1e99]
        vMax = [-1e99,-1e99,-1e99]

        for dv in self.daughterVolumes:
            [vMinDaughter, vMaxDaughter] = dv.extent()

            if vMaxDaughter[0] > vMax[0]:
                vMax[0] = vMaxDaughter[0]
            if vMaxDaughter[1] > vMax[1]:
                vMax[1] = vMaxDaughter[1]
            if vMaxDaughter[2] > vMax[2]:
                vMax[2] = vMaxDaughter[2]

            if vMinDaughter[0] < vMin[0]:
                vMin[0] = vMinDaughter[0]
            if vMinDaughter[1] < vMin[1]:
                vMin[1] = vMinDaughter[1]
            if vMinDaughter[2] < vMin[2]:
                vMin[2] = vMinDaughter[2]

        return [vMin, vMax]