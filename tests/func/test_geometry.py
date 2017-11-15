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

def test_region_disjoint_zones():
    path = "../test_input/disjoint_union.inp"
    model = pyfluka.Model(path)
    # GIVEN: a region which in which 0 and 1 are not disjoint but 2 is
    # disjoint with both 0 and 1:
    region = model.regions['disjoint']
    assert region.disjoint_zones() == {0: [2], 1: [2], 2: [0, 1]}
