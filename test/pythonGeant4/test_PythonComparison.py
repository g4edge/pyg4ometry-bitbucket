import numpy as _np

import pyg4ometry

from . import T700_ComparisonMaterial
from . import T701_ComparisonSolid
from . import T702_ComparisonLogicalVolume
from . import T704_ComparisonAssemblyVolume
from . import T705_ComparisonReplicaVolume
from . import T706_ComparisonDivisionVolume
from . import T707_ComparisonParameterisedVolume

def test_PythonComparison_T700_ComparisonMaterial():
    assert T700_ComparisonMaterial.Test()["teststatus"]

def test_PythonComparison_T701_ComparisonSolid():
    assert T701_ComparisonSolid.Test()["teststatus"]

def test_PythonComparison_T702_ComparisonLogicalVolume():
    assert T702_ComparisonLogicalVolume.Test()["teststatus"]

def test_PythonComparison_T704_ComparisonAssemblyVolume():
    assert T704_ComparisonAssemblyVolume.Test()["teststatus"]

def test_PythonComparison_T705_ComparisonReplicaVolume():
    assert T705_ComparisonReplicaVolume.Test()["teststatus"]

def test_PythonComparison_T706_ComparisonDivisionVolume():
    assert T706_ComparisonDivisionVolume.Test()["teststatus"]

def test_PythonComparison_T707_ComparisonParameterisedVolume():
    assert T707_ComparisonParameterisedVolume.Test()["teststatus"]

