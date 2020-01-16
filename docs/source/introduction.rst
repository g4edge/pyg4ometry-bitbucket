============
Introduction
============

This package started as an internal tool for the BDSIM and machine backgrounds 
group at Royal Holloway. BDSIM is a tool to rapidly create Geant4 models of 
accelerator systems. Creation of geometry is a time consuming activity and 
pyg4ometry hopefully will improve the time take to create accurate reliable 
geometry flies.

Need for programatic geometry generation
----------------------------------------

 * Non-expert user creation and maintainence of geometry
 * Reduce time spent creating geometry
 * Reproducibility
 * Lower number of errors 
 * Parametrisation of geometry
 * Visualisation of geometry
 * Overlap checking
 * Import from other geometry packages

Geant4 key concepts 
-------------------
 
 * GMDL

Geometry key concepts
---------------------

 * Constructive Solid Geometry (CSG)
 * Boolean operations
 * Boundary representation (B-REP)
 * Boundary mesh

Implementation concepts
-----------------------

 * Registry 
 * Parameter
 * ParameterVector
 * Pycsg
