#ifndef CSG_H
#define CSG_H

#include "Vector.h"
#include "Vertex.h"
#include "Plane.h"
#include "Polygon.h"
#include "BSPNode.h"

#include <vector>
#include <string>

struct VertsAndPolys;

struct VertsAndPolys{
  std::vector<Vertex> verts;
  std::vector<std::vector<unsigned> > polys;
  int count;
};

class CSG{
  public:
    CSG();
    ~CSG();
    static CSG* fromPolygons(std::vector<Polygon*> _polygons); 
    CSG* clone(); 
    std::vector<Polygon*> toPolygons();
    CSG* refine();
    void translate(Vector disp);
    void scale(Vector scale);
    void rotate(Vector axis,double angleDeg);
    VertsAndPolys toVerticesAndPolygons();
    void saveVTK(std::string filename);
    CSG* Union(CSG* csg);
    CSG* operator+(CSG* csg);
    CSG* Subtract(CSG* csg);
    CSG* operator-(CSG* csg);
    CSG* Intersect(CSG* csg);
    CSG* operator*(CSG* csg);
    CSG* Inverse();

 /*   static CSG* cube();
    static CSG* sphere();
    static CSG* cylinder();
    static CSG* cone();*/
  
  private:
    std::vector<Polygon*> polygons;
    Vector newVector(Vector v,Vector axis,double angleDeg);
};

#endif
