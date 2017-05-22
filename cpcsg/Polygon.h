#ifndef POLYGON_H
#define POLYGON_H
#include <vector>

#include "Vector.h"
#include "Vertex.h"

class Plane;

class Polygon{
  public:
    Polygon(const std::vector<Vertex>& _vertices, void* _shared);
    Polygon clone();
    void flip();
    unsigned int size();
    Vertex operator [](int i);
    std::vector<Vertex> vertices;
    Plane* plane;
    void* shared;
};


#endif
