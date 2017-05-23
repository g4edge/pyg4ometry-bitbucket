all : _Vector.so _Vertex.so


csg.so : Vector.o Vertex.o Polygon.o Plane.o Solids.o
	g++ -shared -o csg.so $? -L/opt/local/lib/ -lpython2.7

_BSPNode.so : BSPNode.o BSPNode_wrap.o
	g++ -shared BSPNode_wrap.o -L/opt/local/lib/ -lpython2.7 -o $@

_CSG.so : CSG.o CSG_wrap.o
	g++ -shared CSG_wrap.o ./csg.so -L/opt/local/lib/ -lpython2.7 -o $@

_Plane.so : Plane.o Plane_wrap.o _Polygon.so
	g++ -shared Plane_wrap.o ./csg.so  -L/opt/local/lib/ -lpython2.7 -o $@

_Polygon.so : Polygon.o Polygon_wrap.o
	g++ -shared Polygon_wrap.o ./csg.so -L/opt/local/lib/ -lpython2.7 -o $@

_Vertex.so : Vertex.o Vertex_wrap.o
	g++ -shared Vertex_wrap.o ./csg.so -L/opt/local/lib/ -lpython2.7 -o $@

_Vector.so : Vector_wrap.o
	g++ -shared Vector_wrap.o ./csg.so -L/opt/local/lib/ -lpython2.7 -o $@

%.o : %.C
	g++ -O2 -fPIC -c $< -I./

%.o : %.cxx
	g++ -O2 -fPIC -c $< -I/opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/

%_wrap.cxx : %.i
	swig -c++ -python -shadow $<

clean :
	rm -rf *.so *.o *_wrap.cxx *.pyc

