#ifndef VERTEX_H
#define VERTEX_H

class Vertex {
 public:
  Vertex(const vector& pos, const vector& norm);
  Vertex(const Vertex& rhs);
  void flip();
  void interpolate(const Vertex& other, double t); 
};


#endif
