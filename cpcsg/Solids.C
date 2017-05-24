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
  f1.push_back(v6);
  f1.push_back(v5);

  std::vector<Vertex> f2;
  f2.push_back(v1);
  f2.push_back(v4);
  f2.push_back(v8);
  f2.push_back(v5);

  std::vector<Vertex> f3;
  f3.push_back(v1);
  f3.push_back(v2);
  f3.push_back(v3);
  f3.push_back(v4);

  std::vector<Vertex> f4;
  f4.push_back(v3);
  f4.push_back(v4);
  f4.push_back(v8);
  f4.push_back(v7);

  std::vector<Vertex> f5;
  f5.push_back(v2);
  f5.push_back(v3);
  f5.push_back(v7);
  f5.push_back(v6);

  std::vector<Vertex> f6;
  f6.push_back(v5);
  f6.push_back(v6);
  f6.push_back(v7);
  f6.push_back(v8);

  Polygon *p1 = new Polygon(f1,NULL);
  Polygon *p2 = new Polygon(f2,NULL);
  Polygon *p3 = new Polygon(f3,NULL);
  Polygon *p4 = new Polygon(f4,NULL);
  Polygon *p5 = new Polygon(f5,NULL);
  Polygon *p6 = new Polygon(f6,NULL);

  std::vector<Polygon*> p;
  p.push_back(p1);
  p.push_back(p2);
  p.push_back(p3);
  p.push_back(p4);
  p.push_back(p5);
  p.push_back(p6);
  return CSG::fromPolygons(p);
}
