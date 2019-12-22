import unittest as _unittest
import numpy as _np
import pyg4ometry.transformation as _trans
        

import logging as _log

# logger = _log.getLogger()
# logger.disabled = True

class PythonTests(_unittest.TestCase) :

    # #############################
    # Transformation
    # #############################
    def test_Python_Rad2Deg(self) :
        self.assertEqual(_trans.rad2deg(_np.pi),180)

    def test_Python_Deg2Rad(self) :
        self.assertEqual(_trans.deg2rad(180),_np.pi)

    def test_Python_Tbxyz2axisangle(self) :
        self.assertEqual(_trans.tbxyz2axisangle([0.0,_np.pi/2.0,0.0]),
                         [[0.0, 1.0, 0.0], 1.5707963267948966])

    def test_Python_Matrix2axisangle(self) :
        theta = 0.5
        m = _np.array([[_np.cos(theta), -_np.sin(theta),0],[_np.sin(theta),_np.cos(theta),0],[0,0,1]])
        self.assertEqual(_trans.matrix2axisangle(m),
                         [[0.0, 0.0, 1.0000000000000002], 0.4999999999999999])

    def test_Python_Axisangle2matrix(self) :
        pass
    
    def test_Python_Matrix2tbxyz(self) :
        pass

    def test_Python_Tbxyz2matrix(self) :
        pass

    def test_Python_Matrix_from(self) :
        pass 

    # #############################
    # Freecad
    # #############################
    def test_Python_FreeCadImportFail(self) :
        import sys
        # remove freecad 
        for p in sys.path :
            if p.find("freecad") != -1 :
                sys.path.remove(p)
    
        import pyg4ometry.freecad

    # #############################
    # Mesh
    # #############################
    
    
    # #############################
    # CSG
    # #############################

    def test_Python_ExceptionNullMeshErrorIntersection(self) :
        import pyg4ometry

        try :
            reg = pyg4ometry.geant4.Registry()
            s1   = pyg4ometry.geant4.solid.Box("s1",10,10,10, reg, "mm")
            s2   = pyg4ometry.geant4.solid.Box("s2",10,10,10, reg, "mm")

            inter = pyg4ometry.geant4.solid.Intersection("inter",s1,s2,[[0,0,0],[0,0,0]],reg)
            raise pyg4ometry.exceptions.NullMeshError(inter)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def test_Python_ExceptionNullMeshErrorSubtraction(self) :
        import pyg4ometry

        try :
            reg = pyg4ometry.geant4.Registry()
            s1   = pyg4ometry.geant4.solid.Box("s1",10,10,10, reg, "mm")
            s2   = pyg4ometry.geant4.solid.Box("s2",10,10,10, reg, "mm")

            subtra = pyg4ometry.geant4.solid.Subtraction("subtra",s1,s2,[[0,0,0],[0,0,0]],reg)
            raise pyg4ometry.exceptions.NullMeshError(subtra)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def test_Python_ExceptionNullMeshErrorOtherSolid(self) :
        import pyg4ometry

        try :
            reg = pyg4ometry.geant4.Registry()
            s1   = pyg4ometry.geant4.solid.Box("s1",10,10,10, reg, "mm")
            raise pyg4ometry.exceptions.NullMeshError(s1)
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def test_Python_ExceptionNullMeshErrorBasestring(self) :
        import pyg4ometry

        try :
            raise pyg4ometry.exceptions.NullMeshError("s1")
        except pyg4ometry.exceptions.NullMeshError : 
            pass

    def test_Python_ExceptionIdenticalNameError(self) :
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
