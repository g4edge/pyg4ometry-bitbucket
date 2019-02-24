import pytest
import pygdml

import pyfluka.geometry as geo
import pyfluka.vector as vec


@pytest.fixture
def RPP():
    return geo.RPP("rpp", [0, 0, 0], [1, 1, 1])

@pytest.fixture
def null_zone(RPP):
    return geo.Zone([("+", RPP), ("-", RPP)])

@pytest.fixture
def wv():
    return geo.make_world_volume("worldname", "material")

@pytest.fixture
def region():
    box1 = geo.RPP("rpp", [0, 0, 0], [1, 1, 1])
    box2 = geo.RPP("rpp2", [0, 0, 0] , [1, 1, 0.5])
    # box1 - box2
    zone = geo.Zone([("+", box1), ("-", box2)])
    return geo.Region("region", [zone], "material")

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

def test_region_with_redundant_subtraction(RPP):
    sub = geo.RPP("redundant", [1e6, 1e6, 1e6],
                                [1e6+1, 1e6+1, 1e6+1])
    zone = geo.Zone([("+", RPP), ("-", sub)])
    # the original solid should be returned if from it is subtracted a
    # redundant subtraction.
    assert zone.evaluate(optimise=True) == RPP

def test_omit_redundant_RPP_intersection(RPP):
    big_rpp = geo.RPP("redundant",
                      [-1e3, -1e3, -1e3],
                      [1e3, 1e3, 1e3])
    zone = geo.Zone([("+", RPP), ("+", big_rpp)])
    assert zone.evaluate(optimise=True) == RPP

def test_omit_redundant_halfspace_intersection(RPP):
    for ctor in [geo.XZP, geo.XYP, geo.YZP]:
        halfspace = ctor("redundant", 1e3)
        zone = geo.Zone([("+", RPP), ("+", halfspace)])
        assert zone.evaluate(optimise=True) == RPP

def test_region_mesh_fail_null_zone(RPP, null_zone):
    z = geo.Zone([("+", RPP)])
    r = geo.Region("r", [z, null_zone], "material")
    with pytest.raises(pygdml.solid.NullMeshError):
        r.evaluate().gdml_solid().pycsgmesh()

def test_null_zone_mesh_fails(null_zone):
    with pytest.raises(pygdml.solid.NullMeshError):
        null_zone.evaluate().gdml_solid().pycsgmesh()


def test_get_overlap():
    pass

def test_connected_zones():
    pass

def test_coplanar_union():
    pass
