from collections import OrderedDict 

class Registry :
    def __init__(self) : 
        self.defineDict              = OrderedDict()
        self.materialDict            = OrderedDict()
        self.solidDict               = OrderedDict()
        self.logicalVolumeDict       = OrderedDict()
        self.physicalVolumeDict      = OrderedDict()
        self.replicaVolumeDict       = OrderedDict()
        self.parameterisedVolumeDict = OrderedDict()
        self.parameterDict           = OrderedDict()
        self.logicalVolumeList       = []
        self.solidCountDict          = {}
        self.volumeCountDict         = {}
        self.logicalVolumeMeshSkip   = []

    def addDefinition(self, definition) :    
        self.definitionDict[definition.name] = definition

    def addMaterial(self, material) :
        self.materialDict[material.name] = material

    def addSolid(self,solid) :
        self.solidDict[solid.name] = solid

        try:
            self.solidCountDict[solid.type] = self.solidCountDict[solid.type] +1
        except KeyError:
            self.solidCountDict[solid.type] = 1

    def addLogicalVolume(self,volume) :
        self.logicalVolumeDict[volume.name] = volume       

        try:
            self.volumeCountDict["logicalVolume"] = self.volumeCountDict["logicalVolume"] +1
        except KeyError:
            self.volumeCountDict["logicalVolume"] = 1
            
    def addPhysicalVolume(self,volume) : 
        self.physicalVolumeDict[volume.name] = volume
        
        try:
            self.volumeCountDict["physicalVolume"] = self.volumeCountDict["physicalVolume"] +1
        except KeyError:
            self.volumeCountDict["physicalVolume"] = 1
            
    def addReplicaVolume(self,volume) :
        self.replicaVolumeDict[volume.name] = volume
        
        try:
            self.volumeCountDict["replicaVolume"] = self.volumeCountDict["replicaVolume"] +1
        except KeyError:
            self.volumeCountDict["replicaVolume"] = 1

    def addParameterisedVolume(self,volume) :
        self.parametrisedVolumeDict[volume.name] = volume

    def addParameter(self, parameter):
        self.parameterDict[parameter.name] = parameter

    def setWorld(self, worldName) :
        self.worldName = worldName
        self.worldVolume = self.logicalVolumeDict[self.worldName]
        self.orderLogicalVolumes(worldName)
        self.logicalVolumeList.append(worldName)
        
    def orderLogicalVolumes(self, lvName) :

        lv = self.logicalVolumeDict[lvName]
        
        for daughters in lv.daughterVolumes : 
            dlvName = daughters.logicalVolume.name
            try : 
                self.logicalVolumeList.index(dlvName)
            except ValueError: 
                self.orderLogicalVolumes(dlvName)
                self.logicalVolumeList.append(dlvName)
                    
    def clear(self) :
        self.defineDict.clear()
        self.materialDict.clear()
        self.solidDict.clear()
        self.solidCountDict.clear()
        self.volumeCountDict.clear()
        self.logicalVolumeDict.clear()
        self.physicalVolumeDict.clear()
        self.replicaVolumeDict.clear()
        self.parameterisedVolumeDict.clear()
        self.parameterDict.clear()

registry = Registry()

