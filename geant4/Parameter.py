from pygeometry.geant4.Registry import registry as _registry

class Parameter :
    def __init__(self, name, value) : 
        self.name  = name 
        self.value = value
        _registry.addParameter(self)

    def __repr__(self) : 
        return self.name

    def str(self) :
        return 'param:'+self.name+':'+str(self.value)

    def __float__(self) :
        return float(self.value)

    def __getitem__(self, i) : 
        return self.value[i]
