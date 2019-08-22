import pyg4ometry.exceptions
from   pyg4ometry.pycsg.geom import Vector as _Vector
from   pyg4ometry.pycsg.core import CSG    as _CSG
#from   pyg4ometry.gdml.Defines import Auxiliary as _Auxiliary

from   pyg4ometry.visualisation  import Mesh            as _Mesh
from   pyg4ometry.visualisation  import OverlapType     as _OverlapType
import solid                     as                 _solid
import Material                  as                 _mat
import pyg4ometry.transformation as                 _trans

import numpy   as   _np
import logging as   _log


class LogicalVolume(object):
    '''
    LogicalVolume : G4LogicalVolume
    :param solid:  
    :param material:
    :param name: 
    :param registry:      
    :param addRegistry: 
    '''

    def __init__(self, solid, material, name, registry=None, addRegistry=True, **kwargs):
        super(LogicalVolume, self).__init__()

        # type 
        self.type            = "logical"
        
        # geant4 required objects 
        self.solid           = solid
 
        if isinstance(material, _mat.Material):
            self.material = material
        elif isinstance(material, str):
            # This will work out if it is a valid NIST and set the type appropriately
            self.material = _mat.MaterialPredefined(name=material)
        else:
            raise ValueError("Unsupported type for material: {}".format(type(material)))

        self.name            = name
        self.daughterVolumes = []

        # geometry mesh
        self.mesh            = _Mesh(self.solid)

        self.auxiliary = []
        self.addAuxiliaryInfo(kwargs.get("auxiliary", None))

        # registry logic
        if registry and addRegistry:
            registry.addLogicalVolume(self)
        self.registry = registry

    def __repr__(self):
        return 'Logical volume : '+self.name+' '+str(self.solid)+' '+str(self.material)

    def add(self, physicalVolume):
        self.daughterVolumes.append(physicalVolume)

    def checkOverlaps(self, recursive = False) :
        # local meshes 
        transformedMeshes = []

        # transform meshes into logical volume frame 
        for pv in self.daughterVolumes :
            _log.info('LogicalVolume.checkOverlaps> %s' % (pv.name))
            mesh = pv.logicalVolume.mesh.localmesh.clone()

            # rotate 
            aa = _trans.tbxyz2axisangle(pv.rotation.eval())
            mesh.rotate(aa[0],_trans.rad2deg(aa[1]))

            # scale
            if pv.scale :
                mesh.scale(pv.scale.eval())

            # translate 
            mesh.translate(pv.position.eval())
            
            transformedMeshes.append(mesh)

        # overlap daughter pv checks 
        for i in range(0,len(transformedMeshes)) : 
            for j in range(i+1,len(transformedMeshes)) :
                interMesh = transformedMeshes[i].intersect(transformedMeshes[j])
                _log.info('LogicalVolume.checkOverlaps> inter daughter %d %d %d %d' % (i,j, interMesh.vertexCount(), interMesh.polygonCount()))
                if interMesh.vertexCount() != 0  :
                    self.mesh.addOverlapMesh([interMesh,_OverlapType.overlap])

        # coplanar daughter pv checks
        print 'coplanar with pvs'
        for i in range(0,len(transformedMeshes)) :
            for j in range(i+1,len(transformedMeshes)) :
                coplanarMesh = transformedMeshes[i].coplanar(transformedMeshes[j])
                if coplanarMesh.vertexCount() != 0:
                    self.mesh.addOverlapMesh([coplanarMesh, _OverlapType.coplanar])

        # overlap with solid
        for i in range(0,len(transformedMeshes)) : 
            interMesh = transformedMeshes[i].intersect(self.mesh.localmesh.inverse())
            _log.info('LogicalVolume.checkOverlaps> daughter container %d %d %d' % (i, interMesh.vertexCount(), interMesh.polygonCount()))

            if interMesh.vertexCount() != 0 :
                self.mesh.addOverlapMesh([interMesh,_OverlapType.protrusion])

        # coplanar with solid
        print 'coplanar with solid'
        for i in range(0,len(transformedMeshes)) :
            # coplanarMesh = transformedMeshes[i].coplanar(self.mesh.localmesh)
            coplanarMesh = self.mesh.localmesh.coplanar(transformedMeshes[i])
            if coplanarMesh.vertexCount() != 0 :
                self.mesh.addOverlapMesh([coplanarMesh, _OverlapType.coplanar])

    def setSolid(self, solid) : 
        self.solid = solid 
        self.mesh  = _Mesh(self.solid)        


    def addAuxiliaryInfo(self, auxiliary):
        #if auxiliary is not None and not isinstance(auxiliary, _Auxiliary):
        #    raise ValueError("Auxiliary infromation must be a gdml.Defines.Auxiliary instance.")
        if isinstance(auxiliary, list) or isinstance(auxiliary, tuple):
            for aux in auxiliary:
                self.addAuxiliaryInfo(aux)
        else:
            if auxiliary:
                self.auxiliary.append(auxiliary)

    def extent(self,includeBoundingSolid = False) :
        _log.info('LogicalVolume.extent> %s ' % (self.name))

        if includeBoundingSolid :
            [vMin, vMax] = self.mesh.getBoundingBox()
            return [vMin, vMax]
        else :
            vMin = [1e99,1e99,1e99]
            vMax = [-1e99,-1e99,-1e99]

        # transform logical solid BB
                
        for dv in self.daughterVolumes :
            [vMinDaughter, vMaxDaughter] = dv.extent(True)

            if vMaxDaughter[0] > vMax[0] :
                vMax[0] = vMaxDaughter[0]
            if vMaxDaughter[1] > vMax[1] :
                vMax[1] = vMaxDaughter[1]
            if vMaxDaughter[2] > vMax[2] :
                vMax[2] = vMaxDaughter[2]

            if vMinDaughter[0] < vMin[0] :
                vMin[0] = vMinDaughter[0]
            if vMinDaughter[1] < vMin[1] :
                vMin[1] = vMinDaughter[1]
            if vMinDaughter[2] < vMin[2] :
                vMin[2] = vMinDaughter[2]

        return [vMin, vMax]

    def findLogicalByName(self,name) : 
        lv = [] 

        if self.name.find(name) != -1 : 
            lv.append(self)

        
        for d in self.daughterVolumes : 
            l = d.logicalVolume.findLogicalByName(name)
            if len(l) != 0 :
                lv.append(l)
        
        return lv
