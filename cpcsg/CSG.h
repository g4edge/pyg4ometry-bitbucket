#ifndef CSG_H
#define CSG_H

#include "Vector.h"
#include "Vertex.h"
#include "Plane.h"
#include "Polygon.h"
#include "BSPNode.h"

#include <vector>
#include <string>

class CSG{
  public:
    CSG();
    ~CSG();
    static CSG* fromPolygons(std::vector<Polygon*> _polygons); 
    CSG* clone(); 
    std::vector<Polygon*> toPolygons();
    CSG* refine();
    void translate(double disp);
    void scale(double scale);
    void rotate(Vector* axis,double angleDeg);
    struct VertsAndPolys;
    VertsAndPolys toVerticesAndPolygons();
    void saveVTK(std::string filename);
    CSG* union(CSG* csg);
    CSG* operator+(CSG* csg);
    CSG* subtract(CSG* csg);
    CSG* operator-(CSG* csg);
    CSG* intersect(CSG* csg);
    CSG* operator*(CSG* csg);
    CSG* inverse();

    static CSG* cube();
    static CSG* sphere();
    static CSG* cylinder();
    static CSG* cone();
  
  private:
    std::vector<Polygon*> polygons;
};

#endif
