import pyfluka.geometry as geo

def box_zone_from_xzp_xyp_yzp(xcentre=0, ycentre=0, zcentre=0,
                              xsize=20, ysize=20, zsize=20):


    yzp1 = geo.YZP("yzp1", xcentre + xsize/2.0)
    yzp2 = geo.YZP("yzp1", xcentre - xsize/2.0)

    xzp1 = geo.XZP("xzp1", ycentre + ysize/2.0)
    xzp2 = geo.XZP("xzp1", ycentre - ysize/2.0)

    xyp1 = geo.XYP("xyp1", zcentre + zsize/2.0)
    xyp2 = geo.XYP("xyp1", zcentre - zsize/2.0)

    zone =  geo.Zone([("+", yzp1),
                      ("-", yzp2),
                      ("+", xzp1),
                      ("-", xzp2),
                      ("+", xyp1),
                      ("-", xyp2)])
    return zone
