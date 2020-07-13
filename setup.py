from setuptools import find_packages
from distutils.core import setup, Extension
from Cython.Build import cythonize
#import os
#os.environ["CC"] = "gcc-9"
#os.environ["CXX"] = "g++-9"

class ctypes(Extension):
    pass

# might not have cython before running setup
try:
    from Cython.Build import cythonize
except ImportError:
     def cythonize(*args, **kwargs):
         from Cython.Build import cythonize
         return cythonize(*args, **kwargs)

exts = cythonize(["pyg4ometry/pycsg/geom.pyx", "pyg4ometry/pycsg/core.pyx"])
#exts.append(ctypes('pyg4ometry.pycgal.pyg4_cgal', 
#                   sources=['./pyg4ometry/pycgal/pyg4_cgal.cpp'],
#                   include_dirs = ['/opt/local/include', '/usr/local/include'],
#                   library_dirs = ['/usr/local/lib'],
#                   libraries = ['mpfr','gmp','boost_thread-mt','stdc++']))

#try:
#    import pypandoc
#    long_description = pypandoc.convert_file("README.md", "rst")
#except ImportError:
#    print ("Warning: pypandoc module not found, could not convert"
#           " Markdown to reStructuredText." )
#    long_description = ""

setup(
    name="pyg4ometry",
    version="0.9.1",
    packages=find_packages(exclude=["docs", "tests"]),
    package_dir={"pyg4ometry.visualisation": "pyg4ometry/visualisation"},
    package_data={"pyg4ometry.visualisation": ["colours.ini"]},
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
                      "ipython"],
    # pyqt5
    ext_modules=exts,
    python_requires=">=3.7.1", # refer to pep440 for writing these correctly
    author="Stewart T. Boogert",
    author_email="stewart.boogert@rhul.ac.uk",
    description='Geometry package for high energy physics (Geant4, Fluka)',
    #  longdescription=longdescription,
    license='GPL3',
    url='https://bitbucket.org/jairhul/pyg4ometry/',
    keywords='geometry bdsim particle physics accelerators',
)
