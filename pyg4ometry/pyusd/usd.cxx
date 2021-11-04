#include "usd.h"

Stage::Stage() {
  py::print("Stage::Stage>");
  stage = pxr::UsdStage::CreateInMemory();
}

void Stage::Export(py::str exportFileName) {
  py::print("Stage::Export>",exportFileName);
  stage->Export(exportFileName);
}

GeomMesh::GeomMesh(Stage *stage) {
  pxr::VtArray<int> faceVertexCounts = {4};
  pxr::VtArray<int> faceVertexIndices = {0,1,2,3};
  pxr::VtArray<pxr::GfVec3f> points ={ pxr::GfVec3f(0.0f, 0.0f,0.0f),
                                       pxr::GfVec3f(1.0f, 0.0f,0.0f),
                                       pxr::GfVec3f(1.0f, 1.0f,0.0f),
                                       pxr::GfVec3f(0.0f, 1.0f,0.0f)};
  pxr::UsdGeomMesh mesh = pxr::UsdGeomMesh::Define(stage->getStage(), pxr::SdfPath("/mesh"));

  mesh.CreateFaceVertexCountsAttr().Set(faceVertexCounts, 0.0);
  mesh.CreateFaceVertexIndicesAttr().Set(faceVertexIndices, 0.0);
  mesh.CreatePointsAttr().Set(points,0.0);


  auto convertableAttribute = mesh.GetPrim().CreateAttribute(pxr::TfToken("myAttrib"),  pxr::SdfValueTypeNames->Float);
  convertableAttribute.Set(1.23f, 0.0f);
  
  auto unconvertableAttribute = mesh.GetPrim().CreateAttribute(pxr::TfToken("myAttrib2"),  pxr::SdfValueTypeNames->Float);
  unconvertableAttribute.Set(3.45f, 0.0f);
}

GeomMesh::GeomMesh(CSG *csg, Stage *stage) {
  SurfaceMesh &sm = csg->getSurfaceMesh();
  pxr::VtArray<int> faceVertexCounts;
  pxr::VtArray<int> faceVertexIndices;
  pxr::VtArray<pxr::GfVec3f> points;

  pxr::UsdGeomMesh mesh = pxr::UsdGeomMesh::Define(stage->getStage(), pxr::SdfPath("/mesh"));
  
}

/*********************************************
PYBIND
*********************************************/
PYBIND11_MODULE(usd, m) {
  py::class_<Stage>(m,"Stage")
    .def(py::init<>())
    .def("Export",(void (Stage::*)(py::str &)) &Stage::Export);

  py::class_<GeomMesh>(m,"GeomMesh")
    .def(py::init<Stage *>())
    .def(py::init<CSG *, Stage *>());
}
