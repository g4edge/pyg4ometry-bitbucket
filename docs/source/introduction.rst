============
Introduction
============

This package started as an internal tool for the BDSIM and machine backgrounds 
group at Royal Holloway. BDSIM is a tool to rapidly create Geant4 models of 
accelerator systems. Creation of geometry is a time consuming activity and 
pyg4ometry hopefully will improve the time taken to create accurate reliable 
geometry flies.

Need for programatic geometry generation
----------------------------------------

 * Non-expert user creation and maintenance of geometry
 * Reduce time spent creating geometry
 * Reproducibility
 * Lower number of errors 
 * Parameterisation of geometry
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

.. _introduction-registry:

Registry
********


 * Parameter
 * ParameterVector
 * Pycsg

Publications 
------------

On pyg4ometry 
 * `Pyg4ometry : A Tool To Create Geometries For Geant4, Bdsmi, G4Beamline and Fluka For Particle Loss and Energy Deposit Studies, IPAC2019, Melbourne, Australia, 2019 <https://doi.org/10.18429/JACoW-IPAC2019-WEPTS054>`_ Google scholar `cites <https://scholar.google.com/scholar?cites=7483314837088930734&as_sdt=2005&sciodt=0,5&hl=en>`_

