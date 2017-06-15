from IPython import embed

import pyfluka
import pygdml
import os.path as _path

model_path = (_path.dirname(_path.abspath(__file__))
              + "/../ir1_tunnel/ir1_just_geometry.inp")
model = pyfluka.model.Model(model_path)
working = []
not_working = []
for name in model.region_names:
    try:
        model.view_mesh(name)
        working.append(name)
    except pygdml.NullMeshError as error:
        not_working.append((name, error.solid))
