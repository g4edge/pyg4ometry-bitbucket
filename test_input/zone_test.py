import pyfluka



yzplanlow = pyfluka.bodies.YZP("yzplanlow", [-30.0])
yzplanhigh = pyfluka.bodies.YZP("yzplanhigh", [30.0])
xyplanlow = pyfluka.bodies.XYP("xyplanlow", [-30.])
xyplanhigh = pyfluka.bodies.XYP("xyplanhigh", [30.0])
xzplanlow = pyfluka.bodies.XZP("xzplanlow", [-30.0])
xzplanhigh = pyfluka.bodies.XZP("xzplanhigh", [30.0])

cube_defn = [('+', yzplanhigh),
             ('-', yzplanlow),
             ('+', xyplanhigh),
             ('-', xyplanlow),
             ('+', xzplanhigh),
             ('-', xzplanlow)]

zone_1 = pyfluka.bodies.Zone(('+', yzplanhigh),
                             ('-', yzplanlow))
zone_2 = pyfluka.bodies.Zone(('+', xyplanhigh),
                             ('-', xyplanlow))
zone_3 = pyfluka.bodies.Zone(('+', xzplanhigh),
                             ('-', xzplanlow))

cube_def_w_zonz = [('+', zone_1),
                   ('+', zone_2),
                   ('+', zone_3)]

cube_zone = pyfluka.bodies.Zone(*cube_defn)
cube_zone_from_subz = pyfluka.bodies.Zone(*cube_def_w_zonz)
