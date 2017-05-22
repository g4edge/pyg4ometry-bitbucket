#include <CSG.h>    

CSG::CSG(){
  
}
~CSG(){
  for(unsigned i=0;i<polygons.size();i++){
    delete polygons[i];
  }
  polygons.clear();
}

CSG* CSG::fromPolygons(vector<Polygon*> _polygons){
  CSG* csg = new CSG();
  csg->polygons = polygons;
  return csg;
} 

CSG* CSG::clone(){
  CSG* newcsg = new CSG();
  vector<Polygon*> npolygons(this->polygons.size());
  for(unsigned i=0;i<this->polygons.size();i++){
    npolygons[i] = this->polygons[i]->clone();
  }
  newcsg->polygons = npolygons;
  return newcsg;
} 

std::vector<Polygon*> CSG::toPolygons(){
  return this->polygons;
}

CSG* CSG::refine(){
  CSG* newCSG = new CSG();
  for(unsigned i=0;i<this->polygons.size();i++){
    vector<Vertex> verts = polygons[i]->vertices;
    unsigned numVerts = verts.size();
    if(numVerts == 0){
      continue;
    }
    Vector midPos(0.0,0.0,0.0);
    for(int j=0;j<verts.size();j++){
      midPos = midPos + verts[j].pos;
    }
    midPos = midPos / double(numVerts);
    Vector midVert;
    if(verts[0].HasNorm()){
      Vector midNormal = (polygons[i]->plane)->normal();
      midVert = Vertex(midPos,midNormal);
    } 
    else{
      midVert = Vertex(midPos, midNormal);
    }
    vector<Vertex> newVerts = verts;
    for(int j=0;j<numVerts;j++){
      newVerts.push_back(verts[j].interpolate(verts[(i+1)%numVerts],0.5));
    }
    newVerts.push_back(midVert);
    vector<Vertex> vs(4);
    vs[0] = newVerts[0];
    vs[1] = newVerts[numVerts];
    vs[2] = newVerts[2*numVerts];
    vs[3] = newVerts[2*numVerts-1];


  }
}
    void translate(double disp);
    void scale(double scale);
    void rotate(Vector* axis,double angleDeg);
    struct VertsAndPolys;
    VertsAndPolys toVerticesAndPolygons();
    void saveVTK(std::string filename);
    CSG* union(CSG* csg);
    CSG* operator+(CSG* csg);
    CSG* subtract(CSG* csg);
    CSG* operator-(CSG* csg);
    CSG* intersect(CSG* csg);
    CSG* operator*(CSG* csg);
    CSG* inverse();

    static CSG* cube();
    static CSG* sphere();
    static CSG* cylinder();
    static CSG* cone();


