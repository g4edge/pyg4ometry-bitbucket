#ifndef POLYGON_H
#define POLYGON_H
#include <vector>

#include "Vector.h"
#include "Vertex.h"

class Polygon{
  public:
    Polygon(const vector<Vertex>& _vertices, void* _shared);
    Polygon clone();
    void flip();
    size();
    Vertex operator [](int i);
  private:
    vector<Vertex> vertices;
    Plane plane;
    void* shared;
};


#endif
