.. _analysing:

=============
CAD interface
=============

There are multiple different ways to interact with a CAD model. A compelete solid can be 
converted to a tesselated solid. The Open Cascade API has a wealth of ways of creating, 
exploring and modifying CAD models. Pyg4ometry provides a pybind11 python interface to Open 
Cascade. As pyg4ometry just wraps OpenCascade classes the manual for OpenCascade are very useful 

* https://dev.opencascade.org/doc/overview/html/
* https://dev.opencascade.org/doc/refman/html/



Controlling tesselation 
-----------------------

There are two parameters to control the tesselation quality, the linear and angular deviation. 


Setting materials 
-----------------



Object names 
------------ 

Two (or more) object within a CAD file can have the same name. This will cause a problem for the GDML (and the Registry). 


Tetrahedralisation 
------------------

Sometimes it is appropriate to use a tetrahedralisation opposed to a surface mesh. 


Topology exploration
--------------------

The topology of solid can be traversed using Open Cascade. 






