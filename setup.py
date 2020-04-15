from setuptools import setup, find_packages
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from Cython.Build import cythonize


class ctypes(Extension): pass

exts = cythonize(["pyg4ometry/pycsg/geom.pyx","pyg4ometry/pycsg/core.pyx"])
exts.append(ctypes('pyg4ometry.pycgal.pyg4_cgal', 
                   sources=['./pyg4ometry/pycgal/pyg4_cgal.cpp'],
                   include_dirs = ['/opt/local/include'],
                   library_dirs = ['/opt/local/lib'],
                   libraries = ['CGAL','mpfr','gmp','boost_thread-mt','stdc++']))

setup(
    name="pyg4ometry",
    version="0.9.0",
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
    
    ext_modules=exts,

    python_requires="==2.7.*", # refer to pep440 for writing these correctly

    author="Stewart T. Boogert",
    author_email="stewart.boogert@rhul.ac.uk",
    description='Geometry package for high energy physics',
    license='GPL3',
    url='https://bitbucket.org/jairhul/pyg4ometry/',
    keywords='geometry bdsim particle physics accelerators',
)
