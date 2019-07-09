import pyg4ometry.geant4 as g4
import pyg4ometry.fluka as fluka

import pyg4ometry


def test_read(vis=False):
    reader = fluka.Reader("sphere.inp")
    sphere = reader.fluka_model.bodies["sphere"]

def test_write(vis=False):
    pass

if __name__ == '__main__':
    test_read(vis=True)
