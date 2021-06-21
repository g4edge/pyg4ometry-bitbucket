import unittest as _unittest
import numpy as _np
import pyg4ometry.transformation as _trans
from pyg4ometry.geant4.solid import TwoVector

import logging as _log

# logger = _log.getLogger()
# logger.disabled = True

class PythonTests(_unittest.TestCase) :


    # #############################
    # solid two vector
    # #############################
    def test_Python_TwoVector_T001Constructor(self):
        v = TwoVector(1,2)

    def test_Python_TwoVector_T002Repr(self):
        v = TwoVector(1,2)
        s = str(v)

    def test_Python_TwoVector_T003GetItem(self):
        v = TwoVector(1,2)
        self.assertEqual(v[0],1)
        self.assertEqual(v[1],2)
        try :
            print(v[2])
        except IndexError :
            pass


    def test_Python_TwoVector_T004Add(self):
        v1 = TwoVector(1,2)
        v2 = TwoVector(3,4)

        i = 5
        f = 6.0
        s = "r"

        self.assertEqual((v1+v2)[0],4)
        self.assertEqual((v1+v2)[1],6)

        self.assertEqual((v1+i)[0],6)
        self.assertEqual((v1+i)[1],7)

        self.assertEqual((v1+f)[0],7.0)
        self.assertEqual((v1+f)[1],8.0)

        try :
            v1+s
        except ValueError :
            pass

    def test_Python_TwoVector_T005Sub(self):
        v1 = TwoVector(1,2)
        v2 = TwoVector(3,4)

        i = 5
        f = 6.0
        s = "r"

        self.assertEqual((v1-v2)[0],-2)
        self.assertEqual((v1-v2)[1],-2)

        self.assertEqual((v1-i)[0],-4)
        self.assertEqual((v1-i)[1],-3)

        self.assertEqual((v1-f)[0],-5.0)
        self.assertEqual((v1-f)[1],-4.0)

        try :
            v1-s
        except ValueError :
            pass


    def test_Python_TwoVector_T006Mul(self):
        v1 = TwoVector(1,2)

        f = 5
        s = "r"

        self.assertEqual((v1*f)[0],5)
        self.assertEqual((v1*f)[1],10)

        try :
            vv = v1*s
        except ValueError :
            pass

    # #############################
    # Transformation
    # #############################
    def test_Python_Rad2Deg(self) :
        self.assertEqual(_trans.rad2deg(_np.pi),180)

    def test_Python_Deg2Rad(self) :
        self.assertEqual(_trans.deg2rad(180),_np.pi)

    def test_Python_Tbxyz2axisangleX(self) :
        self.assertEqual(_trans.tbxyz2axisangle([_np.pi/2.0,0.0,0.0]),
                         [[1.0, 0.0, 0.0], 1.5707963267948966])

    def test_Python_Tbxyz2axisangleY(self) :
        self.assertEqual(_trans.tbxyz2axisangle([0.0,_np.pi/2.0,0.0]),
                         [[0.0, 1.0, 0.0], 1.5707963267948966])

    def test_Python_Tbxyz2axisangleZ(self) :
        self.assertEqual(_trans.tbxyz2axisangle([0.0,0.0,_np.pi/2.0]),
                         [[0.0, 0.0, 1.0], 1.5707963267948966])

    def test_Python_Matrix2axisangleX(self) :
        theta = 0.5
        m = _np.array([[             1,              0,              0],
                       [             0, _np.cos(theta),-_np.sin(theta)],
                       [             0, _np.sin(theta), _np.cos(theta)]])
        self.assertEqual(_trans.matrix2axisangle(m),
                         [[1.0000000000000002,0.0,0.0], 0.4999999999999999])

    def test_Python_Matrix2axisangleY(self) :
        theta = 0.5
        m = _np.array([[_np.cos(theta),              0,-_np.sin(theta)],
                       [             0,              1,              0],
                       [_np.sin(theta),              0, _np.cos(theta)]])
        self.assertEqual(_trans.matrix2axisangle(m),
                         [[0.0, -1.0000000000000002,0.0], 0.4999999999999999])

    def test_Python_Matrix2axisangleZ(self) :
        theta = 0.5
        m = _np.array([[_np.cos(theta), -_np.sin(theta),0],
                       [_np.sin(theta), _np.cos(theta) , 0],
                       [             0,               0, 1]])
        self.assertEqual(_trans.matrix2axisangle(m),
                         [[0.0, 0.0, 1.0000000000000002], 0.4999999999999999])


    def test_Python_Axisangle2matrixX(self) :
        print(_trans.axisangle2matrix([1.0,0,0],_np.pi/2.0))

    def test_Python_Axisangle2matrixY(self) :
        print(_trans.axisangle2matrix([0,1,0],_np.pi/2.0))

    def test_Python_Axisangle2matrixZ(self):
        print(_trans.axisangle2matrix([0, 0, 1], _np.pi / 2.0))

    def test_Python_Matrix2tbxyz(self) :
        pass

    def test_Python_Tbxyz2matrix(self) :
        pass

    def test_Python_Matrix_MatrixFromTo(self) :
        print(_trans.matrix_from([0,0,1],[0,1,0]))

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

    def test_Python_GetLocalMesh(self):
        import pyg4ometry

        reg = pyg4ometry.geant4.Registry()
        s1 = pyg4ometry.geant4.solid.Box("s1", 10, 10, 10, reg, "mm")
        l1 = pyg4ometry.geant4.LogicalVolume(s1, "G4_Galactic", "l1", reg)
        l1.mesh.getLocalMesh()

    def test_Python_Remesh(self):
        import pyg4ometry

        reg = pyg4ometry.geant4.Registry()
        s1 = pyg4ometry.geant4.solid.Box("s1", 10, 10, 10, reg, "mm")
        l1 = pyg4ometry.geant4.LogicalVolume(s1, "G4_Galactic", "l1", reg)
        l1.mesh.remesh()

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

    ##############################
    # VtkVisualisation
    ##############################

    def test_Python_VisualisationVtk_setOpacity(self):
        import pyg4ometry.test.pythonGeant4.T001_Box

        r = pyg4ometry.test.pythonGeant4.T001_Box.Test(True,False)
        v  = r['vtkViewer']
        v.setOpacity(0,0)
        v.setOpacity(0.5,-1)

    def test_Python_VisualisationVtk_setWireframe(self):
        import pyg4ometry.test.pythonGeant4.T001_Box

        r = pyg4ometry.test.pythonGeant4.T001_Box.Test(True,False)
        v  = r['vtkViewer']
        v.setWireframe()

    def test_Python_VisualisationVtk_setSurface(self):
        import pyg4ometry.test.pythonGeant4.T001_Box

        r = pyg4ometry.test.pythonGeant4.T001_Box.Test(True,False)
        v  = r['vtkViewer']
        v.setSurface()

    def test_Python_VisualisationVtk_setWireframe_VisualisationOptions(self):
        import pyg4ometry.test.pythonGeant4.T001_Box
        import pyg4ometry.visualisation.VtkViewer

        r = pyg4ometry.test.pythonGeant4.T001_Box.Test(True,False)
        lv = r['logicalVolume']
        dv = lv.daughterVolumes[0]
        dv.visOptions.representation = "wireframe"

        v = pyg4ometry.visualisation.VtkViewer()
        v.addLogicalVolume(lv)
        v.view(interactive=False)

    def test_Python_VisualisationVtk_setOpacityOverlap(self):
        import pyg4ometry.test.pythonGeant4.T103_overlap_copl

        r = pyg4ometry.test.pythonGeant4.T103_overlap_copl.Test(True,False)
        v  = r['vtkViewer']
        v.setOpacityOverlap(0)

    def test_Python_VisualisationVtk_setWireframeOverlap(self):
        import pyg4ometry.test.pythonGeant4.T103_overlap_copl

        r = pyg4ometry.test.pythonGeant4.T103_overlap_copl.Test(True,False)
        v  = r['vtkViewer']
        v.setWireframeOverlap()

    def test_Python_VisualisationVtk_setSurfaceOverlap(self):
        import pyg4ometry.test.pythonGeant4.T103_overlap_copl

        r = pyg4ometry.test.pythonGeant4.T103_overlap_copl.Test(True,False)
        v  = r['vtkViewer']
        v.setSurfaceOverlap()

    def test_Python_VisualisationVtk_setRandomColours(self):
        import pyg4ometry.test.pythonGeant4.T103_overlap_copl

        r = pyg4ometry.test.pythonGeant4.T103_overlap_copl.Test(True,False)
        v  = r['vtkViewer']
        v.setRandomColours()

    def test_Python_VisualisationVtk_RandomColour(self):
        import pyg4ometry.test.pythonCompoundExamples.lhc_blm_model as lhc_blm_model
        import pyg4ometry
        wlv = lhc_blm_model.make_lhc_blm()
        v = pyg4ometry.visualisation.VtkViewerColoured(defaultColour="random")
        v.addLogicalVolume(wlv)

    def test_Python_VisualisationVtk_DefaultMaterial(self):
        import pyg4ometry.test.pythonCompoundExamples.lhc_blm_model as lhc_blm_model
        import pyg4ometry
        wlv = lhc_blm_model.make_lhc_blm()
        v = pyg4ometry.visualisation.VtkViewerColouredMaterial()
        v.addLogicalVolume(wlv)

    def test_Python_VisualisationVtk_CustomMaterialColours(self):
        import pyg4ometry.test.pythonCompoundExamples.lhc_blm_model as lhc_blm_model
        import pyg4ometry
        wlv = lhc_blm_model.make_lhc_blm()
        colours = lhc_blm_model.materialToColour
        v = pyg4ometry.visualisation.VtkViewerColoured(materialVisOptions=colours)
        v.addLogicalVolume(wlv)

if __name__ == '__main__':
    _unittest.main(verbosity=2)
