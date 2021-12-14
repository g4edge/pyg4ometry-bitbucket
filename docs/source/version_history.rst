===============
Version History
===============

v1.0.0 - 2021 / 12 / 17
=======================

New Features
------------

* Geometry comparison tests for comparing two different geometry trees.
* Copy number for physical volumes.
* Overlap checking for assembly and replica volumes.
* Ability to analyse a registry structure and usage of objects throughout.
* ROOT geometry loader.

General
-------

* Improved documentation and docstrings.
* Refactored registry for transfer and object versus simply adding an object.
* Optimised imports.
* Cleanded up private imports throughout code to make tab complete cleaner.
* Simplified code in solids by using base class.

Bug Fixes
---------

* Improved search paths for libraries in setup.py.
* Fix merging of registries - object names won't be altered if they don't have to be.
  Fixed a clash with scales.
* Fixed conversion of FLUKA materials to Geant4 - many fixes.
* Fixed some material issues when converting Geant4 to FLUKA.


v0.9.0 - 2021 / 07 / 01
=======================

* Working version regularly used, submitted to CPC Journal for review.
* Based on CGAL for Boolean mesh operations, using pybind11, whereas previously
  was based on pycgal.
* FLUKA conversion to pyg4ometry and GDML has been reimplemented from the pyfluka
  package.
* Extensive code testing has been introduced and basic functionality documented.
* Given the strictness of CGAL, many bugs in meshing algorithms were fixed for all
  solids in `pyg4ometry.geant4.solid`.

Pre-History
===========

* v0.2.0 - 2018 / 06 / 23
* v0.1.4 - 2018 / 06 / 04
* v0.1.2 - 2018 / 06 / 03
* v0.1.1 - 2018 / 06 / 03
* v0.1.0 - 2017 / 06 / 05
* v0.4.0 - 2017 / 10 / 17
* v0.3.0 - 2017 / 07 / 06
