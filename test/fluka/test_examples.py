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

def test_finite_cylinder_parallel_to_x_axis():
    xcentre = 2
    ycentre = 10
    zcentre = 10
    length = 20
    radius = 4

    cylinder_zone = ex.finite_cylinder_parallel_to_x_axis(xcentre=xcentre,
                                                          ycentre=ycentre,
                                                          zcentre=zcentre,
                                                          length=length,
                                                          radius=radius)
    extent = cylinder_zone.extent()
    assert extent.lower.x == xcentre - length / 2.0
    assert extent.upper.x == xcentre + length / 2.0

    assert extent.lower.y == ycentre - radius
    assert extent.upper.y == ycentre + radius

    assert extent.lower.z == zcentre - radius
    assert extent.upper.z == zcentre + radius

def test_finite_cylinder_parallel_to_y_axis():
    xcentre = 2
    ycentre = 10
    zcentre = 10
    length = 20
    radius = 4

    cylinder_zone = ex.finite_cylinder_parallel_to_y_axis(xcentre=xcentre,
                                                          ycentre=ycentre,
                                                          zcentre=zcentre,
                                                          length=length,
                                                          radius=radius)
    extent = cylinder_zone.extent()

    assert extent.lower.x == xcentre - radius
    assert extent.upper.x == xcentre + radius

    assert extent.lower.y == ycentre - length / 2.0
    assert extent.upper.y == ycentre + length / 2.0

    assert extent.lower.z == zcentre - radius
    assert extent.upper.z == zcentre + radius


def test_finite_cylinder_parallel_to_z_axis():
    xcentre = 2
    ycentre = 10
    zcentre = 10
    length = 20
    radius = 4

    cylinder_zone = ex.finite_cylinder_parallel_to_z_axis(xcentre=xcentre,
                                                          ycentre=ycentre,
                                                          zcentre=zcentre,
                                                          length=length,
                                                          radius=radius)
    extent = cylinder_zone.extent()

    assert extent.lower.x == xcentre - radius
    assert extent.upper.x == xcentre + radius

    assert extent.lower.y == ycentre - radius
    assert extent.upper.y == ycentre + radius

    assert extent.lower.z == zcentre - length / 2.0
    assert extent.upper.z == zcentre + length / 2.0
