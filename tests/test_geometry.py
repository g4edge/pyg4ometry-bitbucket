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

def test_subtract_from_world_volume(wv):
    # cube with sides of length 1 and centeres at the origin.
    cube = geo.RPP("cube", [-0.5, -0.5, -0.5], [0.5, 0.5, 0.5])
    # rcc which goes through the centre of cube, centred on (x, y) = (0, 0)
    # and pointing along z, radius 0.25.
    hole = geo.RCC("hole", [0., 0., -1.], [0., 0.,1.], 0.25)
    zone = geo.Zone([("+", cube), ("-", hole)])
    region = geo.Region("r", [zone], "a material")
    region.add_to_volume(wv)

    geo.subtract_from_world_volume(wv, [hole])

    subtraction = pygdml.solid.Subtraction("name",
                                           cube.gdml_solid(),
                                           hole.gdml_solid(length_safety="trim"),
                                           [[3.141592653589793,
                                             0.0,
                                             3.141592653589793],
                                            [ 0. ,  0. , -0.5]])
    assert pygdml.solid.equal_tree(wv.currentVolume, subtraction)

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
