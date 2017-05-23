all : _Vector.so _Vertex.so

_Plane.so : Plane.o Plane_wrap.o _Polygon.so
	g++ -shared Plane.o Plane_wrap.o ./_Vector.so ./_Vertex.so ./_Polygon.so -L/opt/local/lib/ -lpython2.7 -o $@

_Polygon.so : Polygon.o Polygon_wrap.o
	g++ -shared Polygon.o Polygon_wrap.o ./_Vector.so ./_Vertex.so -L/opt/local/lib/ -lpython2.7 -o $@

_Vertex.so : Vertex.o Vertex_wrap.o
	g++ -shared Vertex.o Vertex_wrap.o ./_Vector.so -L/opt/local/lib/ -lpython2.7 -o $@

_Vector.so : Vector.o Vector_wrap.o
	g++ -shared Vector.o Vector_wrap.o -L/opt/local/lib/ -lpython2.7 -o $@

%.o : %.C
	g++ -O2 -fPIC -c $< -I./

%.o : %.cxx
	g++ -O2 -fPIC -c $< -I/opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/

%_wrap.cxx : %.i
	swig -c++ -python -shadow $<

clean :
	rm -rf *.so *.o *_wrap.cxx *.pyc

