#ifndef __SOLID_BASE_H__
#define __SOLID_BASE_H__
#include <string>
#include <CSG.h>


class SolidBase{
  public:
    SolidBase(std::string _name,std::string _type);
    virtual ~SolidBase();
    void SetMesh(CSG* _mesh);
    CSG* GetMesh();
    std::string GetName();
    std::string GetType();
  private:
    std::string name;
    std::string type;
    CSG* mesh;
};

#endif
