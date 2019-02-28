import pytest
import pygdml

import pyfluka.geometry as geo
import pyfluka.vector as vec


@pytest.fixture
def RPP():
    # A cube with sides of 1mm, from origin to 1, 1, 1..
    return geo.RPP("rpp", [0, 0, 0], [1, 1, 1])

@pytest.fixture
def RPP_at_1e6():
    return geo.RPP("rpp1e6", [1e6, 1e6, 1e6],
                   [1e6+1, 1e6+1, 1e6+1])

@pytest.fixture
def null_zone(RPP):
    return geo.Zone([("+", RPP), ("-", RPP)])

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

def test_region_with_redundant_subtraction(RPP, RPP_at_1e6):
    zone = geo.Zone([("+", RPP), ("-", RPP_at_1e6)])
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

def test_get_overlap_returns_none_on_no_overlap(RPP, RPP_at_1e6):
    assert geo.get_overlap(RPP, RPP_at_1e6) is None

def test_get_overlap(RPP):
    overlap_extent = geo.get_overlap(RPP, RPP)
    upper = 1 - geo.LENGTH_SAFETY
    lower = geo.LENGTH_SAFETY
    expected_extent = geo.Extent([lower, lower, lower], [upper, upper, upper])
    assert overlap_extent == expected_extent

def test_connected_zones():
    # All 3 of these overlap:
    box1 = geo.RPP("box1", [0,0,0], [1,1,1])
    box2 = geo.RPP("box2", [0.75, 0, 0.1], [1.75, 1, 0.9])
    box3 = geo.RPP("box4", [1.5, 0, 0.2], [2.5, 1, 0.8])
    zone1 = geo.Zone([("+", box1)])
    zone2 = geo.Zone([("+", box2)])
    zone3 = geo.Zone([("+", box3)])

    # This pair is separate to the first:
    box4 = geo.RPP("box4", [3, 0, 0], [4, 1, 1])
    zone4 = geo.Zone([("+", box4)])
    box5 = geo.RPP("box5", [3.75, 0, 0.1], [4.75, 1, 0.9])
    zone5 = geo.Zone([("+", box5)])

    # This zone is separate to other two.
    box6 = geo.RPP("box6", [5, 0, 0.], [6, 1, 1])
    zone6 = geo.Zone([("+", box6)])
    region = geo.Region("region", [zone1, zone2, zone3, zone4, zone5, zone6], "material")

    expected_connected_zones = [{0, 1, 2}, {3, 4}, {5}]
    assert list(region.connected_zones()) == expected_connected_zones
