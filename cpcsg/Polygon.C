#include "Polygon.h"
#include "Plane.h"

Polygon::Polygon(const std::vector<Vertex>& _vertices, void* _shared){
  vertices = _vertices;
  shared = _shared;
  plane = Plane::fromPoints(vertices[0].position(),vertices[1].position(),vertices[2].position());
}

unsigned int Polygon::size(){
  return vertices.size();
}

Vertex Polygon::operator[](int i){
  return vertices[i];
}

Polygon* Polygon::clone(){
  std::vector<Vertex> vclone;
  for(unsigned i = 0;i<vertices.size();i++){
    vclone.push_back(vertices[i].clone());
  }
  return new Polygon(vclone,shared);
}

void Polygon::flip(){
  std::reverse(vertices.begin(),vertices.end()); 
  for(unsigned i = 0;i<vertices.size();i++){
    vertices[i].flip();
  } 
  plane->flip();
}

