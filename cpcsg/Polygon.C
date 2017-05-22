#include "Polygon.h"

Polygon::Polygon(const vector<Vertex>& _vertices, void* _shared){
  vertices = _vertices;
  shared = _shared;
  plane = Plane::fromPoints(vertices[0].pos,vertices[1].pos,vertices[2].pos);
}

unsigned int Polygon::size(){
  return vertices.size();
}

Vertex Polygon::operator[](int i){
  return vertices[i];
}

Polygon Polygon::clone(){
  vector<Vertex> vclone;
  for(unsigned i = 0;i<vertices.size();i++){
    vclone.push_back(vertices[i].clone());
  }
  return Polygon(vclone,shared);
}

void Polygon::flip(){
  std::reverse(vertices.begin(),vertices.end()); 
  for(unsigned i = 0;i<vertices.size();i++){
    vertices[i] = vertices[i].flip();
  } 
  plane.flip();
}

