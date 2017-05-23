#include "Solids.h"

CSG* Solids::Box(double dx, double dy, double dz) {
  std::vector<Polygon*> polygons;

  Vertex v1 = Vertex(Vector(-1,-1,-1));
  Vertex v2 = Vertex(Vector(-1, 1,-1));
  Vertex v3 = Vertex(Vector( 1, 1,-1));
  Vertex v4 = Vertex(Vector( 1,-1,-1));

  Vertex v5 = Vertex(Vector(-1,-1, 1));
  Vertex v6 = Vertex(Vector(-1, 1, 1));
  Vertex v7 = Vertex(Vector( 1, 1, 1));
  Vertex v8 = Vertex(Vector( 1,-1, 1));
  
  std::vector<Vertex> f1;
  f1.push_back(v1);
  f1.push_back(v2);
  f1.push_back(v3);
  f1.push_back(v4);

  std::vector<Vertex> f2;
  f2.push_back(v5);
  f2.push_back(v6);
  f2.push_back(v7);
  f2.push_back(v8);

  std::vector<Vertex> f3;
  f3.push_back(v1);
  f3.push_back(v5);
  f3.push_back(v8);
  f3.push_back(v4);

  Polygon *p1 = new Polygon(f1,NULL);
  Polygon *p2 = new Polygon(f2,NULL);
  Polygon *p3 = new Polygon(f3,NULL);

  std::vector<Polygon*> p;
  p.push_back(p1);
  p.push_back(p2);
  p.push_back(p3);
  return CSG::fromPolygons(p);
}
