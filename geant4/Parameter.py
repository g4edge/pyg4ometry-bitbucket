from pygeometry.geant4.Registry import registry as _registry

class Parameter(object) :
    def __init__(self, name, value, addRegistry = True) :
        self.name  = name
        self.value = value

        if addRegistry :
            _registry.addParameter(self)

    def __repr__(self) : 
        return self.name

    def str(self) :
        return 'param:'+self.name+':'+str(self.value)

    def __float__(self) :
        return float(self.value)

    def __getitem__(self, i) : 
        return self.value[i]

    def __add__(self, other) :
        return Parameter(str(self)+'+'+str(other),float(self)+float(other),False)

    def __sub__(self, other) :
        return Parameter(str(self)+'-'+str(other),float(self)-float(other),False)

    def __mul__(self, other):
        return Parameter(str(self) + '*' + str(other), float(self) * float(other),False)

    def __rmul__(self, other):
        return Parameter(str(other) + '*' + str(self), float(other) * float(self),False)

    def __div__(self, other):
        return Parameter(str(self) + '/' + str(other), float(self) / float(other),False)
