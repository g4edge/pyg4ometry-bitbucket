#include "Vertex.h"

Vertex::Vertex(){
  pos = Vector();
  norm = Vector();
  hasNorm = false;
}

Vertex::Vertex(const Vector& _pos){
  pos = Vector(_pos);
  norm = Vector();
  hasNorm = false;
}

Vertex::Vertex(const Vector& _pos, const Vector& _norm){
  pos = Vector(_pos);
  norm = Vector(_norm);
  hasNorm = true;
}

Vector Vertex::position(){
  return pos;
}

void Vertex::position(Vector _pos){
  pos = _pos;
}

Vector Vertex::normal(){
  return norm;
}

void Vertex::normal(Vector _norm){
  norm = _norm;
  if(!hasNorm) hasNorm = true;
}

bool Vertex::HasNorm(){
  return hasNorm;
}

Vertex::Vertex(const Vertex& rhs){
  pos = rhs.pos;
  norm = rhs.norm;
  hasNorm = rhs.hasNorm;
}

Vertex Vertex::clone(){
  if(hasNorm){
    return Vertex(pos,norm);
  }
  else{
    return Vertex(pos);
  }
}

void Vertex::flip(){
  norm = norm.negated(); 
}

Vertex Vertex::interpolate(const Vertex& other, double t){
  return Vertex(pos.lerp(other.pos,t),norm.lerp(other.norm,t));
}
