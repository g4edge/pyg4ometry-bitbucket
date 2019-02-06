import pyfluka.examples as ex

def test_example_box_from_xzp_xyp_yzp():
    box_zone = ex.box_zone_from_xzp_xyp_yzp(xcentre=3, ycentre=6, zcentre=9,
                                            xsize=30, ysize=10, zsize=40)
    extent = box_zone.extent()
    assert extent.size.x == 30
    assert extent.size.y == 10
    assert extent.size.z == 40
    assert extent.centre.x == 3
    assert extent.centre.y == 6
    assert extent.centre.z == 9
