#ifndef __ORB_H__
#define __ORB_H__
#include "CSGMesh.h"
#include "Solids.h"
#include "SolidBase.h"

class Orb : public SolidBase{
public:
  Orb(std::string name,double _pRmax):
      SolidBase(name,"Orb"),pRmax(_pRmax)
  {
    SetMesh(CSGMesh::ConstructOrb(pRmax));
  }
  const double pRmax;
};
#endif
