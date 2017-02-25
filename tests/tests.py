import pyfluka
import sys
from IPython import embed

def visiting(argv = None):
    '''
    A test for visiting a file.
    '''

    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file="/tests/fluka_test_input.inp"


    model = pyfluka.Model.Model("/Users/Stuart/Physics/Packages"
                                "/python-tools/pyfluka/" + file)

if __name__ == '__main__':
    visiting(sys.argv)
