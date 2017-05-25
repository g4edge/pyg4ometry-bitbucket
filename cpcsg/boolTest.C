#include "Vector.h"
#include "Solids.h"
#include "CSG.h"
#include "stdlib.h"
#include <iostream>

using namespace std;

int main() {
  cin.ignore();
  double x = 100.;
  double y = 100.;
  double z = 10.;
  CSG *b = Solids::Box(x,y,z);
  double epsilon = 0.1;

  CSG *sub_cub = Solids::Box(x-epsilon,z-epsilon,z);
  sub_cub->translate(Vector(0.0,(z/2.)-(y/2.)-20,epsilon));
  CSG* old;
  for(int i=0;i<2;i++){
    old = b;
    Vector v = Vector(0.0,20.0,0.0);
    sub_cub->translate(v);
    b = b->Subtract(sub_cub); 
    cout << i << " pos sub" << endl;
    delete old;
  }
  delete sub_cub;
  sub_cub = Solids::Box(z-epsilon,y-epsilon,z);

  sub_cub->translate(Vector((z/2.)-(x/2.)-20,0.0,epsilon));
  for(int i=0;i<2;i++){
    old = b;
    Vector v = Vector(20.0,0.0,0.0);
    sub_cub->translate(v);
    b = b->Subtract(sub_cub); 
    cout << i << " post sub2" << endl;
    delete old;
  }
  //Vector v = Vector(5,5,5);
  //b2->translate(v);
  
  
  b->saveVTK("b.vtk");
}
