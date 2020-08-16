from setuptools import find_packages
from distutils.command import build_ext
from distutils.core import setup, Extension
from Cython.Build import cythonize

exts = cythonize(["pyg4ometry/pycsg/geom.pyx", "pyg4ometry/pycsg/core.pyx"])

plat = build_ext.get_platform()+'-'+build_ext.get_python_version()

pyg4_cgal_ext  = Extension('pyg4ometry.pycgal.pyg4_cgal',
                           include_dirs = ['./pyg4ometry/external/cgal-install/include/',
                                           '/opt/local/include/',
                                           '/usr/include/'],
                           libraries = ['mpfr','gmp'],
                           library_dirs = ['/opt/local/lib'],
                           sources = ['./pyg4ometry/pycgal/pyg4_cgal.cpp'],
                           language="c++",
                           extra_compile_args=["-std=c++14"])

cgal_geom_ext = Extension('pyg4ometry.pycgal.geom',
                           sources = ['./pyg4ometry/pycgal/geom.cxx'],
                           language="c++",
                           extra_compile_args=["-std=c++14","-fvisibility=hidden"])

cgal_algo_ext = Extension('pyg4ometry.pycgal.algo',
                           include_dirs = ['./pyg4ometry/external/cgal-install/include/',
                                           '/opt/local/include/',
                                           '/usr/include/'],
                           libraries = ['mpfr','gmp'],
                           library_dirs = ['/opt/local/lib'],
                           sources = ['./pyg4ometry/pycgal/algo.cxx'],
                           extra_objects=['./build/temp.'+plat+'/pyg4ometry/pycgal/geom.o'],
                           language="c++",
                           extra_compile_args=["-std=c++14","-fvisibility=hidden"])

cgal_core_ext = Extension('pyg4ometry.pycgal.core',
                           include_dirs = ['./pyg4ometry/external/cgal-install/include/',
                                           '/opt/local/include/',
                                           '/usr/include/'],
                           libraries = ['mpfr','gmp'],
                           library_dirs = ['/opt/local/lib'],
                           sources = ['./pyg4ometry/pycgal/core.cxx'],
                           extra_objects=['./build/temp.'+plat+'/pyg4ometry/pycgal/geom.o',
                                          './build/temp.'+plat+'/pyg4ometry/pycgal/algo.o'],
                           language="c++",
                           extra_compile_args=["-std=c++14","-fvisibility=hidden"])

exts.append(pyg4_cgal_ext)
exts.append(cgal_geom_ext)
exts.append(cgal_algo_ext)
exts.append(cgal_core_ext)

setup(
    name="pyg4ometry",
    version="0.9.1",
    packages=find_packages(exclude=["docs", "tests"]),
    package_dir={"pyg4ometry.convert": "pyg4ometry/convert",
                 "pyg4ometry.fluka": "pyg4ometry/fluka",
                 "pyg4ometry.geant4": "pyg4ometry/geant4",
                 "pyg4ometry.visualisation": "pyg4ometry/visualisation"},
    package_data={"pyg4ometry.convert": ["periodic-table.csv"],
                  "pyg4ometry.fluka": ["flair_template.flair"],
                  "pyg4ometry.geant4": ["bdsim_materials.txt"],
                  "pyg4ometry.visualisation": ["colours.ini"]},
    install_requires=["antlr4-python3-runtime==4.7.1",  # Generated with 4.7.1 - this avoids warnings
                      "matplotlib",
                      "pandas",
                      "networkx == 2.2",
                      "numpy",
                      "vtk",
                      "cython",
                      "GitPython",
                      "configparser",
                      "testtools",
                      "pypandoc",
                      "ipython",
                      "sympy"],
    ext_modules=exts,
    python_requires=">=3.7.1",
    author="Stewart T. Boogert",
    author_email="stewart.boogert@rhul.ac.uk",
    description='Geometry package for high energy physics (Geant4, Fluka)',
    license='GPL3',
    url='https://bitbucket.org/jairhul/pyg4ometry/',
    keywords='geometry bdsim particle physics accelerators',
)
