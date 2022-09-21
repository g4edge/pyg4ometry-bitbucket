import sys

import setuptools 
from setuptools import find_packages
from Cython.Build import cythonize
from distutils.command import build_ext
from distutils.core import setup, Extension


cgalExtensions = {'geom':['geom.cxx'],
                  'algo':['algo.cxx'],
                  'core':['core.cxx']}

oceExtensions = {'pyg4ometry.pyoce.TCollection':['src/pyg4ometry/pyoce/TCollection.cxx'],
                 'pyg4ometry.pyoce.TKernel':['src/pyg4ometry/pyoce/TKernel.cxx'],
                 'pyg4ometry.pyoce.TDocStd':['src/pyg4ometry/pyoce/TDocStd.cxx'],
                 'pyg4ometry.pyoce.TDataStd':['src/pyg4ometry/pyoce/TDataStd.cxx'],
                 'pyg4ometry.pyoce.TNaming':['src/pyg4ometry/pyoce/TNaming.cxx'],
                 'pyg4ometry.pyoce.TDF':['src/pyg4ometry/pyoce/TDF.cxx'],
                 'pyg4ometry.pyoce.TopoDS':['src/pyg4ometry/pyoce/TopoDS.cxx'],
                 'pyg4ometry.pyoce.gp':['src/pyg4ometry/pyoce/gp.cxx'],
                 'pyg4ometry.pyoce.Geom':['src/pyg4ometry/pyoce/Geom.cxx'],
                 'pyg4ometry.pyoce.Poly':['src/pyg4ometry/pyoce/Poly.cxx'],
                 'pyg4ometry.pyoce.XCAFDoc':['src/pyg4ometry/pyoce/XCAFDoc.cxx'],
                 'pyg4ometry.pyoce.TopAbs':['src/pyg4ometry/pyoce/TopAbs.cxx'],
                 'pyg4ometry.pyoce.TopLoc':['src/pyg4ometry/pyoce/TopLoc.cxx'],
                 'pyg4ometry.pyoce.TopExp':['src/pyg4ometry/pyoce/TopExp.cxx'],
                 'pyg4ometry.pyoce.Message':['src/pyg4ometry/pyoce/Message.cxx'],
                 'pyg4ometry.pyoce.BRep':['src/pyg4ometry/pyoce/BRep.cxx'],
                 'pyg4ometry.pyoce.BRepMesh':['src/pyg4ometry/pyoce/BRepMesh.cxx'],
                 'pyg4ometry.pyoce.StlAPI':['src/pyg4ometry/pyoce/StlAPI.cxx'],
                 'pyg4ometry.pyoce.XCAFApp':['src/pyg4ometry/pyoce/XCAFApp.cxx'],
                 'pyg4ometry.pyoce.STEPCAFControl':['src/pyg4ometry/pyoce/STEPCAFControl.cxx']}

def cmakeDiscovery() :
    print('running cmake')
    pass

def mesonDiscovery() :
    pass
    
def pybind11CGALExtensions(extDict,depDict) :
    pass

def pybind11OCEExtensions(extDict, depDict) :

    extensions = []
    for ext in extDict :
        code = extDict[ext]
        extension = Extension(ext,
                              include_dirs = ["/opt/local/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/pybind11/include/",
                                              "/opt/local/include/opencascade/"],
                              library_dirs=['/opt/local/lib/'],
                              libraries = ['TKXCAF','TKXDESTEP','TKSTL'],
                              sources = code,
                              language="c++",
                              extra_compile_args=["-std=c++14","-fvisibility=hidden"])
        extensions.append(extension)

    return extensions
                              
    
deps = cmakeDiscovery()

csgExts  = cythonize(["src/pyg4ometry/pycsg/geom.pyx", "src/pyg4ometry/pycsg/core.pyx"])
cgalExts = pybind11CGALExtensions(cgalExtensions,deps)
oceExts  = pybind11OCEExtensions(oceExtensions,deps)

exts = []
exts.extend(csgExts)
# exts.extend(cgalExts)
exts.extend(oceExts)

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    # package_data={}, # TODO
    ext_modules=exts
)
