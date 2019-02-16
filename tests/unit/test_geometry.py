import pytest
import pyfluka.geometry as geo
import pyfluka.vector as vec

def test_RPP_ctor():
    # Box with lower corner at origin and opposite corner at [1, 1, 1]
    rpp = geo.RPP("aname", [0, 0, 0], [1, 1, 1])
    assert rpp.name == "aname"
    assert rpp.lower.x == 0
    assert rpp.lower.y == 0
    assert rpp.lower.z == 0
    assert rpp.upper.x == 1
    assert rpp.upper.y == 1
    assert rpp.upper.z == 1

def test_XYP_ctor():
    xyp = geo.XYP("aname", 10)
    assert xzp.name == "aname"
    assert xzp.y == 10

def test_XZP_ctor():
    xzp = geo.XZP("aname", 10)
    assert xzp.name == "aname"
    assert xzp.y == 10

def test_YZP_ctor():
    yzp = geo.YZP("aname", 10)
    assert yzp.name == "aname"
    assert yzp.y == 10

def test_XCC_ctor():
    xcc = geo.XCC("xcc", 10, 12, 14)
    assert xcc.name == "xcc"
    assert xcc.y == 10
    assert xcc.z == 12
    assert xcc.radius == 14

def test_YCC_ctor():
    ycc = geo.YCC("ycc", 10, 12, 14)
    assert ycc.name == "ycc"
    assert ycc.z == 10
    assert ycc.x == 12
    assert ycc.radius == 14

def test_ZCC_ctor():
    zcc = geo.ZCC("zcc", 10, 12, 14)
    assert zcc.name == "zcc"
    assert zcc.x == 10
    assert zcc.y == 12
    assert zcc.radius == 14

def test_RPP_ctor():
    rpp = geo.RPP("rpp",
                  [0, 0.1, 0.2],
                  [1, 1.2, 1.3])
    assert rpp.name == "rpp"
    assert rpp.lower == vec.Three([0, 0, 0])
    assert rpp.upper == vec.Three([1, 1.2, 1.3])
