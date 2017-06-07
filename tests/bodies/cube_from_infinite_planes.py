import pyfluka

yzplanlow = pyfluka.bodies.YZP("yzplanlow", [-30.0])
yzplanhigh = pyfluka.bodies.YZP("yzplanhigh", [30.0])
xyplanlow = pyfluka.bodies.XYP("xyplanlow", [-30.])
xyplanhigh = pyfluka.bodies.XYP("xyplanhigh", [30.0])
xzplanlow = pyfluka.bodies.XZP("xzplanlow", [-30.0])
xzplanhigh = pyfluka.bodies.XZP("xzplanhigh", [30.0])

# yzplanhigh(1e3).view(setclip=False)
# yzplanlow(1e3).view(setclip=False)
# (yzplanhigh(1e3) - yzplanlow(1e3)).view(setclip=False)
# (xzplanhigh(1e3) - xzplanlow(1e3)).view(setclip=False)
# (xyplanhigh(1e3) - xyplanlow(1e3)).view(setclip=False)

scale = 1e2

((yzplanhigh(scale) - yzplanlow(scale))
 + (xzplanhigh(scale) - xzplanlow(scale))
 + (xyplanhigh(scale) - xyplanlow(scale))).view(setclip=True)

(yzplanhigh(scale)
 + xzplanhigh(scale)
 + xyplanhigh(scale)
 - yzplanlow(scale)
 - xzplanlow(scale)
 - xyplanlow(scale)).view(setclip=True)


(yzplanhigh(scale) | yzplanlow(scale)).view(setclip=False)
(yzplanhigh(scale) - yzplanlow(scale)).view(setclip=False)
# (yzplanlow(1e5) - yzplanhigh(1e5)).view(setclip=False)
