#ifndef PLANE_H
#define PLANE_H

class Plane {
 public:
  const double EPSILON= 1.e-5;
  Plane(const Vector& normal, double w);
  Plane(const Plane& plane); 
  static Plane& fromPoints(const Vector& a, const Vector& b, const Vector& c);
  void flip(); 
  void splitPolygon(std::vector<Vertex>& polygon, 
		    std::vector<Polygon> *coplanarFront, 
		    std::vector<Polygon> *coplanarBack,
		    std::vector<Polygon> *front;
		    std::vector<Polygon> *back;
}

#endif
