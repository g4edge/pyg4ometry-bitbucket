import os.path

import pyg4ometry.fluka as fluka


_TEST_DIR = os.path.dirname(__file__)
_TEST_INP = os.path.join(_TEST_DIR, "cylinder.inp")

def test_read(vis=False):
    reader = fluka.Reader(_TEST_INP)
    bodies = reader.fluka_model.bodies
    cylinder = bodies["cyl"]

def test_write(vis=False):
    pass

if __name__ == '__main__':
    test_read(vis=True)
