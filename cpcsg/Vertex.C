#include "Vertex.h"

Vertex::Vertex(){
  pos = Vertex(0.0,0.0,0.0);
  norm = Vertex(0.0,0.0,1.0);
}

Vertex::Vertex(const Vector& _pos, const Vector& _norm){
  pos = Vertex(_pos);
  norm = Vertex(_norm);
}

Vertex::Vertex(const Vertex& rhs){
  pos = rhs.pos;
  norm = rhs.norm;
}

Vertex Vertex::clone(){
  return Vertex(pos,norm);
}

void Vertex::flip(){
  norm = norm.negated(); 
}

Vertex Vertex::interpolate(const Vertex& other, double t){
  return Vertex(pos.lerp(other.pos,t),norm.lerp(other.norm,t));
}
