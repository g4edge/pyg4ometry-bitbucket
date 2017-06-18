#include "CSG.h"
#include "Vector.h"

namespace CSGMesh{
  CSG* ConstructBox(double px,double py,double pz);
  CSG* ConstructCons(double pRmin1, double pRmax1, double pRmin2,double pRmax2, double pDz, double pSPhi, double pDPhi);
  CSG* ConstructWedge(double pRMax,double pSPhi,double pDPhi,double halfzlength);
  CSG* ConstructPlane(Vector* normal,double dist,double zlength);
};
