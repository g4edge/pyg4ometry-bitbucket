import os as _os
import unittest as _unittest

import pyg4ometry
import pandas as pd


def localPath(filename):
    """
    Append the absolute path to *this* directory to the filename so the tests
    can be ran from anywhere
    """
    return _os.path.join(_os.path.dirname(__file__), filename)


def localFile(filename):
    return _os.path.join(_os.path.dirname(__file__), filename)


def exportToVTKTest():
    e = pyg4ometry.visualisation.VtkExporter(localPath('./'))

    reader = pyg4ometry.gdml.Reader(localFile('model.gdml'))
    reg = reader.getRegistry()

    # Paraview export of a model -> each daughter volume of the GDML world volume will have its own .vtm file.

    df_model = pd.read_csv(localFile("df_model.csv"))
    df_color = pd.read_csv(localFile("color_elements.csv"))

    e.export_to_VTK(reg, model=True, df_model=df_model.copy(), df_color=df_color.copy())
    e.export_to_VTK(reg, model=True)

    # Paraview export of a GDML -> the whole GDML will have one .vtm file.

    e.export_to_VTK(reg, model=False, df_model=df_model.copy(), df_color=df_color.copy())
    e.export_to_VTK(reg, model=False)


def exportToParaview():
    e = pyg4ometry.visualisation.VtkExporter(localPath('./'))

    reader = pyg4ometry.gdml.Reader(localFile('model.gdml'))
    reg = reader.getRegistry()

    # Paraview export of a model -> each daughter volume of the GDML world volume will have its own .vtm file.

    df_model = pd.read_csv(localFile("df_model.csv"))
    df_color = pd.read_csv(localFile("color_elements.csv"))

    e.export_to_Paraview(reg, fileName='Paraview_model_user.pvsm', model=True, df_model=df_model.copy(), df_color=df_color.copy())
    e.export_to_Paraview(reg, fileName='Paraview_model_material.pvsm', model=True)

    # Paraview export of a GDML -> the whole GDML will have one .vtm file.

    e.export_to_Paraview(reg, fileName='Paraview_gdml_user.pvsm', model=False, df_model=df_model.copy(), df_color=df_color.copy())
    e.export_to_Paraview(reg, fileName='Paraview_gdml_material.pvsm', model=False)


class VtkExporter(_unittest.TestCase):
    def test_vtkExporter(self):
        exportToVTKTest()
        exportToParaview()


if __name__ == '__main__':
    _unittest.main(verbosity=2)
