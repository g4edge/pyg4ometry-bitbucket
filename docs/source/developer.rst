Developer
=========

Coverage
--------

.. code-block :: console

   cd pyg4ometry/pyg4ometry/test/
   coverage-2.7 run --source pyg4ometry ./runTests.py
   coverage report -m
 
Profiling
---------

.. code-block :: console

   python2.7 -m cProfile -s tottime myscript.py > myscript.log

.. code-block :: console

   pycallgraph-2.7 graphviz -- ../pyg4ometry/test/python/T008_Sphere.py

