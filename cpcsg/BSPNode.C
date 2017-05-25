#include "BSPNode.h"

BSPNode::BSPNode(){
  plane = NULL;
  front = NULL;
  back = NULL;
}

BSPNode::BSPNode(std::vector<Polygon*> &_polygons){
  plane = NULL;
  front = NULL;
  back = NULL;
  build(_polygons);
}

BSPNode::~BSPNode(){
  delete plane;
  delete front;
  delete back;
  for(int i=0;i<polygons.size();i++){
    delete polygons[i];
  }
  polygons.clear();
}

BSPNode* BSPNode::clone(){
  BSPNode* node = new BSPNode();
  if(plane){
    node->plane = this->plane;
  }
  if(front){
    node->front = this->front;
  }
  if(back){
    node->back = this->back;
  }
  if(polygons.size() > 0){
    std::vector<Polygon*> npolygons;
    for(unsigned i=0;i<polygons.size();i++){
      npolygons.push_back(polygons[i]->clone());
    }
    node->polygons = npolygons;
  }
  return node;
}

void BSPNode::invert(){
  for(unsigned i=0;i<polygons.size();i++){
    polygons[i]->flip();
  }
  plane->flip();
  if(front){
    front->invert();
  }
  if(back){
    back->invert();
  }
  BSPNode* temp = front;
  front = back;
  back = temp;
}
    
std::vector<Polygon*> BSPNode::clipPolygons(std::vector<Polygon*> &_polygons){
  if(!plane){
    return _polygons; 
  }
  std::vector<Polygon*> _front;
  std::vector<Polygon*> _back;
  for(unsigned i=0;i<_polygons.size();i++){
    plane->splitPolygon(_polygons[i],_front,_back,_front,_back);
  }
  if(front){
    _front = front->clipPolygons(_front);
  }
  if(back){
    _back = back->clipPolygons(_back);
  }
  _front.insert(_front.end(),_back.begin(),_back.end());
  return _front;
}

void BSPNode::clipTo(BSPNode *bsp){
  polygons = bsp->clipPolygons(polygons);
  if(front){
    front->clipTo(bsp);
  }
  if(back){
    back->clipTo(bsp);
  }
}

std::vector<Polygon*> BSPNode::allPolygons(){
  std::vector<Polygon*> polygons = this->polygons;
  if(front){
    polygons.insert(polygons.end(),front->allPolygons().begin(),front->allPolygons().end());
  }
  if(back){
    polygons.insert(polygons.end(),back->allPolygons().begin(),back->allPolygons().end());
  }
  return polygons;
}

void BSPNode::build(std::vector<Polygon*> _polygons){
  if(_polygons.size() == 0){
    return;
  }
  if(!plane){
    plane = _polygons[0]->plane->clone();
  }
  polygons.push_back(_polygons[0]);
  std::vector<Polygon*> _front;
  std::vector<Polygon*> _back;
  for(unsigned i = 1;i<_polygons.size();i++){
    plane->splitPolygon(_polygons[i],polygons,polygons,_front,_back);
  }
  if(_front.size() > 0){
    if(!front){
      front = new BSPNode();
    } 
    front->build(_front);
  }
  if(_back.size() > 0){
    if(!back){
      back = new BSPNode();
    }
    back->build(_back);
  } 
}

