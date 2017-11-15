import pytest
import pyfluka

def test_get_overlap_overlap():
    path = "../test_input/region_overlap.inp"
    model = pyfluka.Model(path)

    # GIVEN: a pair of overlapping regions
    # RETURN: the extent of that overlap
    overlap1 = model.regions['overlap1']
    overlap2 = model.regions['overlap2']
    overlap = pyfluka.geometry.get_overlap(overlap1, overlap2)
    expected = pyfluka.geometry.Extent([-2.5, -5., -5.],
                                       [2.5, 5., 5.])
    assert overlap == expected

def test_get_overlap_no_overlap():
    path = "../test_input/region_overlap.inp"
    model = pyfluka.Model(path)
    # GIVEN: a pair of regions which do not overlap
    # RETURN: None
    no_overlap1 = model.regions['no_overlap1']
    no_overlap2 = model.regions['no_overlap2']
    assert pyfluka.geometry.get_overlap(no_overlap1, no_overlap2) is None
