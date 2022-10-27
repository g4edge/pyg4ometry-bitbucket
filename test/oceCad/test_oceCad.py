import pyg4ometry as _pyg4
import os as _os

def commonCode(fileName, mats ={}, skip = [], mesh = {}) :
    fileName = _os.path.join(_os.path.dirname(__file__), fileName)
    r = _pyg4.pyoce.Reader(fileName)
    #r.shapeTool.Dump()
    ls = r.freeShapes()
    worldName = _pyg4.pyoce.pythonHelpers.get_TDataStd_Name_From_Label(ls.Value(1))
    reg = _pyg4.convert.oce2Geant4(r.shapeTool, worldName,mats,skip,mesh)
    wa = reg.logicalVolumeDict[worldName]
    # wl = wa.makeWorldVolume()

def test_1_BasicSolids_Bodies() :
    commonCode("1_BasicSolids_Bodies.step")

def test_2_BasicSolids_Components() :
    commonCode("2_BasicSolids_Components.step")

def test_3_BasicSolids_Components_Copied() :
    commonCode("3_BasicSolids_Components_Copied.step")

def test_4_BasicSolids_Components_ManyBodies() :
    commonCode("4_BasicSolids_Components_ManyBodies.step")

def test_5_BasicSolids_Components_NestedComponents() :
    commonCode("5_BasicSolids_Components_NestedComponents.step")

def test_6_SolidFromSketch() :
    commonCode("6_SolidFromSketch.step")

def test_7_Booleans() :
    commonCode("7_Booleans.step")

def test_8_rotationTest() :
    commonCode("8_rotationTest.step")

def test_9_AshTray() :
    commonCode("9_AshTray.step")

def test_10_SectorBendSmall() :
    commonCode("10_SectorBendSmall.step")

def test_11_Material() :
    mats = {"0:1:1:1:1": "G4_H",
            "0:1:1:1:4": "G4_He"}
    commonCode("10_SectorBendSmall.step",mats=mats)

def test_12_Skip() :
    skip = ["0:1:1:1:4"]
    commonCode("10_SectorBendSmall.step",skip=skip)

def test_13_Mesh() :
    mesh = {"0:1:1:1:2": (0.05, 0.05)}
    commonCode("10_SectorBendSmall.step",mesh=mesh)

def test_14_MonolithicConversion() :
    r = _pyg4.pyoce.Reader(_os.path.join(_os.path.dirname(__file__),"1_BasicSolids_Bodies.step"))
    ls = r.freeShapes()
    worldName = _pyg4.pyoce.pythonHelpers.get_TDataStd_Name_From_Label(ls.Value(1))
    worldShape = r.shapeTool.GetShape(ls.Value(1))
    greg = _pyg4.geant4.Registry()
    _pyg4.convert.oceShape_Geant4_Tessellated("world",worldShape,greg)
