#include "SolidBase.h"

SolidBase::SolidBase(std::string _name,std::string _type):name(_name),type(_type){

}

SolidBase::~SolidBase(){
  delete mesh;
}

SolidBase::SetMesh(CSG* _mesh){
  mesh = _mesh;
}

SolidBase::GetMesh(){
  return mesh;
}
