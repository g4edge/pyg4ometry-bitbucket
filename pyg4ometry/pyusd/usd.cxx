#include "usd.h"

#include "algo.h"

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

  int nFaces    = sm.number_of_faces();
  int nVertices = sm.number_of_vertices();

  py::print("GeomMesh::GeomMesh>",nFaces,nVertices);

  Surface_mesh::Point p;

  for(Surface_mesh::Vertex_index vd : sm._surfacemesh->vertices() ) {    
    p = sm._surfacemesh->point(vd);
    points.push_back(pxr::GfVec3f(CGAL::to_double(p.x()), CGAL::to_double(p.y()), CGAL::to_double(p.z())));
  }

  for(Surface_mesh::Face_index fd : sm._surfacemesh->faces() ) {
    int iVertInFace = 0;
    for(Surface_mesh::Halfedge_index hd : CGAL::halfedges_around_face(sm._surfacemesh->halfedge(fd),
								      *(sm._surfacemesh))) {
      iVertInFace++;
      faceVertexIndices.push_back((int)sm._surfacemesh->source(hd));
    }
    faceVertexCounts.push_back(iVertInFace);
  }

  mesh.CreateFaceVertexCountsAttr().Set(faceVertexCounts, 0.0);
  mesh.CreateFaceVertexIndicesAttr().Set(faceVertexIndices, 0.0);
  mesh.CreatePointsAttr().Set(points,0.0);
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
