from setuptools import find_packages
from distutils.command import build_ext
from distutils.core import setup, Extension
from Cython.Build import cythonize
from subprocess import run
from shutil import which
import sys

import pybind11

# https://github.com/pypa/pip/issues/7953
import site
site.ENABLE_USER_SITE = True

plat = build_ext.get_platform()+'-'+build_ext.get_python_version()

exts = cythonize(["pyg4ometry/pycsg/geom.pyx", "pyg4ometry/pycsg/core.pyx"])

# pybind11 include directory  (header only library)
pybind11_include = pybind11.get_include()

# detect python version
pythonMajorVersion = sys.version_info[0]
pythonMinorVersion = sys.version_info[1]

print("Python version : {}.{}".format(pythonMajorVersion,pythonMinorVersion))

# start with system dirs (and port/brew and default miniconda)
includeSearchDirs = ["/usr/include","/usr/local/include","/opt/local/include/","/usr/local/Cellar/include/","/opt/miniconda3/include/"]
librarySearchDirs = ["/usr/lib/","/usr/lib64/","/usr/local/lib/","/usr/local/lib64/","/usr/lib/x86_64-linux-gnu/","/opt/local/lib/","/usr/local/Cellar/lib/","/opt/miniconda3/lib/"]

# search for cgal, pybind11 (only if pybind11_include is not set), mpfr, gmp in the search dirs
def findPackage(name, searchDirs) :
    import glob
    import os.path

    path = set()
    for d in searchDirs :
        for f in glob.glob(d+"/*"+name+"*") :
            path.add(os.path.dirname(f))

    print("Found "+name,list(path))
    if len(path) == 0:
        print("Could not find "+name,path)
        return list()
    else :
        print(list(path))
        return list(path)

incPathSet = set()
libPathSet = set()

# TODO does not handle lists properly
incPath = findPackage("mpfr",includeSearchDirs); incPathSet.add(*set(incPath))
libPath = findPackage("mpfr",librarySearchDirs); libPathSet.add(*set(libPath))
incPath = findPackage("gmp",includeSearchDirs); incPathSet.add(*set(incPath))
libPath = findPackage("gmp",librarySearchDirs); libPathSet.add(*set(libPath))
# incPath = findPackage("pybind11",includeSearchDirs); incPathSet.add(*set(incPath))
incPath = findPackage("CGAL",includeSearchDirs); incPathSet.add(*set(incPath))

print("Using include paths : ",incPath)
print("Using library paths : ",libPath)

# detect conda
condaExe    = which("conda")
if condaExe is not None :
    condaDetect = run([condaExe,"-V"], capture_output=True)
    print("Found conda {}".format(condaExe))

# conda environments


pyg4_cgal_ext  = Extension('pyg4ometry.pycgal.pyg4_cgal',
                           include_dirs = [*incPath,
                                           pybind11_include],
                           libraries = ['mpfr','gmp'],
                           library_dirs = [*libPath],
                           sources = ['./pyg4ometry/pycgal/pyg4_cgal.cpp'],
                           language="c++",
                           extra_compile_args=["-std=c++14"])

cgal_geom_ext = Extension('pyg4ometry.pycgal.geom',
                          include_dirs = [*incPath,
                                          pybind11_include],
                          sources = ['./pyg4ometry/pycgal/geom.cxx'],
                          language="c++",
                          extra_compile_args=["-std=c++14","-fvisibility=hidden"])

cgal_algo_ext = Extension('pyg4ometry.pycgal.algo',
                          include_dirs = [*incPath,
                                          pybind11_include],
                          # libraries = ['mpfr','gmp'],
                          library_dirs = [*libPath],
                          sources = ['./pyg4ometry/pycgal/algo.cxx'],
                          extra_objects=['./build/temp.'+plat+'/pyg4ometry/pycgal/geom.o',
                                         '/opt/local/lib/libmpfr.a',
                                         '/opt/local/lib/libgmp.a'],
                          language="c++",
                          extra_compile_args=["-std=c++14","-fvisibility=hidden"])

cgal_core_ext = Extension('pyg4ometry.pycgal.core',
                          include_dirs = [*incPath,
                                          pybind11_include],
                           # libraries = ['mpfr','gmp'],
                           library_dirs = [*libPath],
                           sources = ['./pyg4ometry/pycgal/core.cxx'],
                           extra_objects=['./build/temp.'+plat+'/pyg4ometry/pycgal/geom.o',
                                          './build/temp.'+plat+'/pyg4ometry/pycgal/algo.o',
                                          '/opt/local/lib/libmpfr.a',
                                          '/opt/local/lib/libgmp.a'],
                           language="c++",
                           extra_compile_args=["-std=c++14","-fvisibility=hidden"])


exts.append(pyg4_cgal_ext)
exts.append(cgal_geom_ext)
exts.append(cgal_algo_ext)
exts.append(cgal_core_ext)

setup(
    name="pyg4ometry",
    version="1.0.1",
    packages=find_packages(exclude=["docs", "tests"]),
    package_dir={"pyg4ometry.convert": "pyg4ometry/convert",
                 "pyg4ometry.fluka": "pyg4ometry/fluka",
                 "pyg4ometry.geant4": "pyg4ometry/geant4",
                 "pyg4ometry.visualisation": "pyg4ometry/visualisation"},
    package_data={"pyg4ometry.convert": ["periodic-table.csv"],
                  "pyg4ometry.fluka": ["flair_template.flair"],
                  "pyg4ometry.geant4": ["nist_elements.txt","nist_materials.txt"],
                  "pyg4ometry.visualisation": ["colours.ini"]},
    install_requires=["antlr4-python3-runtime==4.7.1",  # Generated with 4.7.1 - this avoids warnings
                      "matplotlib",
                      "pandas",
                      "networkx",
                      "numpy",
                      "vtk",
                      "cython",
                      "GitPython",
                      "configparser",
                      "testtools",
                      "pypandoc",
                      "sympy>=1.7"],
    ext_modules=exts,
    python_requires=">=3.7.1",
    author="Stewart T. Boogert",
    author_email="stewart.boogert@rhul.ac.uk",
    description='Geometry package for high energy physics (Geant4, Fluka)',
    license='GPL3',
    url='https://bitbucket.org/jairhul/pyg4ometry/',
    keywords='geometry bdsim particle physics accelerators',
)
