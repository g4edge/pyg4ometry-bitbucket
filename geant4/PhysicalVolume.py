from pygeometry.geant4.Registry import registry as _registry
import copy as _copy
from pygeometry.transformation import *
import sys as _sys

class PhysicalVolume :

    imeshed = 0

    def __init__(self, rotation, position, logicalVolume, name, motherVolume, scale = [1,1,1]) :
        self.rotation      = rotation
        self.position      = position
        self.logicalVolume = logicalVolume
        self.name          = name 
        self.motherVolume  = motherVolume
        self.mesh          = None
        self.motherVolume.add(self)
        self.scale         = scale
        _registry.addPhysicalVolume(self)

    def __repr__(self) : 
        return 'Physical Volume : '+self.name+' '+str(self.rotation)+' '+str(self.position)
        
    def pycsgmesh(self) :

        PhysicalVolume.imeshed = PhysicalVolume.imeshed + 1
        print 'PhysicalVolume mesh count',PhysicalVolume.imeshed

        # see if the volume should be skipped
        try :
            _registry.logicalVolumeMeshSkip.index(self.logicalVolume.name)
            print "Physical volume skipping ---------------------------------------- ",self.name
            return []
        except ValueError :
            self.mesh = _copy.deepcopy(self.logicalVolume.pycsgmesh())

        if self.mesh :
            return self.mesh

        # loop over daughter meshes
        map_nlist(self.mesh,list(self.position),tbxyz(list(self.rotation)),list(self.scale))

        print 'physical mesh', self.name
        return self.mesh

    def gdmlWrite(self, gw, prepend) : 
        # physical volume
        pv = gw.doc.createElement('physvol')
        pv.setAttribute('name',prepend+'_'+self.name+'_pv')
        vr = gw.doc.createElement('volumeref')
        vr.setAttribute('ref',prepend+'_'+self.logicalVolume.name+'_lv')
        pv.appendChild(vr)

        # phys vol translation
        tlatee = gw.doc.createElement('position')
        tlatee.setAttribute('name',prepend+'_'+self.name+'_pos')
        tlatee.setAttribute('x',str(self.position[0]))
        tlatee.setAttribute('y',str(self.position[1]))
        tlatee.setAttribute('z',str(self.position[2]))
        pv.appendChild(tlatee)

        # phys vol rotation
        rote   = gw.doc.createElement('rotation')
        rote.setAttribute('name',prepend+'_'+self.name+'_rot')
        rote.setAttribute('x',str(self.rotation[0]))
        rote.setAttribute('y',str(self.rotation[1]))
        rote.setAttribute('z',str(self.rotation[2]))
        pv.appendChild(rote)

        # phys vol scale
        tscae = gw.doc.createElement('scale')
        tscae.setAttribute('name',prepend+'_'+self.name+'_sca')
        tscae.setAttribute('x',str(self.scale[0]))
        tscae.setAttribute('y',str(self.scale[1]))
        tscae.setAttribute('z',str(self.scale[2]))
        pv.appendChild(tscae)    

        return pv
                           
def map_nlist(nlist,trans,rot,scale = [1,1,1]):
    '''Function to apply transformation (rot then trans) to nested list of meshes (nlist)'''
    for i in range(len(nlist)) :
        if isinstance(nlist[i],list) :
            map_nlist(nlist[i],trans,rot,scale)
        else :
            nlist[i].scale(scale)
            nlist[i].rotate(rot[0],rad2deg(rot[1]))
            nlist[i].translate(trans)
