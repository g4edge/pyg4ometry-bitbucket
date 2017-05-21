#include "Vector.h"

Vector::Vector() 
{
  _x = 0.0;
  _y = 0.0;
  _z = 0.0;
}

Vector::Vector(double xIn, double yIn, double zIn) 
{
  _x = xIn;
  _y = yIn;
  _z = zIn;
}  

Vector::Vector(const Vector &v) 
{
  _x = v._x;
  _y = v._y;
  _z = v._z;
}

Vector::~Vector() 
{
}

double Vector::x() const
{
  return _x;
}

double Vector::y() const
{
  return _y;
}

double Vector::z() const
{
  return _z;
}

Vector Vector::clone() const
{
  return Vector(_x,_y,_z);
}

Vector Vector::plus(const Vector &rhs) const
{
  return Vector(_x+rhs._x, _y+rhs._y, _z+rhs._z);
}

Vector Vector::operator+(const Vector &rhs) const
{
  return this->plus(rhs);
}

Vector Vector::minus(const Vector &rhs) const
{
  return Vector(_x-rhs._x, _y-rhs._y, _z-rhs._z);
}

Vector Vector::operator-(const Vector &rhs) const
{
  return this->minus(rhs);
}

Vector Vector::times(double a) const
{
  return Vector(a*_x, a*_y, a*_z);
}

Vector Vector::operator*(double a) const
{
  return this->times(a);
}

Vector Vector::times(float a) const
{
  return Vector((double)a*_x, (double)a*_y, (double)a*_z);
}

Vector Vector::operator*(float a) const
{
  return this->times(a);
}

Vector Vector::times(int a) const
{
  return Vector((double)a*_x, (double)a*_y, (double)a*_z);
}

Vector Vector::operator*(int a) const
{
  return this->times(a);
}

Vector operator*(double d, const Vector& rhs) 
{
  return rhs.times(d);
}

std::ostream& operator<<(std::ostream& ostr, const Vector& rhs) 
{
  ostr << rhs.x() << " " << rhs.y() << " " << rhs.z() << std::endl;
  return ostr;
}
