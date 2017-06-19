#include <CSGMesh.h>
#include <Solids.h>
#include <SolidBase.h>
#include <Vector.h>

class CutTubs : public SolidBase{
  public:
  CutTubs(std:: string name,double _pRmin,double _pRmax,double _pDz,double _pSPhi,double _pDPhi,double _pLowNorm,double _pHighNorm):
    SolidBase(name,"Cuttubs"),pRmin(_pRmin), pRmax(_pRmax), pDz(_pDz), pSPhi(_pSPhi), pDPhi(_pDPhi), pLowNorm(_pLowNorm), pHighNorm(_pHighNorm);
  {
    SetMesh(CSGMesh::ConstructCutTubs(pRmin, pRmax, pDz, pSPhi, pDPhi, pLowNorm, pHighNorm));
  } 
  const double pRmin, pRmax, pDz, pSPhi, pDPhi;
  Vector* pLowNorm, pHighNorm;
};

CSG* CSGMesh::ConstructCutTubs(double pRmin,double pRmax,double pDz,double pSPhi,double pDPhi,Vector* pLowNorm,Vector* pHighNorm){
  Tubs* basictubs = Tubs("tubs_temp",pRmin,pRmax,pDz,pSPhi,pDPhi);
  CSG* basicmesh = basictubs->GetMesh();
  if((pLowNorm->x() != 0.0 || pLowNorm->y() != 0.0 || pLowNorm->z() != -1.0)
      || (pHighNorm->x() != 0.0 || pHighNorm->y() != 0.0 || pHighNorm->z() != 1.0)){
    CSG* mesh;
    double zlength = 3.0*pDz; //make the dimensions of the semi-infinite plane large enough

    if(pHighNorm->x() != 0.0 || pHighNorm->y() != 0.0 || pHighNorm->z() != 1.0){
      Plane* pHigh_temp = new Plane("pHigh_temp",pHighNorm,pDz,zlength);
      CSG* pHigh = pHigh_temp->GetMesh();
      mesh = basicmesh->subtract(pHigh);
    }
    if(pLowNorm->x() != 0.0 || pLowNorm->y() != 0.0 || pLowNorm->z() != -1.0){
      Plane* pLow_temp = new Plane("pLow_temp",pLowNorm,-pDz,zlength);
      CSG* pLow = pLow_temp->GetMesh();
      mesh = basicmesh->subtract(pLow);
    }
    return mesh;
  }
  else{
    return basicmesh;
  } 
}
