#ifndef VERTEX_H
#define VERTEX_H

#include "Vector.h"

class Vertex {
 public:
  Vertex(const Vector& pos, const Vector& norm);
  Vertex(const Vertex& rhs);
  //Vertex clone();
  //void flip();
  //void interpolate(const Vertex& other, double t); 

 private:
  Vector _pos;
  Vector _normal;
};

#endif
