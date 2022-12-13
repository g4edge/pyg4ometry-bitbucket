import numpy as _np
import os as _os

import pyg4ometry

from . import T000_SolidBase
from . import T001_Box
from . import T002_Tubs
from . import T003_CutTubs
from . import T0031_CutTubs_number
from . import T0032_CutTubs_string
from . import T0033_CutTubs_expression
from . import T0034_CutTubs_DefineTree
from . import T004_Cons
from . import T005_Para
from . import T006_Trd
from . import T007_Trap
from . import T008_Sphere
from . import T009_Orb
from . import T010_Torus
from . import T011_Polycone
from . import T012_GenericPolycone
from . import T013_Polyhedra
from . import T014_GenericPolyhedra
from . import T015_EllipticalTube
from . import T016_Ellipsoid
from . import T017_EllipticalCone
from . import T018_Paraboloid
from . import T019_Hyperboloid
from . import T020_Tet
from . import T021_ExtrudedSolid
from . import T022_TwistedBox
from . import T023_TwistedTrap
from . import T024_TwistedTrd
from . import T025_TwistedTubs
from . import T026_GenericTrap
from . import T028_Union
from . import T029_Subtraction
from . import T030_Intersection
from . import T031_MultiUnion
from . import T032_Scaled
from . import T033_TessellatedSolid
from . import T101_physical_logical
from . import T102_overlap_none
from . import T103_overlap_copl
from . import T103_overlap_copl_simple
from . import T104_overlap_volu
from . import T105_assembly
from . import T106_replica_x
from . import T107_replica_y
from . import T108_replica_z
from . import T109_replica_phi
from . import T110_replica_rho
from . import T111_parameterised_box
from . import T112_parameterised_tube
from . import T201_Materials
from . import T202_OpticalSurface
from . import T203_MaterialsRegistry
from . import T204_NIST_Element
from . import T205_NIST_Material
from . import T300_overlap_assembly_regular_lv
from . import T301_overlap_assembly_none
from . import T302_overlap_assembly_coplanar
from . import T303_overlap_assembly_daughter_collision
from . import T304_overlap_assembly_volumetric
from . import T305_overlap_assembly_nested
from . import T306_overlap_replica_x
from . import T307_overlap_replica_x_internal
from . import T400_MergeRegistry
from . import T401_MergeRegistry_Box
from . import T402_MergeRegistry_Tubs
from . import T403_MergeRegistry_CutTubs
from . import T404_MergeRegistry_Cons
from . import T405_MergeRegistry_Para
from . import T406_MergeRegistry_Trd
from . import T407_MergeRegistry_Trap
from . import T408_MergeRegistry_Sphere
from . import T409_MergeRegistry_Orb
from . import T410_MergeRegistry_Torus
from . import T411_MergeRegistry_Polycone
from . import T412_MergeRegistry_GenericPolycone
from . import T413_MergeRegistry_Polyhedra
from . import T414_MergeRegistry_GenericPolyhedra
from . import T415_MergeRegistry_EllipticalTube
from . import T416_MergeRegistry_Ellipoid
from . import T417_MergeRegistry_EllipticalCone
from . import T418_MergeRegistry_Paraboloid
from . import T419_MergeRegistry_Hyperboloid
from . import T420_MergeRegistry_Tet
from . import T421_MergeRegistry_ExtrudedSolid
from . import T422_MergeRegistry_TwistedBox
from . import T423_MergeRegistry_TwistedTrap
from . import T424_MergeRegistry_TwistedTrd
from . import T425_MergeRegistry_TwistedTubs
from . import T426_MergeRegistry_GenericTrap
from . import T428_MergeRegistry_Union
from . import T429_MergeRegistry_Subtraction
from . import T430_MergeRegistry_Intersection
from . import T431_MergeRegistry_MultiUnion
from . import T432_MergeRegistry_Box_AssemblyConversion
from . import T433_MergeRegistry_Scale
from . import T434_MergeRegistry_CollapseAssembly
from . import T600_LVTessellated
from . import T601_reflect
# from . import T602_lv_cull_daughters
# from . import T603_lv_change_solid_and_trim
# from . import T604_lv_change_solid_and_trim_rot
from . import T605_LvChangeSolid
from . import T606_LvClipSolid
from . import T607_LvChangeAndClipSolid
from . import T608_LvClipSolidRecursive
from . import T609_LvClipSolidRecursiveAssembly

writeNISTMaterials = True

def test_PythonGeant_Plane() :
    p = pyg4ometry.geant4.solid.Plane("plane",[0,0,1],1000)
    str(p)

def test_PythonGeant_Wedge() :
    w = pyg4ometry.geant4.solid.Wedge("wedge",1000,0,1.5*_np.pi,10000)
    str(w)

def test_PythonGeant_T000_SolidBase() :
    assert T000_SolidBase.Test()["testStatus"]

def test_PythonGeant_T001_Box() :
    assert T001_Box.Test(False,False,writeNISTMaterials)["testStatus"]

def test_PythonGeant_T002_Tubs() :
    assert T002_Tubs.Test(False,False,writeNISTMaterials=writeNISTMaterials)

def test_PythonGeant_T003_CutTubs() :
    assert T003_CutTubs.Test(False, False, T003_CutTubs.normal, writeNISTMaterials=writeNISTMaterials)["testStatus"]
    assert T003_CutTubs.Test(False, False, T003_CutTubs.flat_ends)["testStatus"]
    assert T0031_CutTubs_number.Test(False, False)["testStatus"]
    assert T0032_CutTubs_string.Test(False, False)["testStatus"]
    # TODO
    # assert T0033_CutTubs_expression.Test(False, False)["testStatus"]
    assert T0034_CutTubs_DefineTree.Test(False,False)["testStatus"]

def test_PythonGeant_T004_Cons() :
    try :
        assert T004_Cons.Test(False,False,T004_Cons.r1min_gt_r1max,writeNISTMaterials=writeNISTMaterials)["testStatus"]
    except ValueError :
        pass

    try :
        assert T004_Cons.Test(False,False,T004_Cons.r2min_gt_r2max)["testStatus"]
    except ValueError :
        pass

    try :
        assert T004_Cons.Test(False,False,T004_Cons.dphi_gt_2pi)["testStatus"]
    except ValueError :
        pass

    assert T004_Cons.Test(False,False,T004_Cons.dphi_eq_2pi)["testStatus"]
    assert T004_Cons.Test(False,False,T004_Cons.cone_up)["testStatus"]
    assert T004_Cons.Test(False,False,T004_Cons.inner_cylinder)["testStatus"]

    assert T004_Cons.Test(False,False)["testStatus"]

def test_PythonGeant_T005_Para() :
    assert T005_Para.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T006_Trd() :
    assert T006_Trd.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T007_Trap() :
    assert T007_Trap.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T008_Sphere() :
    assert T008_Sphere.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T009_Orb() :
    assert T009_Orb.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T010_Torus() :
    assert T010_Torus.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T011_Polycone() :
    assert T011_Polycone.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T012_GenericPolycone() :
    assert T012_GenericPolycone.Test(False,False,T012_GenericPolycone.normal,writeNISTMaterials=writeNISTMaterials)["testStatus"]

    try :
        T012_GenericPolycone.Test(False,False,T012_GenericPolycone.two_planes)["testStatus"]
    except ValueError :
        pass

def test_PythonGeant_T013_Polyhedra() :
    assert T013_Polyhedra.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T014_GenericPolyhedra() :
    assert T014_GenericPolyhedra.Test(False,False,T014_GenericPolyhedra.normal,writeNISTMaterials=writeNISTMaterials)["testStatus"]

    try :
        T014_GenericPolyhedra.Test(False,False, T014_GenericPolyhedra.two_planes)["testStatus"]
    except ValueError :
        pass

def test_PythonGeant_T015_EllipticalTube() :
    assert T015_EllipticalTube.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T016_Ellipsoid() :
    assert T016_Ellipsoid.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T017_EllipticalCone() :
    assert T017_EllipticalCone.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

    try :
        T017_EllipticalCone.Test(False,False, T017_EllipticalCone.zcut_outofrange,writeNISTMaterials=writeNISTMaterials)["testStatus"]
    except ValueError :
        pass

def test_PythonGeant_T018_Paraboloid() :
    assert T018_Paraboloid.Test(False,False,writeNISTMaterials=writeNISTMaterials)["teststatus"]

def test_PythonGeant_T019_Hyperboloid() :
    assert T019_Hyperboloid.Test(False,False,T019_Hyperboloid.normal,writeNISTMaterials=writeNISTMaterials)["teststatus"]
    assert T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_eq_zero,writeNISTMaterials=writeNISTMaterials)["teststatus"]

    try :
        T019_Hyperboloid.Test(False,False,T019_Hyperboloid.rmin_gt_rmax,writeNISTMaterials=writeNISTMaterials)["testStatus"]
    except ValueError :
        pass

def test_PythonGeant_T020_Tet() :
    assert T020_Tet.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T021_ExtrudedSolid() :
    assert T021_ExtrudedSolid.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T022_TwistedBox() :
    assert T022_TwistedBox.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T023_TwistedTrap() :
    assert T023_TwistedTrap.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T024_TwistedTrd() :
    assert T024_TwistedTrd.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T025_TwistedTubs() :
    assert T025_TwistedTubs.Test(False,False,writeNISTMaterials=writeNISTMaterials)["teststatus"]

def test_PythonGeant_T026_GenericTrap() :
    assert T026_GenericTrap.Test(False,False,writeNISTMaterials=writeNISTMaterials)["teststatus"]

def test_PythonGeant_T028_Union() :
    assert T028_Union.Test(False,False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]
    assert T028_Union.Test(False,False,True,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T029_Subtraction() :
    assert T029_Subtraction.Test(False,False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

    #try :
    #    T029_Subtraction.Test(False,False,True)
    #except pyg4ometry.exceptions.NullMeshError :
    #    pass

def test_PythonGeant_T030_Intersection() :
    assert T030_Intersection.Test(False,False,T030_Intersection.normal,writeNISTMaterials=writeNISTMaterials)["teststatus"]

    #try :
    #    T030_Intersection.Test(False,False,T030_Intersection.non_intersecting)
    #except pyg4ometry.exceptions.NullMeshError :
    #    pass

def test_PythonGeant_T031_MultiUnion() :
    assert T031_MultiUnion.Test(False,False,writeNISTMaterials=writeNISTMaterials)["teststatus"]

def test_PythonGeant_T032_Scaled():
    assert T032_Scaled.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T033_Tessellated():
    assert T033_TessellatedSolid.Test(False,False,writeNISTMaterials=writeNISTMaterials)["testStatus"]

def test_PythonGeant_T101_PhysicalLogical():
    assert T101_physical_logical.Test()["testStatus"]

def test_PythonGeant_T102_OverlapMone():
    assert T102_overlap_none.Test()["testStatus"]

def test_PythonGeant_T103_OverlapCopl():
    assert T103_overlap_copl.Test()["testStatus"]

def test_PythonGeant_T103_OverlapCopl_Simple():
    assert T103_overlap_copl_simple.Test()["testStatus"]

def test_PythonGeant_T104_OverlapVolu():
    assert T104_overlap_volu.Test()["testStatus"]

def test_PythonGeant_T105_Assembly():
    assert T105_assembly.Test()["testStatus"]

def test_PythonGeant_T106_ReplicaX():
    assert T106_replica_x.Test()["testStatus"]

def test_PythonGeant_T107_ReplicaY():
    assert T107_replica_y.Test()["testStatus"]

def test_PythonGeant_T108_ReplicaZ():
    assert T108_replica_z.Test()["testStatus"]

def test_PythonGeant_T109_ReplicaPhi():
    assert T109_replica_phi.Test()["testStatus"]

def test_PythonGeant_T110_ReplicaRho():
    assert T110_replica_rho.Test()["testStatus"]

def test_PythonGeant_T111_parameterised_box():
    assert T111_parameterised_box.Test()["testStatus"]

def test_PythonGeant_T112_parameterised_tube():
    assert T112_parameterised_tube.Test()["testStatus"]

def test_PythonGeant_T201_Materials():
    T201_Materials.Test_MaterialPredefined()
    T201_Materials.Test_MaterialSingleElement()
    T201_Materials.Test_MaterialCompoundMassFraction()
    T201_Materials.Test_MaterialCompoundAtoms()
    T201_Materials.Test_MaterialMixture()
    T201_Materials.Test_MaterialIsotopes()

def test_PythonGeant_T202_OpticalSurface():
    T202_OpticalSurface.Test_OpticalSurface()

def test_PythonGeant_T203_MaterialsRegistry():
    T203_MaterialsRegistry.Test_MaterialsRegistry()

def test_PythonGeant_T204_NIST_Element():
    T204_NIST_Element.Test_NIST_Element()

def test_PythonGeant_T205_NIST_Material():
    T205_NIST_Material.Test_NIST_Material()

def test_PythonGeant_T400_MergeRegistry():
    assert T400_MergeRegistry.Test()["teststatus"]

def test_PythonGeant_T401_MergeRegistry_Box():
    assert T401_MergeRegistry_Box.Test(False,False)["testStatus"]

def test_PythonGeant_T402_MergeRegistry_Tubs():
    assert T402_MergeRegistry_Tubs.Test()["testStatus"]

def test_PythonGeant_T403_MergeRegistry_CutTubs():
    assert T403_MergeRegistry_CutTubs.Test()["testStatus"]

def test_PythonGeant_T404_MergeRegistry_Cons():
    assert T404_MergeRegistry_Cons.Test()["testStatus"]

def test_PythonGeant_T405_MergeRegistry_Para():
    assert T405_MergeRegistry_Para.Test()["testStatus"]

def test_PythonGeant_T406_MergeRegistry_Trd():
    assert T406_MergeRegistry_Trd.Test()["testStatus"]

def test_PythonGeant_T407_MergeRegistry_Trap():
    assert T407_MergeRegistry_Trap.Test()["testStatus"]

def test_PythonGeant_T408_MergeRegistry_Sphere():
    assert T408_MergeRegistry_Sphere.Test()["testStatus"]

def test_PythonGeant_T409_MergeRegistry_Orb():
    assert T409_MergeRegistry_Orb.Test()["testStatus"]

def test_PythonGeant_T410_MergeRegistry_Torus():
    assert T410_MergeRegistry_Torus.Test()["testStatus"]

def test_PythonGeant_T411_MergeRegistry_Polycone():
    assert T411_MergeRegistry_Polycone.Test()["testStatus"]

def test_PythonGeant_T412_MergeRegistry_GenericPolycone():
    assert T412_MergeRegistry_GenericPolycone.Test()["testStatus"]

def test_PythonGeant_T413_MergeRegistry_Polyhedra():
    assert T413_MergeRegistry_Polyhedra.Test()["testStatus"]

def test_PythonGeant_T414_MergeRegistry_GenericPolyhedra():
    assert T414_MergeRegistry_GenericPolyhedra.Test()["testStatus"]

def test_PythonGeant_T415_MergeRegistry_EllipticalTube():
    assert T415_MergeRegistry_EllipticalTube.Test()["testStatus"]

def test_PythonGeant_T416_MergeRegistry_Ellipsoid():
    assert T416_MergeRegistry_Ellipoid.Test()["testStatus"]

def test_PythonGeant_T417_MergeRegistry_EllipticalCone():
    assert T417_MergeRegistry_EllipticalCone.Test()["testStatus"]

def test_PythonGeant_T418_MergeRegistry_EllipticalParaboloid():
    assert T418_MergeRegistry_Paraboloid.Test()["testStatus"]

def test_PythonGeant_T419_MergeRegistry_Hyperboloid():
    assert T419_MergeRegistry_Hyperboloid.Test()["testStatus"]

def test_PythonGeant_T420_MergeRegistry_Tet():
    assert T420_MergeRegistry_Tet.Test()["testStatus"]

def test_PythonGeant_T421_MergeRegistry_ExtrudedSolid():
    assert T421_MergeRegistry_ExtrudedSolid.Test()["testStatus"]

def test_PythonGeant_T422_MergeRegistry_TwistedBox():
    assert T422_MergeRegistry_TwistedBox.Test()["testStatus"]

def test_PythonGeant_T423_MergeRegistry_TwistedTrap():
    assert T423_MergeRegistry_TwistedTrap.Test()["testStatus"]

def test_PythonGeant_T424_MergeRegistry_TwistedTrd():
    assert T424_MergeRegistry_TwistedTrd.Test()["testStatus"]

def test_PythonGeant_T425_MergeRegistry_TwistedTubs():
    assert T425_MergeRegistry_TwistedTubs.Test()["testStatus"]

def test_PythonGeant_T426_MergeRegistry_GenericTrap():
    assert T426_MergeRegistry_GenericTrap.Test()["testStatus"]

def test_PythonGeant_T428_MergeRegistry_Union():
    assert T428_MergeRegistry_Union.Test()["testStatus"]

def test_PythonGeant_T429_MergeRegistry_Subtraction():
    assert T429_MergeRegistry_Subtraction.Test()["testStatus"]

def test_PythonGeant_T430_MergeRegistry_Intersection():
    assert T430_MergeRegistry_Intersection.Test()["testStatus"]

def test_PythonGeant_T431_MergeRegistry_MultiUnion():
    assert T431_MergeRegistry_MultiUnion.Test()["testStatus"]

def test_PythonGeant_T432_MergeRegistryBoxAssemblyConverion():
    assert T432_MergeRegistry_Box_AssemblyConversion.Test()["testStatus"]

def test_PythonGeant_T433_MergeRegistry_Scale():
    assert T433_MergeRegistry_Scale.Test()["testStatus"]

def test_PythonGeant_T434_MergeRegistry_CollapseAssembly():
    assert T434_MergeRegistry_CollapseAssembly.Test()["testStatus"]

def test_PythonGeant_T600_LVTessellated():
    assert T600_LVTessellated.Test()["testStatus"]

def test_PythonGeant_T601_reflect():
    assert T601_reflect.Test()["testStatus"]

#def test_PythonGeant_T602_lv_cull_daughters():
#    assert T602_lv_cull_daughters.Test()["testStatus"]

#def test_PythonGeant_T603_lv_change_solid_and_trim():
#    assert T603_lv_change_solid_and_trim.Test()["testStatus"]

#def test_PythonGeant_T604_lv_change_solid_and_trim_rot():
#    assert T604_lv_change_solid_and_timr_rot.Test()["testStatus"]

def test_PythonGeant_T605_LvChangeSolid():
    assert T605_LvChangeSolid.Test()["testStatus"]

def test_PythonGeant_T606_LvClipSolid():
    assert T606_LvClipSolid.Test()["testStatus"]

def test_PythonGeant_T607_LvChangeAndClipSolid():
    assert T607_LvChangeAndClipSolid.Test()["testStatus"]

def test_PythonGeant_T608_LvClipSolidRecursive():
    assert T608_LvClipSolidRecursive.Test()["testStatus"]

def test_PythonGeant_T609_LvClipSolidRecursiveAssembly():
    assert T609_LvClipSolidRecursiveAssembly.Test()["testStatus"]
