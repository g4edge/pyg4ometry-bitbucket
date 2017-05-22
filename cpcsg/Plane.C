#include "Plane.h"
#include "Polygon.h"

Plane::Plane(const Vector& _normal, double _w){
  normal = _normal;
  w = _w;
}

Plane::Plane(const Plane& plane){
  normal = plane.normal;
  w = plane.w;
}


Plane *Plane::fromPoints(const Vector& a, const Vector& b, const Vector& c){
  Vector n = Vector((b.minus(a)).cross(c.minus(a)).unit());
  return new Plane(n,n.dot(a));
}

void Plane::flip(){
  normal = normal.negated();
  w = -w;
}

void Plane::splitPolygon(Polygon& polygon, 
		    std::vector<Polygon> &coplanarFront, 
		    std::vector<Polygon> &coplanarBack,
		    std::vector<Polygon> &front,
		    std::vector<Polygon> &back){
  
  PolyType polygonType = COPLANAR;
  std::vector<PolyType> vertexLocs;
  
  unsigned int numVertices = polygon.size();

  for(unsigned i = 0; i < numVertices; i++){
    double t = normal.dot(polygon.vertices[i].pos) - w;
    PolyType loctype = INIT;
    if(t < -EPSILON){
      loctype = BACK;
    }
    else if(t > EPSILON){
      loctype = FRONT;
    }
    else{
      loctype = COPLANAR;
    }
    polygonType = PolyType((int) polygonType | (int) loctype);
    vertexLocs.push_back(loctype);
  }


  if(polygonType == COPLANAR){
    double normalDotPlaneNormal = normal.dot((polygon.plane)->normal);
    if(normalDotPlaneNormal > 0){
      coplanarFront.push_back(polygon);
    }
    else{
      coplanarBack.push_back(polygon);
    }
  }
  else if(polygonType == FRONT){
    front.push_back(polygon);
  }
  else if(polygonType == BACK){
    back.push_back(polygon);
  }
  else if(polygonType == SPANNING){
    std::vector<Vertex> f;
    std::vector<Vertex> b;
    for(unsigned i = 0;i < numVertices;i++){
      unsigned j = (i+1) % numVertices;
      PolyType ti = vertexLocs[i];
      PolyType tj = vertexLocs[j];
      Vertex vi = polygon.vertices[i];
      Vertex vj = polygon.vertices[j];
      if(ti != BACK){
        f.push_back(vi);
      }
      if(ti != FRONT){
        if(ti != BACK){
          b.push_back(vi.clone());
        }
        else{
          b.push_back(vi);
        }
      }
      if(((int) ti | (int) tj) == SPANNING){
        double t = (w - normal.dot(vi.pos)) / normal.dot((vj.pos).minus(vi.pos));
        Vertex v = vi.interpolate(vj,t);
        f.push_back(v);
        b.push_back(v.clone());
      }
      if(f.size() >= 3){
        front.push_back(Polygon(f,polygon.shared));
      }
      if(b.size() >=3){
        back.push_back(Polygon(b,polygon.shared));
      }

    }
  }
}


