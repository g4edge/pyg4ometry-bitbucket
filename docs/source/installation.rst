============
Installation
============


Requirements
------------

 * pyg4ometry is developed exclusively for Python 2.7.
 * VTK (Visualisation toolkit)
 * Freecad >0.17

Installation
------------

To install pyg4ometry, simply run ``make install`` from the root pyg4ometry
directory.::

  cd /my/path/to/repositories/
  git clone http://bitbucket.org/jairhul/pyg4ometry
  cd pyg4ometry
  make install

Or install from pypi.::

  pip install pyg4ometry

or alternatively, run ``make develop`` from the same directory to ensure
that any local changes are picked up.

For FreeCAD support need to add library to PYTHONPATH

.. code-block :: console 
   
   export PYTHONPATH=/opt/local/libexec/freecad/lib/


