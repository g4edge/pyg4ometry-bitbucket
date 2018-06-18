# import pyg4ometry.fluka
import pyfluka
import os.path

this_dir_path = os.path.dirname(os.path.abspath(__file__))
path = ("{}/test_input_old/tunnel_cross_section/10.inp".format(this_dir_path))

m = pyfluka.Model(path)
# m.view()
m.write_to_gdml()
# from IPython import embed; embed()
