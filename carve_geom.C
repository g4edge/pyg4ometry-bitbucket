#include <iostream>
#include "carve_geom.h"

// RPP, BOX
carve::mesh::MeshSet<3> *makeCube(const carve::math::Matrix &transform) {
  carve::input::PolyhedronData data;

  data.addVertex(transform * carve::geom::VECTOR(+1.0, +1.0, +1.0));
  data.addVertex(transform * carve::geom::VECTOR(-1.0, +1.0, +1.0));
  data.addVertex(transform * carve::geom::VECTOR(-1.0, -1.0, +1.0));
  data.addVertex(transform * carve::geom::VECTOR(+1.0, -1.0, +1.0));
  data.addVertex(transform * carve::geom::VECTOR(+1.0, +1.0, -1.0));
  data.addVertex(transform * carve::geom::VECTOR(-1.0, +1.0, -1.0));
  data.addVertex(transform * carve::geom::VECTOR(-1.0, -1.0, -1.0));
  data.addVertex(transform * carve::geom::VECTOR(+1.0, -1.0, -1.0));

  data.addFace(0, 1, 2, 3);
  data.addFace(7, 6, 5, 4);
  data.addFace(0, 4, 5, 1);
  data.addFace(1, 5, 6, 2);
  data.addFace(2, 6, 7, 3);
  data.addFace(3, 7, 4, 0);

  return new carve::mesh::MeshSet<3>(data.points, data.getFaceCount(), data.faceIndices);
}

// RCC REC XCC YCC ZCC XEC YEC ZEC
carve::mesh::MeshSet<3> *makeCylinder(int iSlices,
				      double dRadius,
				      double dHeight,
				      const carve::math::Matrix &transform) { 
  carve::input::PolyhedronData data;
  data.reserveVertices(iSlices * 2 + 2);

  data.addVertex(transform * carve::geom::VECTOR(0, 0, +dHeight/2));
  data.addVertex(transform * carve::geom::VECTOR(0, 0, -dHeight/2));  

  for (int i = 0; i < iSlices; i++) {
    double a1 = i * M_PI * 2.0 / iSlices;
    double y = cos(a1) * dRadius;
    double x = sin(a1) * dRadius;
    data.addVertex(transform * carve::geom::VECTOR(x, y, +dHeight/2));
    data.addVertex(transform * carve::geom::VECTOR(x, y, -dHeight/2));
  }
  
  data.reserveFaces(iSlices * 3, 4);
  for (int i = 0; i < iSlices; i++) {
    data.addFace(0,
                 2 + ((i+1) % iSlices) * 2,
                 2 + i * 2);
  }
  for (int i = 0; i < iSlices; i++) {
    data.addFace(2 + i * 2,
                 2 + ((i+1) % iSlices) * 2,
                 3 + ((i+1) % iSlices) * 2,
                 3 + i * 2);
  }
  for (int i = 0; i < iSlices; i++) {
    data.addFace(1,
                 3 + i * 2,
                 3 + ((i+1) % iSlices) * 2);
  }

  return data.createMesh(carve::input::opts());  
}

// TRC
carve::mesh::MeshSet<3> *makeTruncatedCone(const carve::math::Matrix &transform) {
  carve::input::PolyhedronData data; 
  return data.createMesh(carve::input::opts());
}

// SPH
carve::mesh::MeshSet<3> *makeSphere(int iLat, int iLong, const carve::math::Matrix &transform) {
  carve::input::PolyhedronData data;

  int nVert = 0;

  double dTheta = M_PI/(double)iLat;
  double dPhi   = 2*M_PI/(double)iLong;

  data.addVertex(transform * carve::geom::VECTOR( 0.0,  1.0, 0.0));
  data.addVertex(transform * carve::geom::VECTOR( 0.0, -1.0, 0.0));
  nVert += 2;

  int fVert = nVert;
  for(int i=1;i<iLong;i++) { 
    double rsin = 1.0 * sin((double)i*dTheta);
    double y    = 1.0 * cos((double)i*dTheta);
    for(int j=0;j<iLat;j++) { 
      double x = rsin*cos((double)j*dPhi);
      double z = rsin*sin((double)j*dPhi); 
      data.addVertex(transform * carve::geom::VECTOR(x,y,z));
      nVert++;
    }
  }

  // add top triangular faces 
  int iStart = 2;
  for(int j=0;j<iLong;j++) { 
    if(j == iLong-1) {
      data.addFace(iStart+j,0,iStart); 
    }
    else {
      data.addFace(iStart+j,0,iStart+j+1); 
    }
  }

  // add bottom triagnular faces
  iStart = 2+(iLong-2)*iLat;
  for(int j=0;j<iLong;j++) { 
    if(j == iLong-1) {
      data.addFace(1,iStart+j,iStart); 
    }
    else {
      data.addFace(1,iStart+j,iStart+j+1); 
    }
  }

  // add central triangular faces 
  for(int i=1;i<iLat-1;i++) { 
    for(int j=0;j<iLong;j++) { 
      int i1 = (i-1)*iLong+j+2;
      int i2 = (i-1)*iLong+j+1+2;
      int i3 = i*iLong+j+2;
      int i4 = i*iLong+j+1+2;
      if(j==iLong-1) { // Remember spheres are preiodic 
	i2 = (i-1)*iLong+2;
	i4 = i*iLong+2;
      }
      data.addFace(i1,i2,i3);
      data.addFace(i3,i2,i4);
    }
  }
}

// WED RAW 
carve::mesh::MeshSet<3> *makeWedge(const carve::meth::Matrix &transform) { 
  carve::input::PolyhedronData data; 
  return data.createMesh(carve::input::opts());  
}

// XYP XZP YZP PLA
carve::mesh::MeshSet<3> *makePlane(const carve::math::Matrix &transform) {
  carve::input::PolyhedronData data; 
  return data.createMesh(carve::input::opts());  
}

// ARB
carve::mesh::MeshSet<3> *makeConvexPolyhedron(const carve::math::Matrix &transform) {
  carve::input::PolyhedronData data; 
  return data.createMesh(carve::input::opts());  
}

// QUA
carve::mesh::MeshSet<3> *makeQuadric(const carve::math::Matrix &transform) { 
  carve::input::PolyhedronData data; 
  return data.createMesh(carve::input::opts());  
}
