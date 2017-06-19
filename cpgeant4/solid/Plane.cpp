#include <CSGMesh.h>
#include <Solids.h>
#include <SolidBase.h>
#include <Vector.h>

class Plane : public SolidBase{
  public:
  Plane(std::string name, Vector* _normal,double _dist, double _zlength=10000):
    SolidBase(name,"Plane"),normal(_normal),dist(_dist),zlength(_zlength){
      SetMesh(CSGMesh::ConstructPlane(normal,dist,zlength)); 
    }
  const dist,zlength;
  const Vector* normal;
};
  

CSG* CSGMesh::ConstructPlane(Vector* normal,double dist,double zlength){
  Vector unorm = normal->unit();
  double d = zlength;
  CSG* c = CSG::Box(20*d,20*d,2*d);
  double dp = unorm.dot(Vector(0.,0.,1.));

  if( dp != 1 && dp != -1){
    Vector* cp = new Vector(unorm.cross(Vector(0.,0.,10)));
    double an = acos(dp);
    an = (an/M_PI)*180.; 
    c->rotate(cp,an);
  }
  c->translate(new Vector(0.0,0.0,dist+d/dp));
  return c;
}
