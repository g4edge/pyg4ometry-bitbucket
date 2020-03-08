from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="pyg4ometry",
    version="0.2.0",
    packages=find_packages(exclude=["docs", "tests"]),

    # Only tested with version 4.7.
    install_requires=["antlr4-python2-runtime == 4.7",
                      "matplotlib",
                      "networkx == 2.2",
                      "numpy",
                      "vtk",
                      "cython",
                      "GitPython",
                      "testtools"],
    # cython, pyqt5

    ext_modules=cythonize(["pyg4ometry/pycsg/geom.pyx","pyg4ometry/pycsg/core.pyx"]),

    python_requires="==2.7.*", # refer to pep440 for writing these correctly

    author="Stewart T. Boogert",
    author_email="stewart.boogert@rhul.ac.uk",
    description='Geometry package for high energy physics',
    license='GPL3',
    url='https://bitbucket.org/jairhul/pyg4ometry/',
    keywords='geometry bdsim particle physics accelerators',
)
