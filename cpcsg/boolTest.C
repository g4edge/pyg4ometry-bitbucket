#include "Vector.h"
#include "Solids.h"
#include "CSG.h"

int main() {
  CSG *b1 = Solids::Box(10,10,10);
  CSG *b2 = Solids::Box(10,10,10);
  Vector v = Vector(5,5,5);
  b2->translate(v);
  b1->Subtract(b2);
  
  b1->saveVTK("ra.vtk");
}
