import pytest
import pyfluka.geometry as geo


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
    assert xzp.name = "aname"
    assert xzp.y == 10

def test_XZP_ctor():
    xzp = geo.XZP("aname", 10)
    assert xzp.name == "aname"
    assert xzp.y == 10

def test_YZP_ctor():
    yzp = geo.YZP("aname", 10)
    assert yzp.name == "aname"
    assert yzp.y == 10
