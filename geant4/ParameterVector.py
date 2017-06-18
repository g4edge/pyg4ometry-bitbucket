from pygeometry.geant4.Registry import registry as _registry
from pygeometry.geant4.Parameter import Parameter as _Parameter

class ParameterVector(list) :
    def __init__(self, name, vlist = [], addRegistry = True) :
        self.name  = name

        for elem in vlist :
            self.append(elem)

        if addRegistry :
            _registry.addParameter(self)

    def __repr__(self) :
        return self.name

    def str(self) :
        return 'param:'+self.name+':'+str(self.value)

    def __add__(self,other) :
        return ParameterVector(str(self)+"+"+str(other),[self[0]+other[0],
                                                         self[1]+other[1],
                                                         self[2]+other[2]], True)

    def __sub__(self, other):
        return ParameterVector(str(self) + "-" + str(other),[self[0]-other[0],
                                                             self[1]-other[1],
                                                             self[2]-other[2]], True)