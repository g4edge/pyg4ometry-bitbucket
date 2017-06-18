#include <CSGMesh.h>
#include <Solids.h>
#include <SolidBase.h>
#include <Vector.h>

class Cons: public SolidBase{
  public:
  Cons(std::string name, _pRmin1,  _pRmax1,  _pRmin2, _pRmax2,  _pDz,  _pSPhi,  _pDPhi):
    SolidBase(name,"Cons"), pRmin1(_pRmin1),  pRmax1(_pRmax1),  pRmin2(_pRmin2), pRmax2(_pRmax2),  pDz(_pDz),  pSPhi(_pSPhi),  pDPhi(_pDPhi);
  {
    SetMesh(CSGMesh::ConstructCons( pRmin1,  pRmax1,  pRmin2, pRmax2,  pDz,  pSPhi,  pDPhi));
  }
  const double pRmin1,  pRmax1,  pRmin2, pRmax2,  pDz,  pSPhi,  pDPhi;
};

CSG* CSGMesh::ConstructCons( pRmin1,  pRmax1,  pRmin2, pRmax2,  pDz,  pSPhi,  pDPhi){
  double R1,r1,R2,r2;
  double factor;
  if(pRmax1 < pRmax2){
    R1 = pRmax2;
    r1 = pRmin2;
    R2 = pRmax1;
    r2 = pRmin1;
    factor = -1.0;
  }
  else{
    R1 = pRmax1;
    r1 = pRmin1;
    R2 = pRmax2;
    r2 = pRmin2;
    factor = 1.0;
  }
  double h = 2.0*pDz; 
  double H1 = (R2*h)/(R1-R2);
  double H2 = 0.;
  if(r1-r2 != 0.0){
    H2 = (r2*h)/(r1-r2);
  }

  double h1 = factor*(h+H1);
  double h2 = factor*(h+H2);

  CSG* basicmesh = Solids::Cone(new Vector(0.0,0.0,-factor*pDz),new Vector(0.0,0.0,h1-factor),R1);

}
