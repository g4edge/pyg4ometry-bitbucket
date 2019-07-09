import pyg4ometry.geant4 as g4
import pyg4ometry.fluka as fluka

import pyg4ometry


def test_read(vis=False):
    reader = fluka.Reader("cone.inp")
    bodies = reader.fluka_model.bodies
    cone = bodies["cone"]

def test_write(vis=False):
    pass

if __name__ == '__main__':
    test_read(vis=True)
