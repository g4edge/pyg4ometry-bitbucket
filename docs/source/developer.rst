Developer
=========

Unit tests
----------

.. code-block :: console 

   cd pyg4ometry/test
   pytest

Coverage
--------

.. code-block :: console

   cd pyg4ometry/coverage
   ./runCoverage.sh
 
Profiling
---------

.. code-block :: console

   python -m cProfile -s tottime myscript.py > myscript.log

.. code-block :: console

   pycallgraph graphviz -- ../pyg4ometry/test/python/T008_Sphere.py

Updating A Version
------------------

Update the version number in the following files:

* `setup.py`
* `setup.cfg`
* `pyg4ometry/docs/source/conf.py`

Make manual and commit to `pyg4ometry/docs/pyg4ometry.pdf`.

Updating Copyright
------------------

Update the year in the following files:

* `LICENCE.txt`
* `README.md`
* `docs/source/conf.py`
* `docs/source/licence.rst`

