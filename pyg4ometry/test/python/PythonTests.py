import unittest as _unittest

import logging as _log

logger = _log.getLogger()
logger.disabled = True

class PythonTests(_unittest.TestCase) :
    def testFreeCadImportFail(self) :         
        import sys
        # remove freecad 
        for p in sys.path :
            if p.find("freecad") != -1 :
                sys.path.remove(p)
    
        import pyg4ometry.freecad

    def testExceptionNullMeshErrorIntersection(self) : 
        import pyg4ometry

        try :
            reg = pyg4ometry.geant4.Registry()
            s1   = pyg4ometry.geant4.solid.Box("s1",10,10,10, reg, "mm")
            s2   = pyg4ometry.geant4.solid.Box("s2",10,10,10, reg, "mm")

            inter = pyg4ometry.geant4.solid.Intersection("inter",s1,s2,[[0,0,0],[0,0,0]],reg)
            raise pyg4ometry.exceptions.NullMeshError(inter)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def testExceptionNullMeshErrorSubtraction(self) : 
        import pyg4ometry

        try :
            reg = pyg4ometry.geant4.Registry()
            s1   = pyg4ometry.geant4.solid.Box("s1",10,10,10, reg, "mm")
            s2   = pyg4ometry.geant4.solid.Box("s2",10,10,10, reg, "mm")

            subtra = pyg4ometry.geant4.solid.Subtraction("subtra",s1,s2,[[0,0,0],[0,0,0]],reg)
            raise pyg4ometry.exceptions.NullMeshError(subtra)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def testExceptionNullMeshErrorOtherSolid(self) : 
        import pyg4ometry

        try :
            reg = pyg4ometry.geant4.Registry()
            s1   = pyg4ometry.geant4.solid.Box("s1",10,10,10, reg, "mm")
            raise pyg4ometry.exceptions.NullMeshError(s1)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def testExceptionNullMeshErrorBasestring(self) : 
        import pyg4ometry

        try :
            raise pyg4ometry.exceptions.NullMeshError("s1")
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def testExceptionIdenticalNameError(self) :
        import pyg4ometry 


        try : 
            raise pyg4ometry.exceptions.IdenticalNameError("solid_name")
        except pyg4ometry.exceptions.IdenticalNameError :
            pass

        try : 
            raise pyg4ometry.exceptions.IdenticalNameError("solid_name","solid")
        except pyg4ometry.exceptions.IdenticalNameError :
            pass



if __name__ == '__main__':
    _unittest.main(verbosity=2)        
