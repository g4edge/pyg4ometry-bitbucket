#ifndef VECTOR_H
#define VECTOR_H

class Vector {
 public:
  Vector(double x, double y, double z);
  Vector(vector &v)
  ~Vector();
  
  vector  clone();
  vector  plus(const vector &rhs);
  vector  operator+(const vector &rhs);
  vector  minus(const vector &rhs);
  vector  operator-(const vector &rhs);
  vector  times(double a);
  vector  operator*(double a);
  vector  divideBy(double a);
  vector  operator/(double a);
  double  dot(cont vector &rhs);
  vector  scale(const vector &rhs);
  vector  lerp(const vector &rhs, double t);
  vector  unit();
  vector  cross(const vector &rhs);
  double& operator[](int i);
};

#endif
