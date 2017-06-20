#ifndef __EXTRUDED_SOLID_H__
#define __EXTRUDED_SOLID_H__
#include "CSGMesh.h"
#include "Solids.h"
#include "SolidBase.h"
#include "Vector.h"
#include <vector>

class ExtrudedSolid : public SolidBase{
public:
  ExtrudedSolid(std:: string name,std::vector<Vector*> _pPolygon,std::vector<ZSection> _pZslices):
      SolidBase(name,"ExtrudedSolid")
  {
    pPolygon = _pPolygon;
    pZslices = _pZslices;
    SetMesh(CSGMesh::ConstructExtrudedSolid(pPolygon,pZslices));
  }
  std::vector<Vector*> pPolygon;
  std::vector<ZSection> pZslices;
};
#endif
