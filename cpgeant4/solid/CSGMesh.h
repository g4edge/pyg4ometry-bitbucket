#ifndef __CSG_MESH_H__
#define __CSG_MESH_H__
#include "CSG.h"
#include "Vector.h"

namespace CSGMesh{
  CSG* ConstructBox(double px,double py,double pz);
  CSG* ConstructCons(double pRmin1, double pRmax1, double pRmin2,double pRmax2, double pDz, double pSPhi, double pDPhi);
  CSG* ConstructWedge(double pRMax,double pSPhi,double pDPhi,double halfzlength);
  CSG* ConstructPlane(Vector* normal,double dist,double zlength);
  CSG* ConstructTubs(double pRmin,double pRmax,double pDz,double pSPhi,double pDPhi);
  CSG* ConstructCutTubs(double pRmin,double pRmax,double pDz,double pSPhi,double pDPhi,Vector* pLowNorm,Vector* pHighNorm);
  CSG* ConstructTrap(double pDz, double pTheta, double pDPhi, double pDy1, double pDx1, double pDx2, double pAlp1, double pDy2, double pDx3, double pDx4, double pAlp2);
  CSG* ConstructTwistedBox(double twistedangle, double pDx, double pDy, double pDz, int refine);
};

#endif