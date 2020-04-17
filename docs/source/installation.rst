============
Installation
============


Requirements
------------

 * pyg4ometry is developed exclusively for Python 2.7 (Python3 coming soon)
 * `VTK (Visualisation toolkit) <https://vtk.org>`_
 * `Freecad <0.17 <https://www.freecadweb.org>`_
 * `antlr4 <https://www.antlr.org>`_
 * `cython <https://cython.org>`_
 * `GitPython <https://gitpython.readthedocs.io/en/stable/>`_
 * `matplotlib <https://matplotlib.org>`_
 * `CGAL <https://www.cgal.org>`_

Installation
------------

To install pyg4ometry, simply run ``make install`` from the root pyg4ometry
directory::

  cd /my/path/to/repositories/
  git clone http://bitbucket.org/jairhul/pyg4ometry
  cd pyg4ometry
  make install

.. note::
   To build using the git directory and not installing into /usr/local use ``make develop`` 
   instead of ``make install``

To build pycsg with cpython::

  make build_ext

Or install from pypi::

  pip install pyg4ometry

or alternatively, run ``make develop`` from the same directory to ensure
that any local changes are picked up.

FreeCAD support for CAD to GDML conversion
------------------------------------------

For FreeCAD support and you already have it installed you  need to add library to PYTHONPATH, for example 

.. code-block :: console 
   
   export PYTHONPATH=/opt/local/libexec/freecad/lib/

Building FreeCAD can be a pain for MAC so 

.. code-block :: console 

   mkdir FreeCAD
   cd FreeCAD 
   set FCROOT=$pwd
   wget  https://github.com/FreeCAD/FreeCAD/archive/0.19_pre.tar.gz
   tar zxf 0.19_pre.tar.gz
   mkdir build
   mkdir install 
   cd build
   cmake ../FreeCAD-0.18.4 -DCMAKE_INSTALL_PREFIX=../install \
   -DCOIN3D_LIBRARIES=/opt/local/Library/Frameworks/Inventor.framework/Libraries/libCoin.dylib -DBUILD_FEM=0 \
   -DBUILD_MATERIAL=0 -DBUILD_SHIP=0 -DBUILD_DRAFT=0 -DBUILD_TUX=0 -DBUILD_ARCH=0 -DBUILD_PLOT=0 \
   -DBUILD_OPENSCAD=0  
   make -jN
   make install 
   export PYTHONPATH=$PYTHONPATH:$FCROOT/install 


      

