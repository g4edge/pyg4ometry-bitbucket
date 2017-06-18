#include <string>
#include <CSG.h>


class SolidBase{
  public:
    SolidBase(std::string _name,std::string _type);
    virtual ~SolidBase();
    SetMesh(CSG* _mesh);
    CSG* GetMesh();
  private:
    std::name;
    std::type;
    CSG* mesh;
};
