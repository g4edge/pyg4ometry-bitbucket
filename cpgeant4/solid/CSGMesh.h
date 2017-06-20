#ifndef __CSG_MESH_H__
#define __CSG_MESH_H__
#include "CSG.h"
#include "Vector.h"

struct ZSection;

namespace CSGMesh{
  CSG* ConstructBox(double px,double py,double pz);
  CSG* ConstructCons(double pRmin1, double pRmax1, double pRmin2,double pRmax2, double pDz, double pSPhi, double pDPhi);
  CSG* ConstructWedge(double pRMax,double pSPhi,double pDPhi,double halfzlength);
  CSG* ConstructPlane(Vector* normal,double dist,double zlength);
  CSG* ConstructTubs(double pRmin,double pRmax,double pDz,double pSPhi,double pDPhi);
  CSG* ConstructCutTubs(double pRmin,double pRmax,double pDz,double pSPhi,double pDPhi,Vector* pLowNorm,Vector* pHighNorm);
  CSG* ConstructTrap(double pDz, double pTheta, double pDPhi, double pDy1, double pDx1, double pDx2, double pAlp1, double pDy2, double pDx3, double pDx4, double pAlp2);
  CSG* ConstructTwistedBox(double twistedangle, double pDx, double pDy, double pDz, int refine);
  CSG* ConstructExtrudedSolid(std::vector<Vector*> pPolygon,std::vector<ZSection> pZslices);
  CSG* ConstructSphere(double pRmin,double pRmax,double pSPhi,double pDPhi,double pSTheta,double pDTheta,int nslice, int nstack);
  void SphereAppendVertex(std::vector<Vertex*>& vertices,double theta,double phi,double r);
  CSG* ConstructTet(Vector* anchor,Vector* p2,Vector* p3,Vector* p4,bool degeneracyFlag);
  CSG* ConstructTorus(double pRmin,double  pRmax,double  pRtor,double  pSPhi,double  pDPhi,int nslice,int nstack);
  void TorusAppendVertex(std::vector<Vertex*>& vertices,double theta,double phi,double r,double pRtor);
};

struct ZSection{
  ZSection(double _z,Vector* _offset,double _scale):
      z(_z),offset(_offset),scale(_scale) {}
  double z;
  Vector* offset;
  double scale;
};
#endif