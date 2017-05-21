/* File : example.i */
%module Vector

%{
#include "Vector.h"
%}

/* Let's just grab the original header file here */
%include "Vector.h"

%extend Vector {
  char*   __str__() const {
    static char tmp[1024];
    sprintf(tmp,"Vector(%g,%g,%g)", $self->x(),$self->y(),$self->z());
    return tmp;    
  }

  char*   __repr__() const {
    static char tmp[1024];
    sprintf(tmp,"Vector(%g,%g,%g)", $self->x(),$self->y(),$self->z());
    return tmp;    
  }
};

%rename(Vector_add_dc) operator*(double a, const Vector &);