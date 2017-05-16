from pygeometry.geant4.Registry import registry as _registry

class LogicalVolume :
    def __init__(self, solid, material, name) :
        self.solid           = solid
        self.material        = material
        self.name            = name
        self.daughterVolumes = [] 
        self.mesh            = None
        _registry.addLogicalVolume(self)

    def __repr__(self) : 
        return 'Logical volume : '+self.name+' '+str(self.solid)+' '+str(self.material)
    
    def pycsgmesh(self) :
        if self.mesh : 
            return self.mesh 

        if len(self.daughterVolumes) == 0 :
            self.mesh = [self.solid.pycsgmesh()]
            self.mesh[0].alpha     = 0.5
            self.mesh[0].wireframe = False
            self.mesh[0].colour    = [1,1,1]

        else :
            daughterMeshes = []
            for dv in self.daughterVolumes :
                dvMesh = dv.pycsgmesh() 
                daughterMeshes.append(dvMesh)
                self.mesh = [self.solid.pycsgmesh(),daughterMeshes]

            self.mesh[0].alpha     = 0.5
            self.mesh[0].wireframe = False
            self.mesh[0].colour    = [1,0,0]
            self.mesh[0].logical   = True
            
        return self.mesh

    def add(self, physicalVolume) :
        self.daughterVolumes.append(physicalVolume)

    def gdmlWrite(self, gw, prepend) :
        we = gw.doc.createElement('volume')
        we.setAttribute('name',prepend+'_'+self.name+'_lv')
        mr = gw.doc.createElement('materialref')
        if self.material.find("G4") != -1 :          
            mr.setAttribute('ref',self.material)
        else :
            mr.setAttribute('ref',prepend+'_'+self.material)
        we.appendChild(mr)

        sr = gw.doc.createElement('solidref')
        sr.setAttribute('ref',prepend+'_'+self.solid.name)
        we.appendChild(sr)
        
        for dv in self.daughterVolumes : 
            dve = dv.gdmlWrite(gw,prepend)
            we.appendChild(dve)

        gw.structure.appendChild(we)
