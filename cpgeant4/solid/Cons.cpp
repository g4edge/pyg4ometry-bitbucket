#include <CSGMesh.h>
#include <Solids.h>
#include <SolidBase.h>
#include <Vector.h>
#include <Wedge.h>

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


  double wrmax = 3.0*(pRmax1+pRmax2); // ensure radius for intersection wedge is much bigger than solid
  double wzlength = 3.0*pDz;

  CSG* pWedge; 
  if( pDPhi != 2.0*M_PI ){
    Wedge* wedge = new Wedge("wedge_temp",wrmax,pSPhi,pSPhi+pDPhi,wzlength);
    pWedge = wedge->GetMesh();
  }
  else{
    pWedge = Solids::Cylinder(5.*pDz,5.*R1);
  }

  Plane* TopCutPlane = new Plane("pTopCut_temp",new Vector(0.0,0.0,1.0),pDz,wzlength);
  CSG* pTopCut = TopCutPlane->GetMesh();

  Plane* BotCutPlane = new Plane("pBotCut_temp",new Vector(0.0,0.0,-1.0),-pDz,wzlength);
  CSG* pBotCut = BotCutPlane->GetMesh();

  CSG* mesh;
  if(H2 != 0.){
    CSG* sInner = Solids::Cone(new Vector(0.,0.,-factor*pDz),new Vector(0.0,0.0,h2-factor*pDz),r1);
    mesh = basicmesh->Subtract(sInner)->Intersect(pWedge)->Subtract(pBotCut)->Subtract(pTopCut);
  }
  else{
    mesh = basicmesh->Intersect(pWedge)->Subtract(pBotCut)->Subtract(pTopCut); 
  }
  return mesh;
}
