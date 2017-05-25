#include "Vector.h"
#include "Solids.h"
#include "CSG.h"

int main() {
  CSG *b1 = Solids::Box(10,10,10);
  CSG *b2 = Solids::Box(5,5,5);
  Vector v = Vector(5,5,5);
  b2->translate(v);
  
  b1->saveVTK("b1.vtk");
  
  b1->Subtract(b2);
  b2->saveVTK("b2.vtk");
  b1->saveVTK("bu.vtk");
}
