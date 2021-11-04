#ifndef __USD_H
#define __USD_H

#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "pxr/usd/usd/stage.h"
#include "pxr/usd/usdGeom/mesh.h"

#include "core.h"

namespace py = pybind11;

class Stage {
private:
  pxr::UsdStageRefPtr stage;

public :
  Stage();
  void Export(py::str exportFileName);
  pxr::UsdStageRefPtr getStage() {return stage;}
};

class GeomMesh {
private:
  pxr::VtArray<int> faceVertexCounts;
  pxr::VtArray<int> faceVertexIndices;
  pxr::VtArray<pxr::GfVec3f> points;
  pxr::UsdGeomMesh mesh;

public:
  GeomMesh(Stage *);
  GeomMesh(CSG *, Stage *);
};

#endif

