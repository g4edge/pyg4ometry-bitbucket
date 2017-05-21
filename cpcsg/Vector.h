#ifndef VECTOR_H
#define VECTOR_H

#include <iostream>

class Vector {
 public:
  Vector();
  Vector(double x, double y, double z);
  Vector(const Vector &v);
  
  ~Vector();
  double x() const;
  double y() const;
  double z() const;

  Vector  clone() const;  
  Vector  plus(const Vector &rhs) const;
  Vector  operator+(const Vector &rhs) const;
  Vector  minus(const Vector &rhs) const;
  Vector  operator-(const Vector &rhs) const;
  Vector  times(double a) const;
  Vector  times(float a) const;
  Vector  times(int a) const;
  Vector  operator*(double a) const;
  Vector  operator*(float  a) const;
  Vector  operator*(int    a) const;

 private:
  double _x,_y,_z;
  
  /*
  vector  divideBy(double a);
  vector  operator/(double a);
  double  dot(cont vector &rhs);
  vector  scale(const vector &rhs);
  vector  lerp(const vector &rhs, double t);
  vector  unit();
  vector  cross(const vector &rhs);
  double& operator[](int i);
  */
};

std::ostream& operator<<(std::ostream &ostr, const Vector &rhs);
Vector operator*(double a, const Vector &rhs);

#endif
