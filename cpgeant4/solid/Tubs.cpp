#include <CSGMesh.h>
#include <Solids.h>
#include <SolidBase.h>

class Tubs : public SolidBase{
  public:
  Tubs(std::string name,double _pRmin,double _pRmax,double _pDz,double _pSPhi,double _pDPhi):
    SolidBase(name,"Tubs"), pRmin(_pRmin), pRmax(_pRmax), pDz(_pDz), pSPhi(_pSPhi), pDPhi(_pDPhi)
  {
    SetMesh(CSGMesh::ConstructTubs(pRmin, pRmax, pDz, pSPhi, pDPhi);
    const double pRmin, pRmax, pDz, pSPhi, pDPhi;
  }
};

CSG* CSGMesh::ConstructTubs(double pRmin,double pRmax,double pDz,double pSPhi,double pDPhi){
  CSG* basicmesh = Solids::Cylinder(pDz,pRmax);

  if(pRmin == 0 && pSPhi == 0.0 && pDPhi == 2.0*M_PI){
    return basicmesh;
  }
  double wzlength = 3.0*pDz;
  double wrmax = 3.0*pRmax;

  CSG* pWedge;
  if(pDPhi == 2.0*M_PI){
    Wedge* wedge_temp = new Wedge("wedge_temp",wrmax,pSPhi,pSPhi+pDPhi-0.0001,wzlength);
    pWedge = wedge_temp->GetMesh();
  }
  else{
    Wedge* wedge_temp = new Wedge("wedge_temp",wrmax,pSPhi,pSPhi+pDPhi,wzlength);
    pWedge = wedge_temp->GetMesh();
  }
  CSG* mesh;
  if(pRmin != 0.0){
    CSG* sInner = Solid::Cylinder(pDz,pRmin);
    mesh = basicmesh->Subtract(sInner)->Subtract(pWedge->Inverse());
  }
  else{
    mesh = basicmesh->Subtract(pWedge->Inverse());
  }
  return mesh;
}
