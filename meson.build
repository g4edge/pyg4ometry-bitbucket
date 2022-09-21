project(
  'pyg4ometry',
  'c', 'cpp',
  version: '1.0.3',
  license: 'GPL',
  meson_version: '>= 0.63.0',
  default_options: [],
)

dir_base = meson.current_source_dir()
dir_lib = join_paths(dir_base, 'lib')

cc = meson.get_compiler('c')
cpp = meson.get_compiler('cpp')

py_mod = import('python')
py3 = py_mod.find_installation()
py3_dep = py3.dependency()

cython    = find_program('cython')
oce       = dependency('OpenCASCADE', method : 'cmake', required : true)
oceLibs = '-lTKernel -lTKMath -lTKG2d -lTKG3d -lTKGeomBase -lTKBRep -lTKGeomAlgo -lTKTopAlgo -lTKPrim -lTKBO -lTKShHealing -lTKBool -lTKHLR -lTKFillet -lTKOffset -lTKFeat -lTKMesh -lTKXMesh -lTKService -lTKV3d -lTKOpenGl -lTKMeshVS -lTKCDF -lTKLCAF -lTKCAF -lTKBinL -lTKXmlL -lTKBin -lTKXml -lTKStdL -lTKStd -lTKTObj -lTKBinTObj -lTKXmlTObj -lTKVCAF -lTKXSBase -lTKSTEPBase -lTKSTEPAttr -lTKSTEP209 -lTKSTEP -lTKIGES -lTKXCAF -lTKXDEIGES -lTKXDESTEP -lTKSTL -lTKVRML -lTKXmlXCAF -lTKBinXCAF -lTKRWMesh -lTKDraw -lTKTopTest -lTKOpenGlTest -lTKViewerTest -lTKXSDRAW -lTKDCAF -lTKXDEDRAW -lTKTObjDRAW -lTKQADraw'
oceDep    = declare_dependency(compile_args : oce.get_variable('OpenCASCADE_CXX_FLAGS').split(),
	                       link_args : (oce.get_variable('OpenCASCADE_LINKER_FLAGS')+' -L'+oce.get_variable('OpenCASCADE_LIBRARY_DIR')+' '+oceLibs).split(),
			       include_directories : oce.get_variable('OpenCASCADE_INCLUDE_DIR'),
			       version : oce.get_variable('OpenCASCADE_MAJOR_VERSION')+oce.get_variable('OpenCASCADE_MINOR_VERSION')+oce.get_variable('OpenCASCADE_MAINTENANCE_VERSION'))
gmp       = cpp.find_library('gmp',required : true, dirs: '/opt/local/lib/')				
mpfr      = cpp.find_library('mpfr',required : true, dirs: '/opt/local/lib')
cgal      = dependency('CGAL', method : 'cmake', required : true)
boost = dependency('boost')
pybind11  = dependency('pybind11',method : 'cmake', required : true)

subdir('src/pyg4ometry/pycsg')
subdir('src/pyg4ometry/pycgal')
subdir('src/pyg4ometry/pyoce')






