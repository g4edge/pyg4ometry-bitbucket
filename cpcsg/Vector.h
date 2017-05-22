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
  Vector  negated() const;
  Vector  plus(const Vector &rhs) const;
  Vector  operator+(const Vector &rhs) const;
  Vector  minus(const Vector &rhs) const;
  Vector  operator-(const Vector &rhs) const;
  Vector  times(double a) const;
  Vector  operator*(double a) const;
  Vector  divideBy(double a) const ;
  Vector  operator/(double a) const;
  double  dot(const Vector &rhs) const;
  Vector  scale(const Vector &rhs) const;
  Vector  lerp(const Vector &rhs, double t) const;
  double  length() const;
  Vector  unit() const;
  Vector  cross(const Vector &rhs) const;
  double& operator[](int i);
  double  operator[](int i) const;

private:
  double _x,_y,_z;
  
  /*
  */
};

std::ostream& operator<<(std::ostream &ostr, const Vector &rhs);
Vector operator*(double a, const Vector &rhs);

#endif
