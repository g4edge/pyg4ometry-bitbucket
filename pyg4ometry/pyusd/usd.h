#ifndef __USD_H
#define __USD_H

#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/mesh.h"
#include "pxr/usd/usdGeom/pointInstancer.h"


#include <map>
#include <string>

#include "core.h"

namespace py = pybind11;

class UsdExporterFlat {
  
private:
  pxr::UsdStageRefPtr stage;
  std::map<std::string,pxr::UsdGeomMesh> meshes;
  std::map<std::string,pxr::VtArray<pxr::GfVec3f>> instancePositions;
  std::map<std::string,pxr::UsdGeomPointInstancer> pointInstancers;
  
public:
  static bool debug;
  UsdExporterFlat();
  ~UsdExporterFlat();
  void AddCGALMesh(std::string name, CSG *);
  void AddMeshInstance(std::string name, std::vector<double> pos);
  void Export(std::string exportFileName);
  void Complete();
  void DebugPrint();
  
};

#endif

