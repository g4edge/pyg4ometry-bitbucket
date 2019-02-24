import pytest
import pygdml

import pyfluka.geometry as geo
import pyfluka.vector as vec


@pytest.fixture
def RPP():
    return geo.RPP("rpp", [0, 0, 0], [1, 1, 1])

@pytest.fixture
def wv():
    return geo.make_world_volume("worldname", "material")


def test_make_world_volume_result_material(wv):
    assert wv.material == "material"

def test_make_world_volume_result_currentVolume_is_box(wv):
    assert type(wv.currentVolume) is pygdml.solid.Box

def test_make_world_volume_result_has_no_daughter_volumes(wv):
    assert wv.daughterVolumes == []


def test_get_overlap():
    pass

def test_connected_zones():
    pass

def test_coplanar_union():
    pass
