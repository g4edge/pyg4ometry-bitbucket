from pygdml import material as _pygdml_mat
from IPython import embed

def _process_builtin_materials(builtins):
    # Convert the dictionary fluka_g4_material_map strings to
    # pygdml.material.MaterialReference instances.
    output = dict()
    for fluka_name, gdml_material in fluka_g4_material_map.iteritems():
        if isinstance(gdml_material, basestring):
            output[fluka_name] = _pygdml_mat.MaterialReference(gdml_material)
        else:
            output[fluka_name] = gdml_material
    return output
