import pyfluka

a1 = pyfluka.bodies.PLA("a1", [7.592566023653, 6.5079137345597, 0.0,
                               24.0, 20.0, 0.0])
a2 = pyfluka.bodies.PLA("a2", [7.5568908278982, 6.5493053841784,
                               0.0, -32.0, -16.0, 0.0])
b1 = pyfluka.bodies.PLA("b1", [-6.251073559164, 7.8053878416071,
                               0.0, -44.0, 44.0, 0.0])
b2 = pyfluka.bodies.PLA("b2", [-6.564195209058, 7.5439605816431,
                               0.0, 20.0, -20.0, 0.0])
c1 = pyfluka.bodies.PLA("c1", [-0.0, 8.304547985374, 99.654575824488,
                               0.0, 0.0, 100.0])
c2 = pyfluka.bodies.PLA("c2", [-0.0, 7.6696498884737, 99.705448550158,
                               0.0, 10.0, -160.0])

scale = 1e6
# Automatic scaling of infinite bodies is handled in the Zone class,
# but here we hard code it to test the binary operations:
b = a1(scale) + b1(scale) + c1(scale) - a2(scale) - b2(scale) - c2(scale)
# b.view(setclip=True)

cube = pyfluka.bodies.Zone(('+', a1), ('+', b1), ('+', c1),
                           ('-', a2), ('-', b2), ('-', c2))
# cube.gdml_solid().view()
