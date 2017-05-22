all : _Vector.so _Vertex.so

_%.so : %.o %_wrap.o
	g++ -shared $? -L/opt/local/lib/ -lpython2.7 -o $@

%.o : %.C
	g++ -O2 -fPIC -c $< -I./

%.o : %.cxx
	g++ -O2 -fPIC -c $< -I/opt/local/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/

%_wrap.cxx : %.i
	swig -c++ -python -shadow $<

clean :
	rm -rf *.so *.o *_wrap.cxx *.pyc

