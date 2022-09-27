import pyg4ometry.fluka
import os.path

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_EXAMPLES_DIR = ("{}/test_input/examples//".format(_THIS_DIR))



def write_example_tunnel():
    path = (
        "{}/tunnel_cross_section/tunnel_part_10_of_10.inp".format(_EXAMPLES_DIR)
    )
    m = pyg4ometry.fluka.Model(path)
    m.write_to_gdml()


if __name__ == "__main__":
    write_example_tunnel()
