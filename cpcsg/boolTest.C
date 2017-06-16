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
  //CSG *b = Solids::Box(x,y,z);
  CSG *b = Solids::Cone(100,50,32);
  b->translate(new Vector(0.0,0.0,-20.0));
  double epsilon = 0.1;

  /*CSG *sub_cub = Solids::Box(x-epsilon,z-epsilon,z);
  sub_cub->translate(new Vector(0.0,-100.0,epsilon));
  for(int i=0;i<20;i++){
    Vector* v = new Vector(0.0,10.0,0.0);
    b = b->Subtract(sub_cub);
    sub_cub->translate(v);
  }
  sub_cub = Solids::Box(z-epsilon,y-epsilon,z);

  sub_cub->translate(new Vector(-100.0,0.0,epsilon));
  for(int i=0;i<20;i++){
    Vector* v = new Vector(10.0,0.0,0.0);
    b = b->Subtract(sub_cub); 
    sub_cub->translate(v);
  }*/

  CSG* sphere = Solids::Sphere(50);

  b = b->Union(sphere);
  //b->refine(); 
  b->saveVTK("b.vtk");
  sphere->saveVTK("sphere.vtk");
}
