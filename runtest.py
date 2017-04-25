#!/usr/bin/env python
import sys
from IPython import embed
import pyfluka

def to_gdml(argv = None):
    '''
    A test for visiting a file.
    '''

    if len(sys.argv) == 2:
        inp_path = sys.argv[1]

    model = pyfluka.model.Model(inp_path, debug=True)
    model.write_to_gdml(make_gmad = True)


if __name__ == '__main__':
    to_gdml(sys.argv)
