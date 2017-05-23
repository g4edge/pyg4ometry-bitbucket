#ifndef VERTEX_H
#define VERTEX_H

#include "Vector.h"

class Vertex {
 public:
  Vertex();
  Vertex(const Vector& _pos);
  Vertex(const Vector& _pos, const Vector& _norm);
  Vertex(const Vertex& rhs);
  
  Vertex clone();
  void flip();
  Vertex interpolate(const Vertex& other, double t); 
  Vector position();
  void position(Vector _pos);
  Vector normal();
  void normal(Vector _norm);
  bool HasNorm();
 private:
  Vector pos;
  Vector norm;
  bool hasNorm;
};

#endif
