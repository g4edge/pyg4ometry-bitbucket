#include "Vector.h"
#include "Solids.h"
#include "CSG.h"
#include "stdlib.h"
#include <iostream>

using namespace std;

int main() {
  cin.ignore();
  double x = 200.;
  double y = 200.;
  double z = 10.;
  CSG *b = Solids::Box(x,y,z);
  double epsilon = 0.1;

  CSG *sub_cub = Solids::Box(x-epsilon,z-epsilon,z);
  sub_cub->translate(new Vector(0.0,-50.0/*(z/2.)-(y/2.)-20*/,epsilon));
  Vector* v = new Vector(0.0,20.0,0.0);
  for(int i=0;i<5;i++){
    sub_cub->translate(v);
    b = b->Subtract(sub_cub);
  }
  sub_cub = Solids::Box(z-epsilon,y-epsilon,z);

  sub_cub->translate(new Vector(-50.0/*(z/2.)-(x/2.)-20*/,0.0,epsilon));
  for(int i=0;i<5;i++){
    Vector* v = new Vector(20.0,0.0,0.0);
    sub_cub->translate(v);
    b = b->Subtract(sub_cub); 
  }
  
  b->saveVTK("b.vtk");
}
