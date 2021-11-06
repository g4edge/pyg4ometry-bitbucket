#include "usd.h"

#include "algo.h"

bool UsdExporterFlat::debug = false;

UsdExporterFlat::UsdExporterFlat() {
  if(debug)
    py::print("UsdExporterFlat::UsdExporter>");
  
  stage = pxr::UsdStage::CreateInMemory();
}

UsdExporterFlat::~UsdExporterFlat() {
  if(debug)
    py::print("UsdExporterFlat::~UsdExporter>");
}

void UsdExporterFlat::AddCGALMesh(std::string name, CSG *csg) {
  SurfaceMesh &sm = csg->getSurfaceMesh();
  
  std::string pxrPath = "/"+name;
  
  pxr::VtArray<int> faceVertexCounts;
  pxr::VtArray<int> faceVertexIndices;
  pxr::VtArray<pxr::GfVec3f> points;
  pxr::UsdGeomMesh mesh = pxr::UsdGeomMesh::Define(stage, pxr::SdfPath(pxrPath));
  
  int nFaces    = sm.number_of_faces();
  int nVertices = sm.number_of_vertices();
  
  if(debug)
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
  
  /////////////////////////////
  // Add mesh to map
  /////////////////////////////
  meshes.insert(std::pair<std::string,pxr::UsdGeomMesh>(name,mesh));
  
}

void UsdExporterFlat::AddMeshInstance(std::string name, std::vector<double> pos) {
  if(debug)
    py::print("UsdExporterFlat::AddMeshInstance>",name, pos[0],pos[1],pos[2]);

  if (meshes.find(name) == meshes.end()) {
    py::print("UsdExporter::AddMeshInstance> Mesh not defined");
    return;
  }
  
  if (instancePositions.find(name) == instancePositions.end()) {
    pxr::VtArray<pxr::GfVec3f> points;// = new pxr::VtArray<pxr::GfVec3f>();
    points.push_back(pxr::GfVec3f(pos[0], pos[1], pos[2]));
    instancePositions.insert(std::pair<std::string, pxr::VtArray<pxr::GfVec3f>>(name, points));
  }
  else {
    instancePositions[name].push_back(pxr::GfVec3f(pos[0], pos[1], pos[2]));
  }
}

void UsdExporterFlat::Export(std::string exportFileName) {
  if(debug)
    py::print("UsdExporterFlat::Export>");

  this->Complete();
  stage->Export(exportFileName);
}

void UsdExporterFlat::Complete() {
  if(debug)
    py::print("UsdExporterFlat::Complete>");

  for(auto pointPair : instancePositions) {
    std::string pxrPath = "/"+pointPair.first+"_instances";
    pxr::UsdGeomPointInstancer pointInstancer = pxr::UsdGeomPointInstancer::Define(stage, pxr::SdfPath(pxrPath));
    pointInstancers.insert(std::pair<std::string, pxr::UsdGeomPointInstancer>(pointPair.first, pointInstancer));
    pointInstancer.CreatePositionsAttr().Set(pointPair.second,0.0);

    // IMPORTANT : need to add protoindices
    pxr::VtArray<int> pi;
    for(int i=0;i<pointPair.second.size();i++) {
       pi.push_back(0);
    }
    pointInstancer.CreateProtoIndicesAttr().Set(pi);

    // IMPORTANT : set relationship between pointInstancer and meshes
    pxr::UsdRelationship rel = pointInstancer.CreatePrototypesRel();
    rel.AddTarget(pxr::SdfPath("/"+pointPair.first));
  }
}

void UsdExporterFlat::DebugPrint() {
  py::print("UsdExporterFlat::DebugPrint>");
  py::print("meshes ",meshes.size());
  py::print("instancers ",pointInstancers.size());

  pxr::VtArray<pxr::GfVec3f> points;
  for(auto pointInstancer : pointInstancers) {
    pointInstancer.second.GetPositionsAttr().Get(&points,0);
    py::print("instances ", pointInstancer.first, points.size());
    for(auto p : points) {
      py::print(p[0],p[1],p[2]);
    }
  }
}

/*********************************************
PYBIND
*********************************************/
PYBIND11_MODULE(usd, m) {
  
  py::class_<UsdExporterFlat>(m,"UsdExporterFlat")
    .def(py::init<>())
    .def_readwrite_static("debug",&UsdExporterFlat::debug)
    .def("AddCGALMesh", &UsdExporterFlat::AddCGALMesh)
    .def("AddMeshInstance", &UsdExporterFlat::AddMeshInstance)
    .def("Export", &UsdExporterFlat::Export)
    .def("Complete", &UsdExporterFlat::Complete)
    .def("DebugPrint", &UsdExporterFlat::DebugPrint);
}
